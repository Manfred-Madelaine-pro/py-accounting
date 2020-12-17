

# payments have only one tag => apply tag based on regex or enforce a tag
# if a payment is already tagged, must confirm the change for the new tag
# groups use tags to fetch payments
# groups can be based on bare tags but also on other groups (i.e. sub groups)

# groups => id, name
# tag => id, name, token
# groups_tags => group_id, tag_id ( what about sub_group_id ?)
# payments_tags => payment_id, tag_id, details (add some information about the payment, may be null)


# be careful of cyclic dependencies
# comment garantir le non entrecoupage des tags ou groups ? appliquer 2 fois un paiement dans des calculs fausse la valeur
# exemple: tag "commerce electronique" et "Amazon"

# on pourrait avoir une table de (paiment X tag) indexée sur les 2 pour augmenter le temps de recherche
# on parserait les titres de paiements pour en sortir des tags
# on applique un nouveau tag sur toute la table des paiements ou une portion (date)
# (payment_id, tag_id)

# ------------------- Test -------------------


def test():
    # payments = fetch_from_db()
    print("Hi")


def fetch_from_db():
    import account as acc

    return acc.get_all_payments(account_id=1)


if __name__ == "__main__":
    test()
