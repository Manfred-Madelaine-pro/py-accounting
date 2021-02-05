import database as db


TABLE_NAME = "v_raw_payments"


def create_table(con):
    sql_create_table = """
        CREATE TABLE IF NOT EXISTS TABLE_NAME
        (
            id INTEGER PRIMARY KEY, 
            account_id INTEGER, value_date TEXT,
            amount REAL, direction TEXT,
            title TEXT, 
            creation_date text NOT NULL,
        PRIMARY KEY(account_id, value_date, amount, direction)
        );
    """
    db.create(con, sql_create_table.replace("TABLE_NAME", TABLE_NAME))


def insert_rows(con, rows):
    sql_insert_rows = """
        INSERT INTO TABLE_NAME        
            (id, 
            account_id, value_date, amount, direction, title, 
            creation_date)
        VALUES
            ((SELECT IFNULL(MAX(id), 0) + 1 FROM TABLE_NAME), 
            ?, ?, ?, ?, ?, 
            DATETIME('now'));
    """
    db.insert(con, sql_insert_rows.replace("TABLE_NAME", TABLE_NAME), rows)


def select_all_payments(con):
    return db.select_all(con, TABLE_NAME)

    # ----------------------- Filter ---------------------------


def filter_all_payments_by_account_id(con, account_id):
    select_all = f"SELECT * FROM {TABLE_NAME} WHERE account_id = {account_id};"
    return con.execute(select_all)


def filter_all_payments_by_tokens(con, tokens):
    filters = " OR ".join([f"title LIKE '%{token}%'" for token in tokens])
    select_all = f"SELECT * FROM {TABLE_NAME} WHERE {filters};"
    return con.execute(select_all)


# ----------------------- Test ---------------------------


def test_payment_creation():
    con = db.get_connection(":memory:")
    # con = db.get_connection("database/accounting.db")
    create_table(con)

    account_id = 1
    payments = [
        (account_id, "2020-12-20", "70", "C", "tst 1"),
        (account_id, "2020-12-20", "7", "C", "tst 2"),
        (account_id, "2020-12-19", "10", "D", "tst 3"),
        (account_id, "2020-12-19", "20", "C", "tst 2"),
        (account_id, "2020-12-02", "200", "D", "tst 2"),
        (account_id, "2020-12-02", "20", "C", "tst 2"),
        (account_id, "2020-12-20", "100", "C", "tst 2"),
        (account_id + 1, "2020-12-20", "50", "C", "tst 1"),
        (account_id + 1, "2020-12-20", "500", "C", "tst 2"),
        (account_id + 1, "2020-12-19", "200", "D", "tst 3"),
        (account_id, "2020-12-20", "100", "C", "tst 2"),  # Duplication
    ]

    insert_rows(con, payments)
    payments = select_all_payments(con)
    db.print_table(payments)

    con.close()


if __name__ == "__main__":
    test_payment_creation()
