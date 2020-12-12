class Account:
    def __init__(self, id, opening=0):
        self.id = id
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


def get_payments_per_day(payments):
    import itertools

    return {
        vd: list(payments_group)
        for vd, payments_group in itertools.groupby(payments, lambda p: p.value_date)
    }


# ------------------- Metrics -------------------


def get_metrics(date, payments):
    return Metrics(date, payments)


class Metrics:
    def __init__(self, period, payments):
        self.period = period
        self.payments = payments

        self.credits_count = len([1 for p in payments if p.get_signed_amount() >= 0])
        self.debits_count = len(payments) - self.credits_count

        amounts = [payment.get_signed_amount() for payment in payments]
        self.consumption = sum(amounts)
        self.min_payment = min(amounts)
        self.max_payment = max(amounts)

    def __str__(self):
        return (
            f"{self.period} (--{self.debits_count}/++{self.credits_count}): {self.consumption:>+10,.2f}, "
            f"(min:{self.min_payment:>+10,.2f} / max:{self.max_payment:>+10,.2f})"
        )


# ------------------- Test -------------------


def get_all_payments(account):
    import database as db

    DB_NAME = "database/accounting.db"

    con = db.get_connection(DB_NAME)
    raw_payments = db.get_all_payments_by_account_id(con, account.id)

    import payment

    payments = payment.map_to_domain(raw_payments)

    return sorted(payments, key=lambda p: p.value_date, reverse=True)


def test():
    account = Account(id=1)

    # get all payments for account 1
    account.payments = get_all_payments(account)
    [print(payment) for payment in account.payments]

    metrics_per_day = account.get_metrics_per_day()
    [print(metric) for _, metric in metrics_per_day.items()]


if __name__ == "__main__":
    test()
