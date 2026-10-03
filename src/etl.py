import os
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

engine = create_engine(URL.create(
    "postgresql+psycopg2",
    username="postgres",
    password=os.environ["DB_PASSWORD"],
    host="localhost",
    port=5432,
    database="loan_etl",
))

def extract():
    return pd.read_csv("data/loans_raw.csv", parse_dates=["application_date"])

def transform(df):
    df = df.drop_duplicates(subset="loan_id")
    df = df[df["loan_amount"] > 0].copy()
    df["customer_name"] = df["customer_name"].str.strip()
    df["status"] = df["status"].str.strip().str.title().fillna("Unknown")
    return df

def load(raw, clean):
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE staging_loans, loans"))   # makes reruns safe
    raw.to_sql("staging_loans", engine, if_exists="append", index=False)
    clean.to_sql("loans", engine, if_exists="append", index=False)

def run_quality_checks():
    checks = {
        "duplicate loan_ids": "SELECT COUNT(*) FROM (SELECT loan_id FROM loans GROUP BY loan_id HAVING COUNT(*) > 1) d",
        "null values": "SELECT COUNT(*) FROM loans WHERE status IS NULL OR customer_name IS NULL",
        "invalid amounts": "SELECT COUNT(*) FROM loans WHERE loan_amount <= 0",
        "row mismatch (source valid vs target)": """
            SELECT ABS(
              (SELECT COUNT(DISTINCT loan_id) FROM staging_loans WHERE loan_amount > 0)
              - (SELECT COUNT(*) FROM loans))""",
    }
    failed = False
    with engine.connect() as conn:
        for name, sql in checks.items():
            result = conn.execute(text(sql)).scalar()
            print(f"{'PASS' if result == 0 else 'FAIL'} | {name}: {result}")
            failed |= result != 0
    return not failed

if __name__ == "__main__":
    raw = extract()
    clean = transform(raw)
    print(f"Extracted {len(raw)} rows, {len(clean)} after cleaning")
    load(raw, clean)
    if not run_quality_checks():
        raise SystemExit("Data quality checks failed")
    print("Pipeline completed successfully")