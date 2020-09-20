import sqlite3
from prettytable import from_db_cursor


def get_connection(db_name):
    con = sqlite3.connect(db_name)
    con.row_factory = sqlite3.Row
    return con


# ----------------------- Payments ---------------------------


def create_payments_table(con):
    sql_create_payments_table = """
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER, 
            account_id INTEGER, value_date TEXT,
            amount INTEGER, direction TEXT,
            details TEXT, 
            creation_date text NOT NULL,
        PRIMARY KEY(account_id, value_date, amount, direction));
    """
    with con:
        con.execute(sql_create_payments_table)


def insert_payments_rows(con, rows):
    sql_insert_payments = """
        INSERT INTO payments 
            (id, account_id, value_date, amount, direction, details, creation_date)
        VALUES
            ((SELECT IFNULL(MAX(id), 0) + 1 FROM payments), ?, ?, ?, ?, ?, DATETIME('now'));
    """
    with con:
        try:
            con.executemany(sql_insert_payments, rows)
        except sqlite3.IntegrityError:
            return "Line already exists."


def select_all(con, table_name):
    select_all = f"SELECT * FROM {table_name} ORDER by creation_date desc LIMIT 10;"
    return con.execute(select_all)


def get_all_payments(con):
    return select_all(con, "payments")


# ----------------------- Test ---------------------------


def print_table(rows):
    table = from_db_cursor(rows)
    print(table)


def print_table2(con, table_name):
    print(table_name.title())
    rows = select_all(con, table_name)
    table = from_db_cursor(rows)
    print(table)


def test_database_creation():
    con = get_connection(":memory:")
    # con = get_connection("database/events.db")
    create_payments_table(con)

    payments = [
        ("1", "20/12/2020", "70", "C", "tst 1"),
        ("1", "20/12/2020", "7", "C", "tst 2"),
        ("1", "19/12/2020", "10", "D", "tst 3"),
        ("1", "19/12/2020", "20", "C", "tst 2"),
        ("1", "02/12/2020", "200", "D", "tst 2"),
        ("1", "02/12/2020", "20", "C", "tst 2"),
        ("1", "20/12/2020", "100", "C", "tst 2"),
        ("1", "20/12/2020", "100", "C", "tst 2"), # Duplication
    ]

    insert_payments_rows(con, payments)
    payments = get_all_payments(con)
    print_table(payments)

    con.close()


if __name__ == "__main__":
    test_database_creation()
