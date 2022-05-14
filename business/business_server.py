from flask import Flask
from application.bank_service import BankService
from application.queue_service import QueueMessageServer


app = Flask(__name__)
bankService = BankService()
queueService = QueueMessageServer()


@app.route("/deposit/<int:accountId>/<int:amount>", methods=['POST'])
def deposit(accountId, amount):
    queueService.enqueue(bankService.depositWithLock, accountId, amount)
    queueService.executeWhenNeeded()
    return ('', 204)


@app.route("/withdrawal/<int:accountId>/<int:amount>", methods=['POST'])
def withdrawal(accountId, amount):
    queueService.enqueue(bankService.withdrawalWithLock, accountId, amount)
    queueService.executeWhenNeeded()
    return ('', 204)


@app.route("/balance/<int:accountId>", methods=['GET'])
def balance(accountId):
    return str(bankService.getBalance(accountId))


@app.route("/transfer/<int:originAccountId>/<int:targetAccountId>/<int:amount>", methods=['POST'])
def transfer(originAccountId, targetAccountId, amount):
    queueService.enqueue(bankService.transfer,
                         originAccountId, targetAccountId, amount)
    queueService.executeWhenNeeded()
    return ('', 204)


if __name__ == "__main__":
    app.run()
