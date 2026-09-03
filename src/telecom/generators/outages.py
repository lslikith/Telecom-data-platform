from datetime import datetime, timedelta
import random
import pandas as pd

from telecom.config import OUTAGES_DIR, TOTAL_TOWERS


def generate_outages(outage_count: int = 250):
    reasons = [
        "Fiber Cut",
        "Commercial Power Outage",
        "Hardware Component Failure",
        "Scheduled Firmware Maintenance",
        "Severe Weather / Heavy Rain",
        "Backhaul Link Degraded",
    ]
    severities = ["Minor", "Major", "Critical"]

    start_date = datetime(2026, 1, 1)
    end_date = datetime(2026, 8, 31)
    total_days = (end_date - start_date).days

    records = []
    for i in range(1, outage_count + 1):
        tower_idx = random.randint(1, TOTAL_TOWERS)
        outage_start = start_date + timedelta(
            days=random.randint(0, total_days),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )
        duration_min = random.choice([15, 30, 45, 60, 90, 120, 180, 240, 360])
        outage_end = outage_start + timedelta(minutes=duration_min)
        severity = random.choices(severities, weights=[0.55, 0.35, 0.10], k=1)[0]
        impacted_users = random.randint(200, 3500)

        records.append({
            "outage_id": f"OTG{i:05d}",
            "tower_id": f"TWR{tower_idx:05d}",
            "outage_start": outage_start.strftime("%Y-%m-%d %H:%M:%S"),
            "outage_end": outage_end.strftime("%Y-%m-%d %H:%M:%S"),
            "duration_minutes": duration_min,
            "severity": severity,
            "cause": random.choice(reasons),
            "estimated_impacted_users": impacted_users,
        })

    df = pd.DataFrame(records)
    OUTAGES_DIR.mkdir(parents=True, exist_ok=True)
    output_file = OUTAGES_DIR / "tower_outages.csv"
    df.to_csv(output_file, index=False)

    print("=" * 60)
    print("CELL TOWER NETWORK OUTAGES GENERATED")
    print("=" * 60)
    print(f"Total Outage Incidents: {len(df)}")
    print(f"Saved To              : {output_file}")
    return df


if __name__ == "__main__":
    generate_outages()
