import database as db

TABLE_NAME_TAG = "<TABLE_NAME>"
FIELDS_TAG = "<FIELDS>"
FIELDS_TO_INSERT_TAG = "<FIELDS_TO_INSERT>"


LABEL_TABLE = "labels"
LABEL_FIELDS = """
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    creation_date TEXT NOT NULL
"""
LABEL_FIELDS_TO_INSERT = "id, name, creation_date"


LABEL_TOKEN_TABLE = "labels_tokens"
LABEL_TOKEN_FIELDS = """
    label_id INTEGER NOT NULL,
    token TEXT NOT NULL,
    creation_date TEXT NOT NULL,

    PRIMARY KEY (label_id, token),
    FOREIGN KEY(label_id) REFERENCES labels(id)
"""
LABEL_TOKEN_FIELDS_TO_INSERT = "label_id, token, creation_date"


def create_table(con, table, fields):
    sql_create_table = """
        CREATE TABLE IF NOT EXISTS <TABLE_NAME>
        (
            <FIELDS>
        );
    """
    db.create(
        con, sql_create_table.replace(TABLE_NAME_TAG, table).replace(FIELDS_TAG, fields)
    )


def insert_label_rows(con, rows):
    sql_insert_rows = """
        INSERT INTO <TABLE_NAME>
            (<FIELDS_TO_INSERT>)
        VALUES
            ((SELECT IFNULL(MAX(id), 0) + 1 FROM <TABLE_NAME>), 
            ?, 
            DATETIME('now'));
    """
    db.insert(
        con,
        sql_insert_rows.replace(TABLE_NAME_TAG, LABEL_TABLE).replace(
            FIELDS_TO_INSERT_TAG, LABEL_FIELDS_TO_INSERT
        ),
        rows,
    )


def insert_label_token_rows(con, rows):
    sql_insert_rows = """
        INSERT INTO <TABLE_NAME>
            (<FIELDS_TO_INSERT>)
        VALUES
            (?, ?, 
            DATETIME('now'));
    """
    db.insert(
        con,
        sql_insert_rows.replace(TABLE_NAME_TAG, LABEL_TOKEN_TABLE).replace(
            FIELDS_TO_INSERT_TAG, LABEL_TOKEN_FIELDS_TO_INSERT
        ),
        rows,
    )


def select_all_labels(con):
    return db.select_all(con, LABEL_TABLE)


def select_all_labels_and_tokens(con):
    return db.select_all(con, LABEL_TOKEN_TABLE)


def select_all_tokens_by_label_id(con, label_id):
    select_all = f"SELECT * FROM {LABEL_TOKEN_TABLE} WHERE label_id = {label_id};"
    return con.execute(select_all)


# ----------------------- Test ---------------------------


def test_label_and_token_creation():
    con = db.get_connection(":memory:")
    # con = db.get_connection("database/accounting.db")

    create_table(con, LABEL_TABLE, LABEL_FIELDS)
    create_table(con, LABEL_TOKEN_TABLE, LABEL_TOKEN_FIELDS)

    labels = [
        ("Amazon",),
        ("Carrefour",),
        ("Societe Generale",),
    ]

    labels_tokens = [
        (1, "amazon"),
        (2, "carrefour"),
        (3, "societe generale"),
    ]

    insert_label_rows(con, labels)
    labels = select_all_labels(con)
    db.print_table(labels)

    insert_label_token_rows(con, labels_tokens)
    labels_tokens = select_all_labels_and_tokens(con)
    db.print_table(labels_tokens)

    con.close()


if __name__ == "__main__":
    test_label_and_token_creation()
