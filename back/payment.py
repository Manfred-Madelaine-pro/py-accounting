import json

import database_payment as p_db


CREDIT = "C"
DEBIT = "D"

DB_NAME = "database/accounting.db"


class Payment:
    def __init__(
        self, id, account_id, value_date, amount, direction, title, creation_date
    ):
        self.id = id
        self.account_id = account_id
        self.value_date = value_date
        self.amount = amount
        self.direction = direction
        self.title = title
        self.creation_date = creation_date

    def __str__(self):
        return (
            f"({self.value_date}) account #{self.account_id} "
            f"-> {self.get_signed_amount():>+10,.2f}: {self.title}"
        )

    def get_signed_amount(self):
        return self.amount if self.direction == CREDIT else -self.amount

    def to_json(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def map(payment_dto):
        return Payment(
            payment_dto["id"],
            payment_dto["account_id"],
            payment_dto["value_date"],
            payment_dto["amount"],
            payment_dto["direction"],
            payment_dto["title"],
            payment_dto["creation_date"],
        )


# ------------------- Mapper -------------------


def payments_mapping(payments):
    return [Payment.map(payment) for payment in payments]


# ----------------------- Get ---------------------------


# TODO used ?
def get_all_payments():
    con = p_db.db.get_connection(DB_NAME)
    raw_payments = p_db.select_all_payments(con)

    payments = payments_mapping(raw_payments)
    con.close()

    return sorted(payments, key=lambda p: p.value_date, reverse=True)


# ----------------------- Filter ---------------------------


def get_payments_for(account_id):
    con = p_db.db.get_connection(DB_NAME)
    raw_payments = p_db.filter_all_payments_by_account_id(con, account_id)

    payments = payments_mapping(raw_payments)
    con.close()

    return sorted(payments, key=lambda p: p.value_date, reverse=True)


def get_all_payments_containing(tokens):
    con = p_db.db.get_connection(DB_NAME)
    raw_payments = p_db.filter_all_payments_by_tokens(con, tokens)

    payments = payments_mapping(raw_payments)
    con.close()

    return sorted(payments, key=lambda p: p.value_date, reverse=True)


# ------------------- Test -------------------


def test():
    payments = get_all_payments()
    [print(payment) for payment in payments]


if __name__ == "__main__":
    test()
