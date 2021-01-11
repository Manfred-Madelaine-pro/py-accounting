import sqlite3
from prettytable import from_db_cursor


def get_connection(db_name):
    con = sqlite3.connect(db_name)
    con.row_factory = sqlite3.Row
    return con


# ----------------------- Actions ---------------------------


def create(con, sql_create):
    with con:
        con.execute(sql_create)


def insert(con, sql_insert, rows):
    with con:
        try:
            con.executemany(sql_insert, rows)
        except sqlite3.IntegrityError:
            return "Line already exists."


def insert_one(con, sql_insert):
    with con:
        try:
            con.execute(sql_insert)
        except sqlite3.IntegrityError:
            return "Line already exists."


def select_all(con, table_name):
    select_all = f"SELECT * FROM {table_name};"
    return con.execute(select_all)


# ----------------------- Display ---------------------------


def print_table(rows):
    table = from_db_cursor(rows)
    print(table)
