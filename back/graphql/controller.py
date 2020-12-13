import graphene
import account


class Account(graphene.ObjectType):
    id = graphene.ID(required=True)
    value_date = graphene.Date()  # Optional filter
    name = graphene.String()
    payments = graphene.String()
    instant_balance = graphene.Int()


class Query(graphene.ObjectType):
    account = graphene.Field(
        Account,
        description="Look up an account by ID.",
        id=graphene.Argument(
            graphene.ID, description="ID of the account.", required=True
        ),
    )

    def resolve_account(self, info, id):
        extracted = account.get_account(id)
        return Account(
            id=id,
            name=extracted.name,
            payments=extracted.payments,
            # instant_balance=extracted.instant_balance
        )


account_schema = graphene.Schema(query=Query)
