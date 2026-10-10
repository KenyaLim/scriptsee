import unittest

from portscan_detector import (
    DetectionConfig,
    PacketFeature,
    PortScanDetector,
)


class PortScanDetectorTests(unittest.TestCase):
    def test_alerts_when_unique_ports_exceed_threshold(self) -> None:
        detector = PortScanDetector(
            DetectionConfig(
                window_seconds=10,
                ttl_seconds=30,
                unique_ports_threshold=3,
                connections_threshold=99,
                syn_ratio_threshold=1.1,
            )
        )
        packets = [
            PacketFeature(float(index), "10.0.0.2", "10.0.0.3", 80 + index, "S")
            for index in range(3)
        ]
        alerts = detector.process_many(packets)
        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0].unique_ports, 3)

    def test_old_events_leave_sliding_window(self) -> None:
        detector = PortScanDetector(
            DetectionConfig(
                window_seconds=5,
                ttl_seconds=10,
                unique_ports_threshold=3,
                connections_threshold=99,
                syn_ratio_threshold=1.1,
            )
        )
        for index in range(2):
            detector.process(
                PacketFeature(float(index), "10.0.0.2", "10.0.0.3", 80 + index, "S")
            )
        alert = detector.process(
            PacketFeature(6.0, "10.0.0.2", "10.0.0.3", 82, "S")
        )
        self.assertIsNone(alert)

    def test_expired_state_is_removed(self) -> None:
        detector = PortScanDetector(
            DetectionConfig(window_seconds=5, ttl_seconds=10)
        )
        detector.process(PacketFeature(1.0, "10.0.0.2", "10.0.0.3", 80, "S"))
        self.assertEqual(detector.state_count, 1)
        detector.expire(12.0)
        self.assertEqual(detector.state_count, 0)

    def test_invalid_ttl_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            PortScanDetector(DetectionConfig(window_seconds=10, ttl_seconds=5))


if __name__ == "__main__":
    unittest.main()
