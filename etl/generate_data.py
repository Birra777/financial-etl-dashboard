import os
from datetime import datetime

import numpy as np
import pandas as pd

# Fixed paths to keep everything inside the project folder
RAW_DIR = "data/raw"
os.makedirs(RAW_DIR, exist_ok=True)


def generate_source(source_name, num_records):
    dates = pd.date_range(end=datetime.today(), periods=num_records, freq="H")
    categories = [
        "Groceries",
        "Utilities",
        "Salary",
        "Dining",
        "Transfer",
        "ATM Withdrawal",
    ]

    data = {
        "transaction_id": [
            f"TXN-{source_name[:3].upper()}-{i:05d}" for i in range(1, num_records + 1)
        ],
        "date": dates,
        "amount": np.random.uniform(10, 5000, num_records).round(2),
        "category": np.random.choice(categories, num_records),
        "customer_id": [
            f"CUST-{np.random.randint(1, 500)}" for _ in range(num_records)
        ],
    }
    df = pd.DataFrame(data)

    # Convert dates to strings to simulate a raw CSV (fixes the FutureWarning)
    df["date"] = df["date"].astype(str)

    # --- Inject Dirty Data for ETL to clean ---
    # 1. Add some duplicates
    df = pd.concat([df, df.sample(frac=0.02)])

    # 2. Add missing customer IDs (NULLs)
    null_indices = np.random.choice(df.index, size=int(len(df) * 0.03), replace=False)
    df.loc[null_indices, "customer_id"] = np.nan

    # 3. Add negative amounts (invalid for this specific schema)
    neg_indices = np.random.choice(df.index, size=int(len(df) * 0.01), replace=False)
    df.loc[neg_indices, "amount"] = -df.loc[neg_indices, "amount"]

    # 4. Mess up some dates (string format instead of datetime)
    bad_date_indices = np.random.choice(
        df.index, size=int(len(df) * 0.02), replace=False
    )
    df.loc[bad_date_indices, "date"] = "2023-INVALID-DATE"

    df.to_csv(f"{RAW_DIR}/{source_name.lower()}_transactions.csv", index=False)
    print(f"Generated {len(df)} records for {source_name}.")


if __name__ == "__main__":
    generate_source("Online_Banking", 1500)
    generate_source("Branch_Deposits", 500)
    generate_source("ATM_Network", 800)
