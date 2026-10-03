# Loan ETL Pipeline with Data Quality Checks

## Problem
Raw loan data arrives with duplicates, invalid amounts, and inconsistent status values.
This pipeline cleans it, loads it into PostgreSQL, and verifies the result.

## Flow
CSV → staging_loans (raw) → transform (Pandas) → loans (clean) → SQL quality checks

## Tech
Python, Pandas, SQLAlchemy, PostgreSQL

## How to run
1. `pip install -r requirements.txt`
2. Create a database named `loan_etl` and create the `staging_loans` and `loans` tables
3. `export DB_PASSWORD='your_password'`
4. `python src/generate_data.py`
5. `python src/etl.py`

## Quality checks
- Duplicate loan IDs in the target
- Null values in required columns
- Invalid loan amounts
- Source-vs-target row reconciliation

Table constraints (primary key, CHECK, NOT NULL) prevent bad data; the reconciliation check detects rows lost between source and target.

## Sample output
(add a screenshot of the PASS lines here)