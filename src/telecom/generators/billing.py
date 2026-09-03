from datetime import datetime, timedelta
import random
import pandas as pd

from telecom.common import load_customers
from telecom.config import BILLING_DIR


def generate_billing():
    df_customers = load_customers()
    customer_ids = df_customers["customerID"].dropna().unique().tolist()

    # Generate 1 to 3 monthly billing cycles for each customer
    months = [
        (datetime(2026, 6, 1), "2026-06"),
        (datetime(2026, 7, 1), "2026-07"),
        (datetime(2026, 8, 1), "2026-08"),
    ]

    billing_records = []
    bill_seq = 1

    # Map customer monthly charges from CRM
    charges_map = dict(zip(df_customers["customerID"], df_customers["MonthlyCharges"]))

    for bill_date, month_str in months:
        for cid in customer_ids:
            base_charge = float(charges_map.get(cid, round(random.uniform(299, 1499), 2)))
            additional = round(random.choice([0.0, 0.0, 0.0, 50.0, 100.0, 150.0]), 2)
            discount = round(random.choice([0.0, 0.0, 25.0, 50.0]), 2)
            subtotal = max(base_charge + additional - discount, 0.0)
            tax = round(subtotal * 0.18, 2)
            total = round(subtotal + tax, 2)

            due_date = bill_date + timedelta(days=15)
            status = random.choices(
                ["Paid", "Pending", "Overdue"],
                weights=[0.88, 0.08, 0.04],
                k=1
            )[0]

            billing_records.append({
                "bill_id": f"BIL{bill_seq:07d}",
                "customer_id": cid,
                "billing_period": month_str,
                "bill_date": bill_date.strftime("%Y-%m-%d"),
                "due_date": due_date.strftime("%Y-%m-%d"),
                "base_amount": base_charge,
                "additional_charges": additional,
                "discount_amount": discount,
                "tax_amount": tax,
                "total_amount": total,
                "payment_status": status,
            })
            bill_seq += 1

    df = pd.DataFrame(billing_records)
    BILLING_DIR.mkdir(parents=True, exist_ok=True)
    output_file = BILLING_DIR / "customer_billing.csv"
    df.to_csv(output_file, index=False)

    print("=" * 60)
    print("CUSTOMER BILLING DATASET GENERATED")
    print("=" * 60)
    print(f"Total Bills Generated: {len(df)}")
    print(f"Saved To             : {output_file}")
    return df


if __name__ == "__main__":
    generate_billing()
