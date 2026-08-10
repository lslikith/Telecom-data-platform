from datetime import datetime, timedelta
import random

import pandas as pd

from telecom.config.settings import (
    TOTAL_TOWERS,
    TOWERS_DIR
)

# --------------------------------------------------
# Cities
# --------------------------------------------------

locations = [

    ("Bengaluru","Karnataka",12.9716,77.5946),
    ("Hyderabad","Telangana",17.3850,78.4867),
    ("Chennai","Tamil Nadu",13.0827,80.2707),
    ("Mumbai","Maharashtra",19.0760,72.8777),
    ("Delhi","Delhi",28.7041,77.1025),
    ("Pune","Maharashtra",18.5204,73.8567),
    ("Kolkata","West Bengal",22.5726,88.3639),
    ("Ahmedabad","Gujarat",23.0225,72.5714),
    ("Jaipur","Rajasthan",26.9124,75.7873),
    ("Lucknow","Uttar Pradesh",26.8467,80.9462)

]

vendors = [
    "Ericsson",
    "Nokia",
    "Samsung",
    "Huawei"
]

technology = [
    "4G",
    "5G"
]

status = [
    "Active",
    "Maintenance"
]

records = []

for i in range(1, TOTAL_TOWERS + 1):

    city, state, lat, lon = random.choice(locations)

    install_date = datetime.today() - timedelta(
        days=random.randint(300, 2500)
    )

    records.append({

        "tower_id": f"T{i:06d}",

        "tower_name": f"{city[:3].upper()}-TWR-{i:03d}",

        "city": city,

        "state": state,

        "latitude": round(lat + random.uniform(-0.03,0.03),6),

        "longitude": round(lon + random.uniform(-0.03,0.03),6),

        "technology": random.choice(technology),

        "vendor": random.choice(vendors),

        "capacity": random.randint(1500,3500),

        "installation_date": install_date.date(),

        "status": random.choice(status)

    })

df = pd.DataFrame(records)

TOWERS_DIR.mkdir(
    parents=True,
    exist_ok=True
)

output_file = TOWERS_DIR / "towers.csv"

df.to_csv(
    output_file,
    index=False
)

print("="*60)

print("Tower Dataset Generated")

print("="*60)

print(df.head())

print()

print(f"Total Towers : {len(df)}")

print(f"Saved To : {output_file}")