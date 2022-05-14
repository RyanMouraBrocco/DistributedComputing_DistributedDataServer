from flask import Flask


app = Flask(__name__)


@app.route("/deposit/<int:accountId>/<int:amount>", methods=['POST'])
def deposit(accountId, amount):

    return ('', 204)


@app.route("/deposit/<int:accountId>/<int:amount>", methods=['POST'])
def deposit(accountId, amount):

    return ('', 204)


if __name__ == "__main__":
    app.run()
