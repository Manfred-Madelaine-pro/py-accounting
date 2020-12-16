import csv

import database_raw_payment as rp_db


DB_NAME = "database/accounting.db"


class RawPayment:
    def __init__(
        self, source, file_name, account_id, value_date, amount, direction, title
    ):
        self.source = source
        self.file_name = file_name
        self.account_id = account_id
        self.value_date = value_date
        self.amount = amount
        self.direction = direction
        self.title = title

    def __str__(self):
        return (
            f"{self.value_date}, {self.amount:>10,.2f}, {self.direction}, {self.title}, "
            f"{self.source}, {self.account_id}, {self.file_name}"
        )

    def to_tuple(self):
        return (
            self.value_date,
            self.amount,
            self.direction,
            self.title,
            self.account_id,
            self.source,
            self.file_name,
        )


# --------------------------- Integrate ---------------------------


def integrate(source_name, dir_path):
    files_raw_payments = get_data_from_all_files(source_name, dir_path)
    save(files_raw_payments)


def save(files_raw_payments):
    con = rp_db.db.get_connection(DB_NAME)

    for f_name, raw_payments in files_raw_payments.items():
        # if file already in DB skip
        if not already_integrated(con, f_name):
            rows = [rp.to_tuple() for rp in raw_payments]
            rp_db.insert_payments_rows(con, rows)

    raw_payments = rp_db.select_all_raw_payments(con)
    con.close()

    rp_db.db.print_table(raw_payments)


def already_integrated(con, f_name):
    sql_results = rp_db.get_distinct_file_name(con)
    files_integrated = [r["file_name"] for r in sql_results]
    return f_name in files_integrated


def get_data_from_all_files(source_name, dir_path):
    # get all files in dir
    files_path = get_all_files_path(dir_path)

    # parse each file
    files_raw_payments = {}
    for f_path in sorted(files_path):
        f_name = get_file_name(f_path)
        files_raw_payments[f_name] = read_file(source_name, f_name, f_path)

    return files_raw_payments


# --------------------------- Societe General Parser ---------------------------


def read_file(source_name, f_name, file_path):
    def skipped(row):
        # True if first character of the row is unexpected
        # or if row is column names
        return ("=" == row[0][0]) or ("date" in row[0])

    with open(file_path, mode="r", encoding="ISO-8859-1") as infile:
        reader = csv.reader(infile)
        account_id = get_account_id(f_name)
        return [
            to_raw_payment(source_name, f_name, account_id, parse(row))
            for row in reader
            if not skipped(row)
        ]


def parse(row):
    row = ",".join(row).replace("é", "e").replace("°", ".").split(";")
    row[1] = " ".join(row[1].split())
    row[2] = string_to_float(row[2])
    return row


def to_raw_payment(source_name, f_name, account_id, row):
    title = row[1]
    amount = row[2]
    value_date = row[0]

    direction = ["D", "C"][amount >= 0]
    amount = abs(amount)

    return RawPayment(
        source_name, f_name, account_id, value_date, amount, direction, title
    )


# --------------------------- Utils ---------------------------


def get_all_files_path(directory):
    import glob

    all_files_regex = "*"
    return glob.glob(directory + all_files_regex)


def get_file_name(f_path):
    return f_path.split("/")[-1]


def get_account_id(f_name):
    return f_name.split("_")[1]


def string_to_float(string):
    string = string.replace(",", ".")
    return -float(string.replace("-", "")) if ("-" in string) else float(string)


# --------------------------- Test ---------------------------


def test():
    source_name = "Societe General"
    dir_path = "../data/sg/"
    files_raw_payments = get_data_from_all_files(source_name, dir_path)

    for f_name, raw_payments in files_raw_payments.items():
        print("- Raw Payments in", f_name, ":")
        [print("", rp) for _, rp in zip(range(10), raw_payments)]


def test2():
    source_name = "Societe General"
    dir_path = "../data/sg/"
    integrate(source_name, dir_path)


if __name__ == "__main__":
    # test()
    test2()
