import time
from datetime import datetime

from telecom.generators.billing import generate_billing
from telecom.generators.master_data import (
    generate_cities,
    generate_plans,
    generate_telecom_circles,
    generate_vendors,
)
from telecom.generators.outages import generate_outages
from telecom.generators.payments import generate_payments
from telecom.generators.plans import PlanGenerator
from telecom.generators.support import generate_support_tickets
from telecom.generators.towers import generate_towers
from telecom.generators.usage import generate_usage


def run_all_generators():
    start_time = time.time()
    print("=" * 70)
    print("TELECOM DATA PLATFORM - SYNTHETIC DATA GENERATION SUITE")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    # 1. Master Datasets
    print("\n[1/7] Generating Master Datasets (Vendors, Cities, Circles)...")
    generate_vendors()
    generate_cities()
    generate_telecom_circles()
    generate_plans()

    # 2. Plans & Towers
    print("\n[2/7] Generating Plans & Cell Towers...")
    PlanGenerator().generate()
    generate_towers()

    # 3. Billing
    print("\n[3/7] Generating Customer Billing Cycles...")
    generate_billing()

    # 4. Payments
    print("\n[4/7] Generating Customer Payment Transactions...")
    generate_payments()

    # 5. Usage
    print("\n[5/7] Generating High-Resolution Cellular Usage...")
    generate_usage(days_count=7, sample_size=2000)

    # 6. Support Tickets
    print("\n[6/7] Generating Customer Support Tickets...")
    generate_support_tickets(ticket_count=3500)

    # 7. Outages
    print("\n[7/7] Generating Network Tower Outages...")
    generate_outages(outage_count=250)

    elapsed = round(time.time() - start_time, 2)
    print("\n" + "=" * 70)
    print(f"ALL DATASETS GENERATED SUCCESSFULLY IN {elapsed} SECONDS!")
    print("=" * 70)


if __name__ == "__main__":
    run_all_generators()
