from datetime import datetime, timedelta
import random
import pandas as pd

from telecom.common import load_customers
from telecom.config import TOTAL_TOWERS, USAGE_DIR


def generate_usage(days_count: int = 7, sample_size: int = 2000):
    df_customers = load_customers()
    all_cids = df_customers["customerID"].dropna().unique().tolist()
    # sample a representative cohort of customers for high-resolution usage tracking
    sampled_cids = random.sample(all_cids, min(sample_size, len(all_cids)))

    end_date = datetime(2026, 8, 31)
    dates = [end_date - timedelta(days=d) for d in range(days_count)]

    usage_records = []
    usg_seq = 1

    for dt in dates:
        dt_str = dt.strftime("%Y-%m-%d")
        for cid in sampled_cids:
            # 85% chance of daily activity
            if random.random() < 0.85:
                tower_idx = random.randint(1, TOTAL_TOWERS)
                data_mb = round(random.uniform(50, 4500), 2)
                voice_min = random.randint(0, 180)
                sms = random.randint(0, 25)
                is_roaming = random.random() < 0.12

                usage_records.append({
                    "usage_id": f"USG{usg_seq:08d}",
                    "customer_id": cid,
                    "usage_date": dt_str,
                    "tower_id": f"TWR{tower_idx:05d}",
                    "voice_minutes": voice_min,
                    "data_usage_mb": data_mb,
                    "data_usage_gb": round(data_mb / 1024.0, 3),
                    "sms_count": sms,
                    "is_roaming": is_roaming,
                })
                usg_seq += 1

    df = pd.DataFrame(usage_records)
    USAGE_DIR.mkdir(parents=True, exist_ok=True)
    output_file = USAGE_DIR / "daily_usage.csv"
    df.to_csv(output_file, index=False)

    print("=" * 60)
    print("DAILY CELLULAR USAGE DATASET GENERATED")
    print("=" * 60)
    print(f"Total Usage Events: {len(df)}")
    print(f"Saved To          : {output_file}")
    return df


if __name__ == "__main__":
    generate_usage()
