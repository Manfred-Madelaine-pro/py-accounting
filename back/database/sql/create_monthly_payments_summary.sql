CREATE VIEW IF NOT EXISTS monthly_payments_summary AS 
SELECT 
value_date, 
sum(signed_amount) As end_of_day_balance,
sum(case when direction = 'C' Then signed_amount else 0 end) as total_credits,
sum(case when direction = 'C' Then 1 else 0 end) as count_credits,
sum(case when direction = 'D' Then signed_amount else 0 end) as total_debits,
sum(case when direction = 'D' Then 1 else 0 end) as count_debits,
max(signed_amount) max,
min(signed_amount) min

FROM v_payments 
GROUP by value_date