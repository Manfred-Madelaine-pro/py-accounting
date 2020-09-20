CREATE VIEW IF NOT EXISTS v_payments AS 
SELECT 
  account_id,
  amount,
  direction,
  CASE
		WHEN direction = 'D' THEN
			-amount
		ELSE
			amount
		END signed_amount,
  label,
  value_date,
  creation_date
FROM payments
ORDER BY value_date