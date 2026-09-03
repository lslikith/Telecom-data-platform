from pathlib import Path
import pandas as pd
from telecom.config import PLANS_DIR


class PlanGenerator:
    """
    Generates the telecom plans dataset in generated/plans.
    """

    def __init__(self):
        self.output_dir = PLANS_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate(self):
        plans = [
            {
                "plan_id": "P001",
                "plan_name": "Basic 299",
                "monthly_price": 299.00,
                "data_limit_gb": 30,
                "network_type": "4G",
                "voice_minutes": 500,
                "sms_limit": 100,
                "validity_days": 28,
                "plan_category": "Prepaid"
            },
            {
                "plan_id": "P002",
                "plan_name": "Premium 499",
                "monthly_price": 499.00,
                "data_limit_gb": 75,
                "network_type": "5G",
                "voice_minutes": 1000,
                "sms_limit": 500,
                "validity_days": 28,
                "plan_category": "Prepaid"
            },
            {
                "plan_id": "P003",
                "plan_name": "Unlimited 799",
                "monthly_price": 799.00,
                "data_limit_gb": -1,
                "network_type": "5G",
                "voice_minutes": -1,
                "sms_limit": -1,
                "validity_days": 30,
                "plan_category": "Postpaid"
            },
            {
                "plan_id": "P004",
                "plan_name": "Family 999",
                "monthly_price": 999.00,
                "data_limit_gb": -1,
                "network_type": "5G",
                "voice_minutes": -1,
                "sms_limit": -1,
                "validity_days": 30,
                "plan_category": "Postpaid"
            },
            {
                "plan_id": "P005",
                "plan_name": "Business 1499",
                "monthly_price": 1499.00,
                "data_limit_gb": -1,
                "network_type": "5G",
                "voice_minutes": -1,
                "sms_limit": -1,
                "validity_days": 30,
                "plan_category": "Postpaid"
            },
            {
                "plan_id": "P006",
                "plan_name": "Fiber Starter 599",
                "monthly_price": 599.00,
                "data_limit_gb": 3300,
                "network_type": "Fiber",
                "voice_minutes": -1,
                "sms_limit": 0,
                "validity_days": 30,
                "plan_category": "Broadband"
            },
            {
                "plan_id": "P007",
                "plan_name": "Fiber Gigafast 1499",
                "monthly_price": 1499.00,
                "data_limit_gb": 3300,
                "network_type": "Fiber",
                "voice_minutes": -1,
                "sms_limit": 0,
                "validity_days": 30,
                "plan_category": "Broadband"
            }
        ]

        df = pd.DataFrame(plans)
        output_file = self.output_dir / "plans.csv"
        df.to_csv(output_file, index=False)

        print("=" * 60)
        print("TELECOM PLANS GENERATED")
        print("=" * 60)
        print(f"Total Plans: {len(df)}")
        print(f"Saved To   : {output_file}")
        return df


if __name__ == "__main__":
    PlanGenerator().generate()