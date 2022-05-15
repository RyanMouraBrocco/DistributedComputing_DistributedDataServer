from concurrent.futures import process
from flask import Flask
from application.bank_service import BankService
from application.queue_service import QueueMessageServer
from shared.auth_middleware import authMiddleware
from settings import authKeys


app = Flask(__name__)
bankService = BankService()
queueService = QueueMessageServer()
app.wsgi_app = authMiddleware(app.wsgi_app, authKeys)


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
    app.run(threaded=True, process=10)
