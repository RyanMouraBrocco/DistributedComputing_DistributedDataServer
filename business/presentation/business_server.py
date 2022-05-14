from flask import Flask
from business.application.bank_service import BankService


app = Flask(__name__)
bankService = BankService()


@app.route("/deposit/<int:accountId>/<int:amount>", methods=['POST'])
def deposit(accountId, amount):
    
    return ('', 204)


@app.route("/withdrawal/<int:accountId>/<int:amount>", methods=['POST'])
def withdrawal(accountId, amount):

    return ('', 204)


@app.route("/balance/<int:accountId>", methods=['GET'])
def balance(accountId):
    return ('', 200)


@app.route("/transfer/<int:originAccountId>/<int:targetAccountId>/<int:amount>", methods=['POST'])
def transfer(originAccountId, targetAccountId, amount):
    return ('', 204)


if __name__ == "__main__":
    app.run()
