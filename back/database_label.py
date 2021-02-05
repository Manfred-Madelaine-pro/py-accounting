import database as db

TABLE_NAME_TAG = "<TABLE_NAME>"
FIELDS_TAG = "<FIELDS>"
FIELDS_TO_INSERT_TAG = "<FIELDS_TO_INSERT>"


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


# ----------------------- Label ---------------------------


LABEL_TABLE = "labels"
LABEL_FIELDS = """
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    creation_date TEXT NOT NULL,
    
    UNIQUE(name)
"""
LABEL_FIELDS_TO_INSERT = "id, name, creation_date"


def insert_label_rows(con, rows):
    sql_insert_rows = """
        INSERT OR IGNORE INTO <TABLE_NAME>
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


def insert_label(con, name):
    sql_insert_label = """
        INSERT OR IGNORE INTO <TABLE_NAME>
            (<FIELDS_TO_INSERT>)
        VALUES
            ((SELECT IFNULL(MAX(id), 0) + 1 FROM <TABLE_NAME>), 
            "?", 
            DATETIME('now'));
    """
    req = (
        sql_insert_label.replace(TABLE_NAME_TAG, LABEL_TABLE)
        .replace(FIELDS_TO_INSERT_TAG, LABEL_FIELDS_TO_INSERT)
        .replace("?", name)
    )
    db.insert_one(con, req)


def update_label(con, label_id, name):
    sql = f'UPDATE labels SET name = "{name}" WHERE id = {label_id}'
    return con.execute(sql)


def select_all_labels(con):
    return db.select_all(con, LABEL_TABLE)


# ----------------------- Label Token ---------------------------


LABEL_TOKEN_TABLE = "labels_tokens"
LABEL_TOKEN_FIELDS = """
    id INTEGER PRIMARY KEY,
    label_id INTEGER NOT NULL,
    token TEXT NOT NULL,
    creation_date TEXT NOT NULL,
    
    UNIQUE(label_id, token)
    FOREIGN KEY(label_id) REFERENCES labels(id)
"""
LABEL_TOKEN_FIELDS_TO_INSERT = "id, label_id, token, creation_date"


def insert_label_token_rows(con, rows):
    sql_insert_rows = """
        INSERT OR IGNORE INTO <TABLE_NAME>
            (<FIELDS_TO_INSERT>)
        VALUES
            ((SELECT IFNULL(MAX(id), 0) + 1 FROM <TABLE_NAME>), 
            ?, ?, 
            DATETIME('now'));
    """
    db.insert(
        con,
        sql_insert_rows.replace(TABLE_NAME_TAG, LABEL_TOKEN_TABLE).replace(
            FIELDS_TO_INSERT_TAG, LABEL_TOKEN_FIELDS_TO_INSERT
        ),
        rows,
    )


def insert_token(con, label_id, token):
    sql_insert_token = """INSERT OR IGNORE INTO labels_tokens (id, label_id, token, creation_date)
    VALUES ((SELECT IFNULL(MAX(id), 0) + 1 FROM labels_tokens),  """
    sql_insert_token += f' "{label_id}", "{token}", DATETIME("now"));'
    db.insert_one(con, sql_insert_token)


def select_all_labels_with_tokens(con):
    sql = """
    SELECT lb.id label_id, name, lt.id token_id, token 
    FROM labels lb 
    LEFT JOIN labels_tokens lt 
    ON lb.id = lt.label_id;
    """
    return con.execute(sql)


# TODO used ?
def select_all_tokens(con):
    return db.select_all(con, LABEL_TOKEN_TABLE)


def select_all_tokens_by_label_id(con, label_id):
    select_all = f"SELECT * FROM {LABEL_TOKEN_TABLE} WHERE label_id = {label_id};"
    return con.execute(select_all)


# ----------------------- Tagged Payment ---------------------------


TAGGED_PAYMENT_TABLE = "tagged_payments"
TAGGED_PAYMENT_FIELDS = """
    payment_id INTEGER NOT NULL,
    label_id INTEGER NOT NULL,
    creation_date TEXT NOT NULL,

    PRIMARY KEY (payment_id, label_id),
    FOREIGN KEY(label_id) REFERENCES labels(id)
    FOREIGN KEY(payment_id) REFERENCES raw_payment(id)
"""
TAGGED_PAYMENT_FIELDS_TO_INSERT = "payment_id, label_id, creation_date"


def insert_tagged_payment_rows(con, rows): # TODO used ?
    sql_insert_rows = """
        INSERT OR IGNORE INTO <TABLE_NAME>
            (<FIELDS_TO_INSERT>)
        VALUES
            (?, ?, 
            DATETIME('now'));
    """
    db.insert(
        con,
        sql_insert_rows.replace(TABLE_NAME_TAG, TAGGED_PAYMENT_TABLE).replace(
            FIELDS_TO_INSERT_TAG, TAGGED_PAYMENT_FIELDS_TO_INSERT
        ),
        rows,
    )


def insert_tagged_payment(con, payment_id, label_id):
    sql_insert_token = "INSERT OR IGNORE INTO tagged_payments (payment_id, label_id, creation_date)"
    sql_insert_token += f' VALUES ("{payment_id}", "{label_id}", DATETIME("now"));'
    db.insert_one(con, sql_insert_token)


def select_all_tagged_payments(con):
    return db.select_all(con, TAGGED_PAYMENT_TABLE)


def get_payments_grouped_by_token(con):
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
        ("CAF",),
    ]

    labels_tokens = [
        (1, "amazon"),
        (2, "carrefour"),
        (3, "societe generale"),
        (1, "amz"),
    ]

    tagged_payment = [
        (1, 1),
        (1, 2),
        (2, 3),
    ]

    insert_label_rows(con, labels)
    labels = select_all_labels(con)
    db.print_table(labels)

    insert_label_token_rows(con, labels_tokens)
    labels_tokens = select_all_tokens(con)
    db.print_table(labels_tokens)

    create_table(con, TAGGED_PAYMENT_TABLE, TAGGED_PAYMENT_FIELDS)

    insert_tagged_payment_rows(con, tagged_payment)
    tagged_payment = select_all_tagged_payments(con)
    db.print_table(tagged_payment)

    con.close()


if __name__ == "__main__":
    test_label_and_token_creation()
