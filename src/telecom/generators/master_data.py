import pandas as pd
from telecom.config import MASTER_DIR


def generate_vendors():
    vendors = [
        {"vendor_id": "V001", "vendor_name": "Ericsson", "country": "Sweden"},
        {"vendor_id": "V002", "vendor_name": "Nokia", "country": "Finland"},
        {"vendor_id": "V003", "vendor_name": "Samsung Networks", "country": "South Korea"},
        {"vendor_id": "V004", "vendor_name": "Huawei", "country": "China"},
        {"vendor_id": "V005", "vendor_name": "Cisco", "country": "USA"},
    ]
    df = pd.DataFrame(vendors)
    output_path = MASTER_DIR / "vendors.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Vendor Master Generated: {len(df)} records -> {output_path}")
    return df


def generate_cities():
    cities = [
        {"city_id": "CT001", "city": "Bengaluru", "state": "Karnataka", "telecom_circle": "Karnataka", "latitude": 12.9716, "longitude": 77.5946},
        {"city_id": "CT002", "city": "Mysuru", "state": "Karnataka", "telecom_circle": "Karnataka", "latitude": 12.2958, "longitude": 76.6394},
        {"city_id": "CT003", "city": "Hyderabad", "state": "Telangana", "telecom_circle": "Andhra Pradesh & Telangana", "latitude": 17.3850, "longitude": 78.4867},
        {"city_id": "CT004", "city": "Chennai", "state": "Tamil Nadu", "telecom_circle": "Tamil Nadu", "latitude": 13.0827, "longitude": 80.2707},
        {"city_id": "CT005", "city": "Mumbai", "state": "Maharashtra", "telecom_circle": "Mumbai", "latitude": 19.0760, "longitude": 72.8777},
        {"city_id": "CT006", "city": "Pune", "state": "Maharashtra", "telecom_circle": "Maharashtra & Goa", "latitude": 18.5204, "longitude": 73.8567},
        {"city_id": "CT007", "city": "Delhi", "state": "Delhi", "telecom_circle": "Delhi NCR", "latitude": 28.7041, "longitude": 77.1025},
        {"city_id": "CT008", "city": "Kolkata", "state": "West Bengal", "telecom_circle": "Kolkata", "latitude": 22.5726, "longitude": 88.3639},
        {"city_id": "CT009", "city": "Ahmedabad", "state": "Gujarat", "telecom_circle": "Gujarat", "latitude": 23.0225, "longitude": 72.5714},
        {"city_id": "CT010", "city": "Jaipur", "state": "Rajasthan", "telecom_circle": "Rajasthan", "latitude": 26.9124, "longitude": 75.7873},
    ]
    df = pd.DataFrame(cities)
    output_path = MASTER_DIR / "cities.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Cities Master Generated: {len(df)} records -> {output_path}")
    return df


def generate_telecom_circles():
    circles = [
        {"circle_id": "CIR01", "circle_name": "Karnataka", "category": "Metro", "headquarters": "Bengaluru"},
        {"circle_id": "CIR02", "circle_name": "Mumbai", "category": "Metro", "headquarters": "Mumbai"},
        {"circle_id": "CIR03", "circle_name": "Delhi NCR", "category": "Metro", "headquarters": "New Delhi"},
        {"circle_id": "CIR04", "circle_name": "Kolkata", "category": "Metro", "headquarters": "Kolkata"},
        {"circle_id": "CIR05", "circle_name": "Tamil Nadu", "category": "Circle A", "headquarters": "Chennai"},
        {"circle_id": "CIR06", "circle_name": "Maharashtra & Goa", "category": "Circle A", "headquarters": "Pune"},
        {"circle_id": "CIR07", "circle_name": "Andhra Pradesh & Telangana", "category": "Circle A", "headquarters": "Hyderabad"},
        {"circle_id": "CIR08", "circle_name": "Gujarat", "category": "Circle A", "headquarters": "Ahmedabad"},
        {"circle_id": "CIR09", "circle_name": "Rajasthan", "category": "Circle B", "headquarters": "Jaipur"},
    ]
    df = pd.DataFrame(circles)
    output_path = MASTER_DIR / "telecom_circles.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Telecom Circles Master Generated: {len(df)} records -> {output_path}")
    return df


def generate_plans():
    plans = [
        {"plan_id": "P001", "plan_name": "Basic 299", "monthly_price": 299.00, "validity_days": 28, "data_limit_gb": 30, "voice_minutes": "Unlimited", "sms_limit": 100, "network_type": "4G", "plan_category": "Prepaid"},
        {"plan_id": "P002", "plan_name": "Premium 499", "monthly_price": 499.00, "validity_days": 28, "data_limit_gb": 75, "voice_minutes": "Unlimited", "sms_limit": 100, "network_type": "5G", "plan_category": "Prepaid"},
        {"plan_id": "P003", "plan_name": "Unlimited 799", "monthly_price": 799.00, "validity_days": 30, "data_limit_gb": -1, "voice_minutes": "Unlimited", "sms_limit": -1, "network_type": "5G", "plan_category": "Postpaid"},
        {"plan_id": "P004", "plan_name": "Family 999", "monthly_price": 999.00, "validity_days": 30, "data_limit_gb": -1, "voice_minutes": "Unlimited", "sms_limit": -1, "network_type": "5G", "plan_category": "Postpaid"},
        {"plan_id": "P005", "plan_name": "Business 1499", "monthly_price": 1499.00, "validity_days": 30, "data_limit_gb": -1, "voice_minutes": "Unlimited", "sms_limit": -1, "network_type": "5G", "plan_category": "Postpaid"},
        {"plan_id": "P006", "plan_name": "Fiber Starter 599", "monthly_price": 599.00, "validity_days": 30, "data_limit_gb": 3300, "voice_minutes": "Unlimited", "sms_limit": 0, "network_type": "Fiber", "plan_category": "Broadband"},
        {"plan_id": "P007", "plan_name": "Fiber Gigafast 1499", "monthly_price": 1499.00, "validity_days": 30, "data_limit_gb": 3300, "voice_minutes": "Unlimited", "sms_limit": 0, "network_type": "Fiber", "plan_category": "Broadband"},
    ]
    df = pd.DataFrame(plans)
    output_path = MASTER_DIR / "telecom_plans.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Plans Master Generated: {len(df)} records -> {output_path}")
    return df


if __name__ == "__main__":
    generate_vendors()
    generate_cities()
    generate_telecom_circles()
    generate_plans()