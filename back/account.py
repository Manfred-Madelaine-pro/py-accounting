import json


class Account:
    def __init__(self, id, opening=0):
        self.id = id
        self.name = "My name is Test"
        self.payments = []
        self.opening = opening

    def __str__(self):
        return f"account #{self.id}"

    def get_metrics_per_day(self):
        payments_per_day = get_payments_per_day(self.payments)
        metrics_per_day = {}
        for date, payments in payments_per_day.items():
            metrics_per_day[date] = get_metrics(date, payments)
        return metrics_per_day

    def to_json(self):
        return json.dumps(self.__dict__)


def get_account_metrics(id):
    account = get_account(id)
    return account.get_metrics_per_day()


def get_account(id):
    account = Account(id)
    account.payments = get_all_payments(account)
    return account


# ------------------- Test -------------------


def get_all_payments(account_id):
    import database_payment as p_db

    DB_NAME = "database/accounting.db"

    con = p_db.db.get_connection(DB_NAME)
    raw_payments = p_db.get_all_payments_by_account_id(con, account_id)

    import payment

    payments = payment.map_to_domain(raw_payments)

    return sorted(payments, key=lambda p: p.value_date, reverse=True)


def test():
    account = Account(id=1)

    # get all payments for account 1
    account.payments = get_all_payments(account.id)
    # [print(payment) for payment in account.payments]

    metrics_per_day = account.get_metrics_per_day()
    [print(metric) for _, metric in metrics_per_day.items()]


if __name__ == "__main__":
    test()
