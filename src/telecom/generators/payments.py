from datetime import datetime, timedelta
import random
import pandas as pd

from telecom.config import BILLING_DIR, PAYMENTS_DIR


def generate_payments():
    billing_file = BILLING_DIR / "customer_billing.csv"
    if not billing_file.exists():
        from telecom.generators.billing import generate_billing
        df_bills = generate_billing()
    else:
        df_bills = pd.read_csv(billing_file)

    payment_methods = [
        "UPI",
        "Credit Card",
        "Debit Card",
        "Net Banking",
        "Electronic check",
        "Mailed check",
        "Bank transfer (automatic)",
    ]

    gateways = ["Razorpay", "PhonePe", "Paytm", "BillDesk", "Stripe"]

    payment_records = []
    pmt_seq = 1

    for _, bill in df_bills.iterrows():
        # Only paid or attempted bills generate payments
        if bill["payment_status"] in ["Paid", "Overdue"]:
            bill_date = datetime.strptime(bill["bill_date"], "%Y-%m-%d")
            # Payment occurred within 1 to 14 days of bill date
            payment_date = bill_date + timedelta(
                days=random.randint(1, 14),
                hours=random.randint(8, 22),
                minutes=random.randint(0, 59)
            )

            status = "SUCCESS" if bill["payment_status"] == "Paid" else "FAILED"
            # small chance of failure even if paid initially
            if random.random() < 0.03 and status == "SUCCESS":
                status = "FAILED"

            payment_records.append({
                "payment_id": f"PMT{pmt_seq:07d}",
                "bill_id": bill["bill_id"],
                "customer_id": bill["customer_id"],
                "payment_datetime": payment_date.strftime("%Y-%m-%d %H:%M:%S"),
                "amount": bill["total_amount"],
                "payment_method": random.choice(payment_methods),
                "payment_gateway": random.choice(gateways),
                "transaction_status": status,
                "transaction_ref": f"TXN{random.randint(100000000, 999999999)}",
            })
            pmt_seq += 1

    df = pd.DataFrame(payment_records)
    PAYMENTS_DIR.mkdir(parents=True, exist_ok=True)
    output_file = PAYMENTS_DIR / "customer_payments.csv"
    df.to_csv(output_file, index=False)

    print("=" * 60)
    print("CUSTOMER PAYMENTS DATASET GENERATED")
    print("=" * 60)
    print(f"Total Payments Generated: {len(df)}")
    print(f"Saved To                : {output_file}")
    return df


if __name__ == "__main__":
    generate_payments()
