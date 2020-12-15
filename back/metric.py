import datetime
import json

DAY = "day"
WEEK = "week"
MONTH = "month"
YEAR = "year"
SUPPORTED_PERIODS = [DAY, WEEK, MONTH, YEAR]

UP_TO_MONTH_DIGITS = 7
UP_TO_YEAR_DIGITS = 4


# ------------------- Metrics -------------------


class Metrics:
    def __init__(self, period, payments):
        self.period = period
        # self.payments = payments

        self.credits_count = len([1 for p in payments if p.get_signed_amount() >= 0])
        self.debits_count = len(payments) - self.credits_count
        self.simple_metrics(payments)

    def __str__(self):
        return (
            f"{self.period} (--{self.debits_count}/++{self.credits_count}): {self.sum_payment:>+10,.2f}, "
            f"(min:{self.min_payment:>+10,.2f} / max:{self.max_payment:>+10,.2f} / avg:{self.avg_payment:>+10,.2f})"
        )

    def to_json(self):
        return json.dumps(self.__dict__)

    def simple_metrics(self, payments):
        amounts = [payment.get_signed_amount() for payment in payments]
        self.min_payment = min(amounts)
        self.max_payment = max(amounts)
        self.sum_payment = sum(amounts)
        self.avg_payment = sum(amounts) / len(amounts)


# ------------------- Calculate Metrics -------------------


def calculate_metrics(period, payments):
    grouped_payments = group_by(period, payments)
    metrics = {}
    for period, payments in grouped_payments.items():
        metrics[period] = Metrics(period, payments)
    return metrics


# ------------------- Group By -------------------


def group_by(period, payments):
    group_by_map = {
        DAY: group_by_day,
        WEEK: group_by_week,
        MONTH: group_by_month,
        YEAR: group_by_year,
    }
    return group_by_map[period](payments)


def group_by_day(payments):
    return group(payments, lambda p: p.value_date)


def group_by_week(payments):
    return group(payments, lambda p: str_to_date(p.value_date).isocalendar()[1])


def group_by_month(payments):
    return group(payments, lambda p: p.value_date[:UP_TO_MONTH_DIGITS])


def group_by_year(payments):
    return group(payments, lambda p: p.value_date[:UP_TO_YEAR_DIGITS])


# -- Utils

def group(payments, key):
    grouped_by = {}
    for p in payments:
        grouped_by[key(p)] = grouped_by.get(key(p), []) + [p]
    return grouped_by


def str_to_date(str):
    return datetime.datetime.strptime(str, "%Y-%m-%d").date()


# ------------------- Test -------------------


def test():
    # payments = generate_fake_payments()
    payments = fetch_from_db()
    sorted_payments = sorted(payments, key=lambda p: p.value_date, reverse=True)
    # [print(p) for p in sorted_payments]

    # test_all_group_by(payments)
    for period in SUPPORTED_PERIODS[-1:1:-1]:
        print(period, ":")
        metrics = calculate_metrics(period, payments)
        [print("\t", metric) for _, metric in metrics.items()]


def generate_fake_payments():
    import payment as pymt
    from datetime import date

    acc_id = 1
    d = ["D", "C"]
    vds = ["2020-11-10", "2020-12-11", "2020-12-12"]
    return [pymt.Payment(i,
                         acc_id,
                         vds[i % len(vds)],
                         i * 10,
                         d[i % len(d)],
                         f"pymt {i}",
                         date.today())
            for i in range(1, 10)]


def fetch_from_db():
    import account as acc

    account_id = 1
    return acc.get_all_payments(account_id)



def test_all_group_by(payments):
    print()
    res = group_by(DAY, payments)
    [print(k, v) for k, v in res.items()]

    print()
    res = group_by(WEEK, payments)
    [print(k, v) for k, v in res.items()]

    print()
    res = group_by(MONTH, payments)
    [print(k, v) for k, v in res.items()]

    print()
    res = group_by(YEAR, payments)
    [print(k, v) for k, v in res.items()]


if __name__ == "__main__":
    test()
