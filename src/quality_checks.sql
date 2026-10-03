-- 1. Duplicate loan IDs in target
SELECT loan_id, COUNT(*) FROM loans GROUP BY loan_id HAVING COUNT(*) > 1;

-- 2. Null values in required columns
SELECT COUNT(*) FROM loans WHERE status IS NULL OR customer_name IS NULL;

-- 3. Invalid loan amounts
SELECT COUNT(*) FROM loans WHERE loan_amount <= 0;

-- 4. Row reconciliation: valid distinct source rows vs target rows
SELECT
  (SELECT COUNT(DISTINCT loan_id) FROM staging_loans WHERE loan_amount > 0) AS source_valid,
  (SELECT COUNT(*) FROM loans) AS target_rows;