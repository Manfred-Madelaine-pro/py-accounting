INSERT INTO payments (account_id,amount,direction,label,value_date,creation_date) VALUES (
	?,
	?,
	?,
	?,
	?,
	DATETIME('now')
);