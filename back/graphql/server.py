from flask import Flask
from flask_graphql import GraphQLView

from controller import account_schema

app = Flask(__name__)
app.add_url_rule(
    "/accounts",
    view_func=GraphQLView.as_view("graphql", schema=account_schema, graphiql=True),
)

app.run()
