

# ------------------- Test -------------------


def test():
    # payments = fetch_from_db()
    print("Hi")


def fetch_from_db():
    import account as acc

    return acc.get_all_payments(account_id=1)


if __name__ == "__main__":
    test()
