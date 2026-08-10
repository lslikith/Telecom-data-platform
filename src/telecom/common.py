import random
from datetime import datetime, timedelta

import pandas as pd

from telecom.config import CRM_FILE


def load_customers():
    return pd.read_csv(CRM_FILE)


def random_date(start, end):
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))


def random_datetime():
    return random_date(
        datetime(2025, 1, 1),
        datetime(2026, 12, 31)
    )


def generate_id(prefix, number):
    return f"{prefix}{number:06d}"