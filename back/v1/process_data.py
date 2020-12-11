LABEL_ID = 1
AMOUNT_ID = 2


class Monthly_payments:
    def __init__(self, date, payments):
        self.date = date
        self.payments = payments

        self.debits = []
        self.credits = []
        self.total_credit = 0
        self.total_debit = 0

        self.fixed_debits = []
        self.fixed_credits = []
        self.total_fixed_credits = 0
        self.total_fixed_debits = 0

        self.process_payments()

    def process_payments(self):
        for p in self.payments:
            if p[AMOUNT_ID] < 0:
                self.debits += [p[AMOUNT_ID]]
            else:
                self.credits += [p[AMOUNT_ID]]

        self.total_credit = sum(self.credits)
        self.max_credit = max(self.credits)

        self.total_debit = sum(self.debits)
        self.min_debit = min(self.debits)

        self.cash = self.total_debit + self.total_credit

    # Move everything to DB !! create tables and views that are created on the fly
    def add_fix_payment(self, label, amount):
        if amount > 0:
            self.fixed_credits += [amount]
            self.total_fixed_credits = sum(self.fixed_credits)
        else:
            self.fixed_debits += [amount]
            self.total_fixed_debits = sum(self.fixed_debits)

    def __repr__(self):
        fa = lambda a: f"{a:,.2f} EUR"

        txt = ""
        txt += f"{self.date} :"
        txt += "\n"
        txt += (
            f"\tTotal credit : {fa(self.total_credit)} \t (Max : {fa(self.max_credit)})"
        )
        txt += (
            f"\t (Fixed : {fa(self.total_fixed_credits)})"
            if self.total_fixed_credits
            else ""
        )
        txt += "\n"
        txt += f"\tTotal dedit : {fa(self.total_debit)} \t (Min : {fa(self.min_debit)})"
        txt += (
            f"\t (Fixed : {fa(self.total_fixed_debits)})"
            if self.total_fixed_debits
            else ""
        )
        txt += "\n"
        txt += f"\tCash : {fa(self.cash)}"
        return txt


if __name__ == "__main__":
    payments = [
        ["05/08/2020", "CARTE X9372 04/08 SOCIETE GENERAL", -0.3, "EUR"],
        [
            "05/08/2020",
            "VIR RECU 3596405960S DE: CAF DE L ESSONNE MOTIF: XPXREFERENCE 023183784 ME 7522052KMADELAINE 072020ME",
            308.0,
            "EUR",
        ],
        [
            "04/08/2020",
            "VIR RECU 3593215985S DE: Ruben Madelaine MOTIF: - REF: c314c28da3604be0b7b0f21ab202ace5",
            400.0,
            "EUR",
        ],
        ["04/08/2020", "CHEQUE 6", -340.0, "EUR"],
        [
            "03/08/2020",
            "000001 VIR EUROPEEN EMIS LOGITEL POUR: Qantum Cats Group REF: 9021617023763 MOTIF: Approvisionnement",
            -2200.0,
            "EUR",
        ],
    ]

    mp = Monthly_payments("/".join(payments[0][0].split("/")[1:]), payments)
    print(mp)
