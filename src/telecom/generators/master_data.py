import pandas as pd

from telecom.config import MASTER_DIR


def generate_vendors():

    vendors = [

        {
            "vendor_id": "V001",
            "vendor_name": "Ericsson",
            "country": "Sweden"
        },

        {
            "vendor_id": "V002",
            "vendor_name": "Nokia",
            "country": "Finland"
        },

        {
            "vendor_id": "V003",
            "vendor_name": "Samsung Networks",
            "country": "South Korea"
        },

        {
            "vendor_id": "V004",
            "vendor_name": "Huawei",
            "country": "China"
        },

        {
            "vendor_id": "V005",
            "vendor_name": "Cisco",
            "country": "USA"
        }

    ]

    # Convert List -> DataFrame
    df = pd.DataFrame(vendors)

    # Save DataFrame -> CSV
    output_path = MASTER_DIR / "vendors.csv"

    df.to_csv(
        output_path,
        index=False
    )

    print("=" * 50)
    print("Vendor Master Generated Successfully")
    print("=" * 50)
    print(df)

    print(f"\nFile saved to:\n{output_path}")


def generate_cities():

    cities = [

        {
            "city_id": "CT001",
            "city": "Bengaluru",
            "state": "Karnataka",
            "telecom_circle": "South",
            "latitude": 12.9716,
            "longitude": 77.5946
        },

        {
            "city_id": "CT002",
            "city": "Mysuru",
            "state": "Karnataka",
            "telecom_circle": "South",
            "latitude": 12.2958,
            "longitude": 76.6394
        },

        {
            "city_id": "CT003",
            "city": "Hyderabad",
            "state": "Telangana",
            "telecom_circle": "South",
            "latitude": 17.3850,
            "longitude": 78.4867
        }

    ]

    df = pd.DataFrame(cities)

    output_path = MASTER_DIR / "cities.csv"

    df.to_csv(
        output_path,
        index=False
    )

    print("\nCities Generated Successfully\n")
    print(df)

if __name__ == "__main__":
    generate_vendors()
    generate_cities()