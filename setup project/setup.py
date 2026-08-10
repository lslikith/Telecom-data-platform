from pathlib import Path

# Project Root
ROOT = Path(".")

# Folders to create
folders = [
    "datasets/generated/billing",
    "datasets/generated/outages",
    "datasets/generated/payments",
    "datasets/generated/plans",
    "datasets/generated/support",
    "datasets/generated/towers",
    "datasets/generated/usage",
]

print("=" * 60)
print("Creating Project Folder Structure")
print("=" * 60)

for folder in folders:
    path = ROOT / folder
    path.mkdir(parents=True, exist_ok=True)
    print(f"Created: {path}")

print("\nAll folders created successfully.")