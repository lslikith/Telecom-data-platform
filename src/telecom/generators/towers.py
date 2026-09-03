from datetime import datetime, timedelta
import random
import pandas as pd

from telecom.config import TOTAL_TOWERS, TOWERS_DIR

# Cities for Cell Towers
locations = [
    ("Bengaluru", "Karnataka", 12.9716, 77.5946),
    ("Hyderabad", "Telangana", 17.3850, 78.4867),
    ("Chennai", "Tamil Nadu", 13.0827, 80.2707),
    ("Mumbai", "Maharashtra", 19.0760, 72.8777),
    ("Delhi", "Delhi", 28.7041, 77.1025),
    ("Pune", "Maharashtra", 18.5204, 73.8567),
    ("Kolkata", "West Bengal", 22.5726, 88.3639),
    ("Ahmedabad", "Gujarat", 23.0225, 72.5714),
    ("Jaipur", "Rajasthan", 26.9124, 75.7873),
    ("Lucknow", "Uttar Pradesh", 26.8467, 80.9462),
]

vendors = ["Ericsson", "Nokia", "Samsung Networks", "Huawei", "Cisco"]
technologies = ["4G", "5G"]
statuses = ["Active", "Active", "Active", "Maintenance", "Degraded"]


def generate_towers():
    records = []
    for i in range(1, TOTAL_TOWERS + 1):
        city, state, lat, lon = random.choice(locations)
        install_date = datetime.today() - timedelta(days=random.randint(200, 2000))
        records.append({
            "tower_id": f"TWR{i:05d}",
            "tower_name": f"{city[:3].upper()}-TWR-{i:04d}",
            "city": city,
            "state": state,
            "latitude": round(lat + random.uniform(-0.04, 0.04), 6),
            "longitude": round(lon + random.uniform(-0.04, 0.04), 6),
            "technology": random.choice(technologies),
            "vendor": random.choice(vendors),
            "capacity": random.randint(1500, 5000),
            "installation_date": install_date.strftime("%Y-%m-%d"),
            "status": random.choice(statuses),
        })

    df = pd.DataFrame(records)
    TOWERS_DIR.mkdir(parents=True, exist_ok=True)
    output_file = TOWERS_DIR / "towers.csv"
    df.to_csv(output_file, index=False)

    print("=" * 60)
    print("CELL TOWERS DATASET GENERATED")
    print("=" * 60)
    print(f"Total Towers: {len(df)}")
    print(f"Saved To    : {output_file}")
    return df


if __name__ == "__main__":
    generate_towers()