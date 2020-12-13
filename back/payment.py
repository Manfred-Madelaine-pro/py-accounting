import json


CREDIT = "C"
DEBIT = "D"


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


# ------------------- Mapper -------------------


def map_to_domain(payments):
    return [to_domain(payment) for payment in payments]


def to_domain(payment):
    return Payment(
        payment["id"],
        payment["account_id"],
        payment["value_date"],
        payment["amount"],
        payment["direction"],
        payment["title"],
        payment["creation_date"],
    )


# ------------------- Test -------------------


def test():
    import database as db

    DB_NAME = "database/accounting.db"

    con = db.get_connection(DB_NAME)
    raw_payments = db.get_all_payments(con)

    payments = map_to_domain(raw_payments)
    sorted_payments = sorted(payments, key=lambda p: p.value_date, reverse=True)

    # display all payments
    [print(payment) for payment in sorted_payments]


if __name__ == "__main__":
    test()
