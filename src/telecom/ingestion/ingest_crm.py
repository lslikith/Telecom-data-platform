import shutil
from datetime import datetime

from telecom.config import CRM_FILE, RAW_DIR


def ingest_crm():

    # Create destination folder if it doesn't exist
    destination_folder = RAW_DIR / "crm"
    destination_folder.mkdir(parents=True, exist_ok=True)

    # Generate timestamped filename
    today = datetime.now().strftime("%Y%m%d")

    destination_file = (
        destination_folder /
        f"customer_churn_{today}.csv"
    )

    # Copy source file to RAW layer
    shutil.copy2(CRM_FILE, destination_file)

    print("=" * 60)
    print("CRM INGESTION SUCCESSFUL")
    print("=" * 60)
    print(f"Source      : {CRM_FILE}")
    print(f"Destination : {destination_file}")


if __name__ == "__main__":
    ingest_crm()