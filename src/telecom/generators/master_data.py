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

def generate_plans():

    
    plans = [

    {
        "plan_id": "P001",
        "plan_name": "Basic 299",
        "monthly_price": 299,
        "validity_days": 28,
        "data_limit_gb": 30,
        "voice_minutes": "Unlimited",
        "sms_limit": 100,
        "network_type": "4G",
        "plan_category": "Prepaid"
    },

    {
        "plan_id": "P002",
        "plan_name": "Premium 499",
        "monthly_price": 499,
        "validity_days": 28,
        "data_limit_gb": 75,
        "voice_minutes": "Unlimited",
        "sms_limit": 100,
        "network_type": "5G",
        "plan_category": "Prepaid"
    }
    ]


    df = pd.DataFrame(plans)

    output_path = MASTER_DIR / "telecom_plans.csv"

    df.to_csv(
        output_path,
        index=False
    )

    print("\nPlans Generated Successfully\n")
    print(df)

if __name__ == "__main__":
    generate_vendors()
    generate_cities()
    generate_plans()