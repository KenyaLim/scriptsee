from __future__ import annotations

import argparse
from pathlib import Path

from portscan_detector import (
    DetectionConfig,
    PortScanDetector,
    capture_live,
    read_pcap,
    write_alerts,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Rule-based IPv4/TCP port-scan detector"
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--pcap", type=Path, help="Read packets from a PCAP file")
    source.add_argument("--interface", help="Capture live traffic on this interface")
    parser.add_argument("--output", type=Path, default=Path("alerts.csv"))
    parser.add_argument("--window", type=float, default=10.0)
    parser.add_argument("--ttl", type=float, default=30.0)
    parser.add_argument("--ports-threshold", type=int, default=10)
    parser.add_argument("--connections-threshold", type=int, default=20)
    parser.add_argument("--syn-ratio-threshold", type=float, default=0.70)
    parser.add_argument(
        "--count",
        type=int,
        default=0,
        help="Live packets to capture; 0 means continue until interrupted",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.pcap is not None and not args.pcap.is_file():
        parser.error(
            f"PCAP file tidak ditemukan: {args.pcap}. "
            "Buat rekaman terlebih dahulu dengan tcpdump atau gunakan path "
            "file yang benar."
        )
    config = DetectionConfig(
        window_seconds=args.window,
        ttl_seconds=args.ttl,
        unique_ports_threshold=args.ports_threshold,
        connections_threshold=args.connections_threshold,
        syn_ratio_threshold=args.syn_ratio_threshold,
    )
    detector = PortScanDetector(config)
    packets = (
        read_pcap(args.pcap)
        if args.pcap is not None
        else capture_live(args.interface, args.count)
    )
    alerts = detector.process_many(packets)
    write_alerts(alerts, args.output)
    print(f"Deteksi selesai: {len(alerts)} alert, state tersisa: {detector.state_count}")
    print(f"Alert tersimpan di: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
