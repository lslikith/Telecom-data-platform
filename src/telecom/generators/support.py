from datetime import datetime, timedelta
import random
import pandas as pd

from telecom.common import load_customers
from telecom.config import SUPPORT_DIR


def generate_support_tickets(ticket_count: int = 3500):
    df_customers = load_customers()
    customer_ids = df_customers["customerID"].dropna().unique().tolist()
    # Note: Customers who churn often have higher support ticket frequency
    churned_cids = set(df_customers[df_customers["Churn"] == "Yes"]["customerID"].tolist())

    categories = [
        "Network Slowdown",
        "Billing Dispute",
        "Call Drops",
        "SIM Issue",
        "Plan Modification",
        "Broadband Outage",
        "Roaming Issue",
    ]

    priorities = ["Low", "Medium", "High", "Critical"]
    channels = ["Mobile App", "Call Center", "Web Portal", "Chatbot", "Retail Store"]
    statuses = ["Resolved", "Closed", "Closed", "In Progress", "Escalated"]

    start_date = datetime(2026, 1, 1)
    end_date = datetime(2026, 8, 31)
    delta_days = (end_date - start_date).days

    records = []
    for i in range(1, ticket_count + 1):
        # 40% chance of ticket coming from churned cohort
        if random.random() < 0.40 and churned_cids:
            cid = random.choice(list(churned_cids))
        else:
            cid = random.choice(customer_ids)

        created_dt = start_date + timedelta(
            days=random.randint(0, delta_days),
            hours=random.randint(7, 23),
            minutes=random.randint(0, 59)
        )

        status = random.choice(statuses)
        resolution_hours = round(random.uniform(0.5, 72.0), 1)
        resolved_dt = created_dt + timedelta(hours=resolution_hours) if status in ["Resolved", "Closed"] else None

        # Satisfaction score: lower for churned/billing disputes
        if cid in churned_cids or random.random() < 0.25:
            csat = random.choice([1, 2, 3])
        else:
            csat = random.choice([3, 4, 5])

        records.append({
            "ticket_id": f"TKT{i:06d}",
            "customer_id": cid,
            "category": random.choice(categories),
            "priority": random.choice(priorities),
            "channel": random.choice(channels),
            "created_at": created_dt.strftime("%Y-%m-%d %H:%M:%S"),
            "resolved_at": resolved_dt.strftime("%Y-%m-%d %H:%M:%S") if resolved_dt else None,
            "resolution_time_hours": resolution_hours if resolved_dt else None,
            "status": status,
            "satisfaction_score": csat if resolved_dt else None,
        })

    df = pd.DataFrame(records)
    SUPPORT_DIR.mkdir(parents=True, exist_ok=True)
    output_file = SUPPORT_DIR / "support_tickets.csv"
    df.to_csv(output_file, index=False)

    print("=" * 60)
    print("CUSTOMER SUPPORT TICKETS DATASET GENERATED")
    print("=" * 60)
    print(f"Total Support Tickets: {len(df)}")
    print(f"Saved To             : {output_file}")
    return df


if __name__ == "__main__":
    generate_support_tickets()
