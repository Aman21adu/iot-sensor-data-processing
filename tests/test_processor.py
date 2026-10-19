"""Basic built-in unittest checks; no pytest dependency required."""

import unittest

from src.processor import analyze_data, clean_data


class DataProcessingTests(unittest.TestCase):
    def test_cleaning_rejects_bad_duplicate_and_normalizes_id(self):
        sample = [
            {"timestamp": "2026-10-18T09:00:00", "sensor_id": " room_a ", "temperature_c": "25", "humidity_pct": "50"},
            {"timestamp": "2026-10-18T09:00:00", "sensor_id": "ROOM_A", "temperature_c": "27", "humidity_pct": "52"},
            {"timestamp": "2026-10-18T09:10:00", "sensor_id": "ROOM_B", "temperature_c": "oops", "humidity_pct": "50"},
        ]
        cleaned, rejected = clean_data(sample)
        self.assertEqual(len(cleaned), 1)
        self.assertEqual(cleaned[0]["sensor_id"], "ROOM_A")
        self.assertEqual(rejected["duplicate sensor and timestamp"], 1)
        self.assertEqual(rejected["missing or nonnumeric measurement"], 1)

    def test_numpy_alerts(self):
        samples = [
            {"timestamp": "2026-10-18T09:00:00", "sensor_id": "ROOM_A", "temperature_c": 25.0, "humidity_pct": 50.0},
            {"timestamp": "2026-10-18T09:10:00", "sensor_id": "ROOM_A", "temperature_c": 31.0, "humidity_pct": 50.0},
            {"timestamp": "2026-10-18T09:20:00", "sensor_id": "ROOM_B", "temperature_c": 23.0, "humidity_pct": 75.0},
        ]
        overall, per_sensor = analyze_data(samples)
        self.assertEqual(overall["valid_readings"], 3)
        self.assertEqual(overall["alert_readings"], 2)
        self.assertAlmostEqual(overall["average_temperature_c"], 79 / 3)
        self.assertEqual(sum(s["alert_readings"] for s in per_sensor), 2)

    def test_no_cleaned_data(self):
        with self.assertRaisesRegex(ValueError, "No valid readings"):
            analyze_data([])


if __name__ == "__main__":
    unittest.main()
