import json

import database_label as l_db


DB_NAME = "database/accounting.db"


"""
    create_label(name, token) 
    
    match(tokens, paymnent)
        [matched tokens]

    ? get_all_tokens(label_name) 
    
    saveMapping(pymt id, token id)
"""


# ------------------- Label -------------------


class Label:
    def __init__(self, id, name, tokens=[]):
        self.id = id
        self.name = name
        self.tokens = tokens

    def __str__(self):
        return f"Label #({self.id}): {self.name} (tokens={self.tokens:})"

    def to_json(self):
        return json.dumps(self.__dict__)

    def to_tuple(self): # TODO list in tuple /!\
        return (
            self.name,
            self.tokens,
        )

    @staticmethod
    def map(label_dto):
        return Label(
            label_dto["id"],
            label_dto["name"],
        )


class TaggedPayment:
    def __init__(self, payment_id, label_id):
        self.payment_id = payment_id
        self.label_id = label_id

    def to_tuple(self):
        return (
            self.payment_id,
            self.label_id,
        )

# ------------------- Mapper -------------------


def labels_mapping(labels):
    return [Label.map(label) for label in labels]


def tokens_mapping(tokens):
    return [to_domain(token) for token in tokens]


def to_domain(token_dto):
    return token_dto["token"]


# ------------------- Get -------------------


def get_all_labels():
    con = l_db.db.get_connection(DB_NAME)
    labels_dto = l_db.select_all_labels(con)

    labels = labels_mapping(labels_dto)
    for label in labels:
        tokens = l_db.select_all_tokens_by_label_id(con, label.id)
        label.tokens = tokens_mapping(tokens)

    con.close()
    return sorted(labels, key=lambda l: l.name)


# ------------------- Actions -------------------


def create(label):
    pass


def add_token(label_id, token):
    # if token not exists
    pass


def remove_token(label_id, token):
    # if token not exists
    pass


def reset_token(label_id):
    pass


# ------------------- Tag -------------------

def tag(payments):
    # fetch all tags
    labels = get_all_labels()
    # flattened_tokens = [token for label in labels for token in label.tokens]

    tagged_payments = []
    for label in labels:
        for payment in payments:
            if match(payment.title, label):
                tagged_payments += [TaggedPayment(payment.id, label.id)]

    # save batch to raw_payments_labels
    pass


def match(text, label):
    # use regex ? test perfs
    pass


def untag(payments, tags):
    # remove each tags if present
    pass


# ------------------- Save -------------------

def save_tagged_payment(tagged_payments):
    con = l_db.db.get_connection(DB_NAME)

    rows = [tp.to_tuple() for tp in tagged_payments]
    l_db.insert_payments_rows(con, rows)

    raw_payments = l_db.select_all_raw_payments(con)
    con.close()

    l_db.db.print_table(raw_payments)


# ------------------- Test -------------------


def test():
    # get all
    labels = get_all_labels()
    [print(label) for label in labels]

    # insert new label
    # complete with token
    # filter payments


if __name__ == "__main__":
    test()
