import database as db


TABLE_NAME = "raw_payments"


def create_table(con):
    sql_create_table = """
        CREATE TABLE IF NOT EXISTS TABLE_NAME
        (
            id INTEGER,
            value_date TEXT,
            amount REAL,
            direction TEXT,
            title TEXT,
            account_id INTEGER, 
            source TEXT,
            file_name TEXT,
        
            creation_date text NOT NULL
        );
    """
    db.create(con, sql_create_table.replace("TABLE_NAME", TABLE_NAME))


def insert_payments_rows(con, rows):
    sql_insert_rows = """
        INSERT INTO TABLE_NAME
            (id, 
            value_date, amount, direction, title, account_id, source, file_name, 
            creation_date)
        VALUES
            ((SELECT IFNULL(MAX(id), 0) + 1 FROM TABLE_NAME), 
            ?, ?, ?, ?, ?, ?, ?, 
            DATETIME('now'));
    """
    db.insert(con, sql_insert_rows.replace("TABLE_NAME", TABLE_NAME), rows)


def select_all_raw_payments(con):
    return db.select_all(con, TABLE_NAME)


def get_distinct_file_name(con):
    select_distinct = f"SELECT DISTINCT file_name FROM {TABLE_NAME};"
    return con.execute(select_distinct)


# ----------------------- Test ---------------------------


def test_raw_payment_creation():
    con = db.get_connection(":memory:")
    # con = db.get_connection("database/accounting.db")
    create_table(con)

    account_id = 1
    raw_payments = [
        ("2020-12-20", "100", "C", "salary", account_id, "SG", "file.csv"),
        ("2020-12-20", "5", "D", "food", account_id, "SG", "file.csv"),
        ("2020-12-20", "15", "D", "netflix", account_id, "SG", "file.csv"),
    ]

    insert_payments_rows(con, raw_payments)
    raw_payments = select_all_raw_payments(con)
    db.print_table(raw_payments)

    con.close()


if __name__ == "__main__":
    test_raw_payment_creation()
