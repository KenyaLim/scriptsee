"""Rule-based IPv4/TCP port-scan detector.

The detector is deliberately independent of packet capture. It accepts packet
features, so the same logic can be tested with PCAP files or live traffic.
"""

from __future__ import annotations

import csv
import time
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Deque, Dict, Iterable, Optional, Tuple


FlowKey = Tuple[str, str]


@dataclass(frozen=True)
class PacketFeature:
    timestamp: float
    source_ip: str
    destination_ip: str
    destination_port: int
    flags: str


@dataclass
class DetectionConfig:
    window_seconds: float = 10.0
    ttl_seconds: float = 30.0
    unique_ports_threshold: int = 10
    connections_threshold: int = 20
    syn_ratio_threshold: float = 0.70
    min_packets_for_ratio: int = 5


@dataclass
class FlowState:
    events: Deque[PacketFeature] = field(default_factory=deque)
    last_seen: float = 0.0
    expires_at: float = 0.0


@dataclass(frozen=True)
class Alert:
    timestamp: float
    source_ip: str
    destination_ip: str
    unique_ports: int
    connections: int
    syn_ratio: float
    reason: str

    def as_dict(self) -> dict[str, str]:
        return {
            "timestamp": datetime.fromtimestamp(
                self.timestamp, tz=timezone.utc
            ).isoformat(),
            "source_ip": self.source_ip,
            "destination_ip": self.destination_ip,
            "unique_ports": str(self.unique_ports),
            "connections": str(self.connections),
            "syn_ratio": f"{self.syn_ratio:.4f}",
            "reason": self.reason,
        }


class PortScanDetector:
    """Maintain bounded flow state and emit at most one alert per active flow."""

    def __init__(self, config: Optional[DetectionConfig] = None) -> None:
        self.config = config or DetectionConfig()
        if self.config.window_seconds <= 0 or self.config.ttl_seconds <= 0:
            raise ValueError("window_seconds and ttl_seconds must be positive")
        if self.config.ttl_seconds < self.config.window_seconds:
            raise ValueError("ttl_seconds must be >= window_seconds")
        if self.config.unique_ports_threshold < 1:
            raise ValueError("unique_ports_threshold must be positive")
        self._states: Dict[FlowKey, FlowState] = {}
        self._alerted: set[FlowKey] = set()

    @property
    def state_count(self) -> int:
        return len(self._states)

    def expire(self, now: Optional[float] = None) -> None:
        """Remove flow records whose TTL has elapsed."""
        current = time.time() if now is None else now
        expired = [
            key for key, state in self._states.items()
            if state.expires_at <= current
        ]
        for key in expired:
            self._states.pop(key, None)
            self._alerted.discard(key)

    def process(self, packet: PacketFeature) -> Optional[Alert]:
        if not 0 <= packet.destination_port <= 65535:
            raise ValueError("destination_port must be between 0 and 65535")
        self.expire(packet.timestamp)
        key = (packet.source_ip, packet.destination_ip)
        state = self._states.setdefault(key, FlowState())
        cutoff = packet.timestamp - self.config.window_seconds
        while state.events and state.events[0].timestamp < cutoff:
            state.events.popleft()
        state.events.append(packet)
        state.last_seen = packet.timestamp
        state.expires_at = packet.timestamp + self.config.ttl_seconds

        if key in self._alerted:
            return None
        alert = self._evaluate(packet.timestamp, key, state)
        if alert is not None:
            self._alerted.add(key)
        return alert

    def _evaluate(
        self, timestamp: float, key: FlowKey, state: FlowState
    ) -> Optional[Alert]:
        events = state.events
        unique_ports = len({event.destination_port for event in events})
        connections = len(events)
        syn_packets = sum("S" in event.flags for event in events)
        syn_ratio = syn_packets / connections if connections else 0.0
        reasons = []
        if unique_ports >= self.config.unique_ports_threshold:
            reasons.append("unique_ports_threshold")
        if connections >= self.config.connections_threshold:
            reasons.append("connections_threshold")
        if (
            connections >= self.config.min_packets_for_ratio
            and syn_ratio >= self.config.syn_ratio_threshold
        ):
            reasons.append("syn_ratio_threshold")
        if not reasons:
            return None
        return Alert(
            timestamp=timestamp,
            source_ip=key[0],
            destination_ip=key[1],
            unique_ports=unique_ports,
            connections=connections,
            syn_ratio=syn_ratio,
            reason=",".join(reasons),
        )

    def process_many(self, packets: Iterable[PacketFeature]) -> list[Alert]:
        return [
            alert
            for packet in packets
            if (alert := self.process(packet)) is not None
        ]


def read_pcap(path: str | Path) -> Iterable[PacketFeature]:
    """Yield IPv4/TCP features from a PCAP file using Scapy."""
    try:
        from scapy.all import IP, TCP, PcapReader
    except ImportError as exc:
        raise RuntimeError(
            "Scapy is required for PCAP/live capture. Install requirements.txt."
        ) from exc

    with PcapReader(str(path)) as reader:
        for packet in reader:
            if IP not in packet or TCP not in packet:
                continue
            yield PacketFeature(
                timestamp=float(packet.time),
                source_ip=packet[IP].src,
                destination_ip=packet[IP].dst,
                destination_port=int(packet[TCP].dport),
                flags=str(packet[TCP].flags),
            )


def capture_live(interface: str, packet_count: int = 0) -> Iterable[PacketFeature]:
    """Capture IPv4/TCP features. Requires root/CAP_NET_RAW in most systems."""
    try:
        from scapy.all import IP, TCP, sniff
    except ImportError as exc:
        raise RuntimeError(
            "Scapy is required for PCAP/live capture. Install requirements.txt."
        ) from exc

    packets = sniff(
        iface=interface,
        filter="ip and tcp",
        count=packet_count,
        store=True,
    )
    for packet in packets:
        if IP in packet and TCP in packet:
            yield PacketFeature(
                timestamp=float(packet.time),
                source_ip=packet[IP].src,
                destination_ip=packet[IP].dst,
                destination_port=int(packet[TCP].dport),
                flags=str(packet[TCP].flags),
            )


def write_alerts(alerts: Iterable[Alert], path: str | Path) -> None:
    rows = [alert.as_dict() for alert in alerts]
    fieldnames = [
        "timestamp",
        "source_ip",
        "destination_ip",
        "unique_ports",
        "connections",
        "syn_ratio",
        "reason",
    ]
    with Path(path).open("w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
