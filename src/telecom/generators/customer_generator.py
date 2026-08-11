import pandas as pd

from telecom.config import CRM_FILE


def analyze_customer_data():

    df = pd.read_csv(CRM_FILE)

    print(df.head())


if __name__ == "__main__":
    analyze_customer_data()