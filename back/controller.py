from flask import Flask, url_for, render_template, jsonify, request

import account

app = Flask(__name__)


@app.route("/")
def index():
    return "Index Page"


@app.errorhandler(404)
def page_not_found(error):
    return render_template("page_not_found.html"), 404


@app.route("/accounts/<id>/payments")
def accounts_payments_api(id):
    payments = account.get_account(id).payments
    if not payments:
        return page_not_found("")

    return jsonify([payment.to_json() for payment in payments])


@app.route("/accounts/<id>/metrics")
def accounts_metrics_api(id):
    metrics = account.get_account_metrics(id)

    date = request.args.get("date")
    if date:
        metrics = {k: metric for k, metric in metrics.items() if k == date}

    return jsonify([metric.to_json() for metric in metrics.values()])


if __name__ == "__main__":
    with app.test_request_context():
        print(url_for("index"))
        print(url_for("accounts_payments_api", id=1))
        print(url_for("accounts_metrics_api", id=1))
        print(url_for("accounts_metrics_api", id=1, date="2020-12-20"))
