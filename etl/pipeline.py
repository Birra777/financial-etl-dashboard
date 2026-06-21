import logging
import os

import pandas as pd

# 1. Define clean paths (no more ../ confusion)
RAW_DIR = "data/raw"
PROC_DIR = "data/processed"
LOG_FILE = os.path.join(PROC_DIR, "validation_report.log")

# 2. Create the processed folder BEFORE setting up the logger
os.makedirs(PROC_DIR, exist_ok=True)

# 3. Now setup logging safely
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.WARNING,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def extract():
    """Read all CSVs from raw folder and add a source system tag."""
    df_list = []
    for file in os.listdir(RAW_DIR):
        if file.endswith(".csv"):
            df = pd.read_csv(os.path.join(RAW_DIR, file))
            df["source_system"] = file.split("_")[0]
            df_list.append(df)
    return pd.concat(df_list, ignore_index=True)


def transform(df):
    """Clean, standardize, and deduplicate."""
    # 1. Standardize column names
    df.columns = df.columns.str.lower().str.strip()

    # 2. Convert Dates (Coerce invalid dates to NaT)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # 3. Deduplicate based on transaction_id
    original_len = len(df)
    df = df.drop_duplicates(subset=["transaction_id"], keep="first")
    logging.warning(f"Deduplication: Removed {original_len - len(df)} duplicate rows.")

    return df


def validate_and_load(df):
    """Validate data rules, log issues, drop invalid rows, and save."""
    original_len = len(df)

    # Rule 1: Required fields cannot be null
    required_fields = ["transaction_id", "date", "amount", "customer_id"]
    for field in required_fields:
        null_count = df[field].isna().sum()
        if null_count > 0:
            logging.warning(f"Validation: Found {null_count} NULL values in '{field}'.")

    # Drop rows missing required fields
    df = df.dropna(subset=required_fields)

    # Rule 2: Amount must be > 0
    invalid_amounts = df[df["amount"] <= 0]
    if not invalid_amounts.empty:
        logging.warning(
            f"Validation: Found {len(invalid_amounts)} rows with invalid amounts (<= 0). Transaction IDs: {invalid_amounts['transaction_id'].tolist()[:5]}..."
        )
        df = df[df["amount"] > 0]

    logging.warning(
        f"Validation Complete: Dropped {original_len - len(df)} invalid rows out of {original_len}."
    )

    # Load to Parquet
    df.to_parquet(os.path.join(PROC_DIR, "transactions_clean.parquet"), index=False)
    print(f"ETL Complete. Clean data saved to parquet. Final row count: {len(df)}")


if __name__ == "__main__":
    raw_df = extract()
    clean_df = transform(raw_df)
    validate_and_load(clean_df)
