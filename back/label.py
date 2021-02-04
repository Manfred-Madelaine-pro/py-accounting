import json

import database_label as l_db


DB_NAME = "database/accounting.db"


# ------------------- Label -------------------


class Label:
    def __init__(self, id, name, tokens=None):
        if tokens is None:
            tokens = []
        self.id = id
        self.name = name
        self.tokens = tokens

    def __str__(self):
        return f"Label #{self.id}: {self.name:20} tokens=({', '.join([str(token) for token in self.tokens])})"

    def to_json(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def map(label_dto):
        return Label(
            label_dto["id"],
            label_dto["name"],
        )


class Token:
    def __init__(self, id, token):
        self.id = id
        self.token = token

    def __str__(self):
        return f"#{self.id}: {self.token}"


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


def label_token_mapping(label_token_dto):
    return (
        label_token_dto["label_id"],
        label_token_dto["name"],
        label_token_dto["token_id"],
        label_token_dto["token"],
    )


# ------------------- Get -------------------


def get_all_labels():
    con = l_db.db.get_connection(DB_NAME)
    labels_with_tokens_dto = l_db.select_all_labels_with_tokens(con)

    labels = {}
    for label_token in labels_with_tokens_dto:
        label_id, name, token_id, token = label_token_mapping(label_token)
        labels[label_id] = labels.get(label_id, Label(label_id, name))
        labels[label_id].tokens += [Token(token_id, token)] if token else []

    con.close()
    return sorted(labels.values(), key=lambda l: l.name)


def get_all_tagged_payments():
    con = l_db.db.get_connection(DB_NAME)
    labels_with_tokens_dto = l_db.select_all_labels_with_tokens(con)

    labels = {}
    for label_token in labels_with_tokens_dto:
        label_id, name, token_id, token = label_token_mapping(label_token)
        labels[label_id] = labels.get(label_id, Label(label_id, name))
        labels[label_id].tokens += [Token(token_id, token)] if token else []

    con.close()
    return sorted(labels.values(), key=lambda l: l.name)


# ------------------- Actions -------------------


def connect_and_execute(action, *args):
    con = l_db.db.get_connection(DB_NAME)
    action(con, *args)
    con.commit()
    con.close()


def create(label_name):
    connect_and_execute(l_db.insert_label, label_name)


def update_name(label_id, new_name):
    connect_and_execute(l_db.update_label, label_id, new_name)


def add_token(label_id, token):
    # if token not exists
    connect_and_execute(l_db.insert_token, label_id, token)


def remove_token(label_id, token_id):
    # if token not exists
    pass


# ------------------- Tag -------------------


def tag(payments):
    labels = get_all_labels()

    tagged_payments = []
    for label in labels:
        for payment in payments:
            if match(payment.title, label):
                tagged_payments += [TaggedPayment(payment.id, label.id)]

    save_tagged_payment(tagged_payments)  # TODO test


def match(text, label):
    for t in label.tokens:
        print(t.token.lower() in text.lower(), t.token.lower(), text.lower(), text.lower().find(t.token.lower()))
    return len([1 for t in label.tokens if t.token.lower() in text.lower()]) > 0


def untag(payments, tags):
    # remove each tags if present
    pass


# ------------------- Save -------------------

# TODO tests
def save_tagged_payment(tagged_payments):
    con = l_db.db.get_connection(DB_NAME)

    [l_db.insert_tagged_payment(con, *tp.to_tuple()) for tp in tagged_payments]

    raw_payments = l_db.select_all_tagged_payments(con)
    # l_db.db.print_table(raw_payments)

    con.close()


# ------------------- Test -------------------


def test():
    # insert new label
    new_label = "Retrait DAB"
    create(new_label)
    new_label = "Caisse d'Allocation Familliale"
    create(new_label)
    new_label = "Employeur SG"
    create(new_label)
    new_label = "Nexity Studea"
    create(new_label)
    new_label = "Quantum Cats Group"
    create(new_label)
    new_label = "Auchan Villebon"
    create(new_label)
    new_label = "Carrefour Market"
    create(new_label)
    new_label = "Lessive"
    create(new_label)
    new_label = "RATP"
    create(new_label)
    new_label = "Navigo"
    create(new_label)
    new_label = "Bouygues Telecom"
    create(new_label)
    new_label = "Electricite de France"
    create(new_label)
    new_label = "DGFIP impots"
    create(new_label)
    new_label = "PayPal"
    create(new_label)
    new_label = "Netflix"
    create(new_label)
    new_label = "Maison Chapin"
    create(new_label)

    # update name
    # update_name(6, "Caisse d'Allocation Familliale")

    labels = get_all_labels()
    [print(label) for label in labels]

    # complete with token
    new_token = "RETRAIT DAB"
    add_token(5, new_token)
    new_token = "CAF DE L ESSONNE"
    add_token(6, new_token)
    new_token = "SOCIETE GENERALE MOTIF: Appointements"
    add_token(7, new_token)
    new_token = "Nexity studea"
    add_token(8, new_token)
    new_token = "Quantum Cats Group"
    add_token(9, new_token)
    new_token = "AUCHAN VILLEBON"
    add_token(10, new_token)
    new_token = "CARREFOURMARKET"
    add_token(11, new_token)
    new_token = "JLT MATIC"
    add_token(12, new_token)
    new_token = "RATP"
    add_token(13, new_token)
    new_token = "Navigo"
    add_token(14, new_token)
    new_token = "BOUYGUES TELECOM"
    add_token(15, new_token)
    new_token = "ELECTRICITE DE FRANCE"
    add_token(16, new_token)
    new_token = "DGFIP IMPOT"
    add_token(17, new_token)
    new_token = "PAYPAL"
    add_token(18, new_token)
    new_token = "Netflix"
    add_token(19, new_token)
    new_token = "MAISON CHOPIN"
    add_token(20, new_token)


def test_on_payments():
    # get pymts
    import payment as p

    payments = p.get_all_payments()
    tag(payments)

    # get tagged p


if __name__ == "__main__":
    test()
    test_on_payments()