CREATE TABLE IF NOT EXISTS payments ( 
  account_id INTEGER,
  amount INTEGER,
  direction TEXT,
  label TEXT,
  value_date TEXT,
  creation_date text NOT NULL,

  PRIMARY KEY(account_id,amount,direction,label,value_date)
);