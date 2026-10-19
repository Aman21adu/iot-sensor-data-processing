"""Small CSV -> clean -> NumPy analytics app for AASTU AI/ML Week 1."""

import argparse
import csv
from collections import Counter
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

REQUIRED_COLUMNS = ("timestamp", "sensor_id", "temperature_c", "humidity_pct")
# Demo validation rules; change them if your real sensor has other valid limits.
MIN_TEMP_C, MAX_TEMP_C = -20.0, 60.0
HOT_THRESHOLD_C = 30.0
HIGH_HUMIDITY_PCT = 70.0


def load_csv(path):
    """Read rows from a CSV file into a list of dictionaries."""
    with open(path, newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        if not reader.fieldnames or not set(REQUIRED_COLUMNS).issubset(reader.fieldnames):
            raise ValueError(f"CSV must contain these columns: {', '.join(REQUIRED_COLUMNS)}")
        return list(reader)


def clean_data(raw_rows):
    """Normalize rows, remove duplicate readings, and reject invalid values."""
    cleaned = []
    rejected = Counter()
    seen_readings = set()

    for row in raw_rows:
        sensor_id = (row.get("sensor_id") or "").strip().upper()
        time_text = (row.get("timestamp") or "").strip()
        if not sensor_id or not time_text:
            rejected["missing sensor ID or timestamp"] += 1
            continue

        try:
            timestamp = datetime.fromisoformat(time_text).isoformat(timespec="seconds")
        except ValueError:
            rejected["invalid timestamp"] += 1
            continue

        try:
            temperature = float((row.get("temperature_c") or "").strip())
            humidity = float((row.get("humidity_pct") or "").strip())
        except (TypeError, ValueError):
            rejected["missing or nonnumeric measurement"] += 1
            continue

        if not np.isfinite(temperature) or not np.isfinite(humidity):
            rejected["non-finite measurement"] += 1
            continue
        if not (MIN_TEMP_C <= temperature <= MAX_TEMP_C and 0 <= humidity <= 100):
            rejected["out-of-range measurement"] += 1
            continue

        reading_key = (timestamp, sensor_id)
        if reading_key in seen_readings:
            rejected["duplicate sensor and timestamp"] += 1
            continue
        seen_readings.add(reading_key)

        cleaned.append({
            "timestamp": timestamp,
            "sensor_id": sensor_id,
            "temperature_c": temperature,
            "humidity_pct": humidity,
        })

    return sorted(cleaned, key=lambda r: (r["timestamp"], r["sensor_id"])), rejected


def analyze_data(cleaned):
    """Use NumPy for vectorized statistics and high-reading detection."""
    if not cleaned:
        raise ValueError("No valid readings remained after cleaning.")

    temperatures = np.array([r["temperature_c"] for r in cleaned], dtype=float)
    humidity = np.array([r["humidity_pct"] for r in cleaned], dtype=float)
    sensors = np.array([r["sensor_id"] for r in cleaned])
    alerts = (temperatures >= HOT_THRESHOLD_C) | (humidity >= HIGH_HUMIDITY_PCT)

    overall = {
        "valid_readings": len(cleaned),
        "average_temperature_c": float(np.mean(temperatures)),
        "min_temperature_c": float(np.min(temperatures)),
        "max_temperature_c": float(np.max(temperatures)),
        "average_humidity_pct": float(np.mean(humidity)),
        "alert_readings": int(np.sum(alerts)),
    }

    per_sensor = []
    for sensor_id in np.unique(sensors):
        mask = sensors == sensor_id  # Boolean indexing: select one sensor.
        per_sensor.append({
            "sensor_id": str(sensor_id),
            "readings": int(np.sum(mask)),
            "avg_temperature_c": round(float(np.mean(temperatures[mask])), 2),
            "avg_humidity_pct": round(float(np.mean(humidity[mask])), 2),
            "alert_readings": int(np.sum(alerts[mask])),
        })
    return overall, per_sensor


def write_csv(path, rows, columns):
    """Save a CSV report with a header, creating its folder if necessary."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def plot_temperatures(cleaned, path):
    """Save a temperature trend chart for each sensor."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(9, 4.5))
    for sensor_id in sorted({row["sensor_id"] for row in cleaned}):
        records = [r for r in cleaned if r["sensor_id"] == sensor_id]
        xs = [datetime.fromisoformat(r["timestamp"]) for r in records]
        ys = [r["temperature_c"] for r in records]
        ax.plot(xs, ys, marker="o", linewidth=1.5, label=sensor_id)
    ax.axhline(HOT_THRESHOLD_C, linestyle="--", linewidth=1.2, label="Hot threshold (30°C)")
    ax.set_title("Temperature Trend by Sensor (Synthetic Sample Data)")
    ax.set_ylabel("Temperature (°C)")
    ax.set_xlabel("Time")
    ax.legend(ncol=2)
    ax.grid(alpha=0.25)
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def main():
    root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description="Clean and analyze a sample IoT sensor CSV.")
    parser.add_argument("--input", type=Path, default=root / "data" / "raw_sensor_readings.csv")
    parser.add_argument("--output", type=Path, default=root / "outputs")
    args = parser.parse_args()

    raw_rows = load_csv(args.input)
    cleaned, rejected = clean_data(raw_rows)
    overall, summary = analyze_data(cleaned)
    args.output.mkdir(parents=True, exist_ok=True)
    write_csv(args.output / "cleaned_sensor_readings.csv", cleaned, REQUIRED_COLUMNS)
    write_csv(args.output / "sensor_summary.csv", summary, (
        "sensor_id", "readings", "avg_temperature_c", "avg_humidity_pct", "alert_readings"
    ))
    plot_temperatures(cleaned, args.output / "temperature_trend.png")

    print("IoT SENSOR DATA PROCESSOR")
    print(f"Raw: {len(raw_rows)} | Clean: {len(cleaned)} | Rejected: {sum(rejected.values())}")
    for reason, count in sorted(rejected.items()):
        print(f"  Rejected - {reason}: {count}")
    print(f"Overall average temperature: {overall['average_temperature_c']:.2f} °C")
    print(f"Overall average humidity: {overall['average_humidity_pct']:.2f}%")
    print(f"Readings meeting alert conditions: {overall['alert_readings']}")
    for row in summary:
        print(f"  {row['sensor_id']}: {row['readings']} readings, "
              f"{row['avg_temperature_c']:.2f} °C avg, "
              f"{row['alert_readings']} alerts")
    print(f"Reports and chart saved to: {args.output.resolve()}")


if __name__ == "__main__":
    main()
