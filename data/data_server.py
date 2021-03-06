from shared.auth_middleware import authMiddleware
from threading import Lock
from flask import Flask
from settings import authKeys
from shared.log_repository import LogRepository

app = Flask(__name__)

logRepository = LogRepository()

# this object is like a database with tables, then it has the lock in whole table and lock by id index
# in this case lock in table is just used to add new value, i can edit some value even the table is in lock
database = {
    "accounts": {
        "data": {},
        "lock": Lock()
    }
}


def initAccounts():
    for i in range(1, 11):
        createIfNotExistsItemInAccount(0, i, 1000)


app.wsgi_app = authMiddleware(app.wsgi_app, authKeys)


def lockTable(tableName):
    database[tableName]["lock"].acquire()


def unLockTable(tableName):
    database[tableName]["lock"].release()


def lockItemInTable(tableName, id):
    database[tableName]["data"][id]["lock"].acquire()


def unLockItemInTable(tableName, id):
    database[tableName]["data"][id]["lock"].release()


def getValueInTableById(tableName, id):
    return database[tableName]["data"][id]


def createIfNotExistsItemInAccount(businessId, accountId, initialAmount=0):
    lockTable('accounts')

    if(not accountId in database["accounts"]["data"].keys()):
        database["accounts"]["data"][accountId] = {
            "amount": initialAmount,
            "state": {"locked": False, "owner": businessId},
            "lock": Lock()
        }

    unLockTable('accounts')


def log(logName, businessId, accountId, amount=None):
    amountString = str(amount) if amount != None else 'NULL'
    logRepository.log(str(businessId) + ',' + logName +
                      ',' + str(accountId) + ',' + amountString)


@app.route("/getLock/<int:businessId>/<int:accountId>", methods=['POST'])
def getLock(businessId, accountId):
    createIfNotExistsItemInAccount(businessId, accountId)
    lockItemInTable('accounts', accountId)

    account = getValueInTableById('accounts', accountId)
    if(account["state"]["locked"]):
        unLockItemInTable('accounts', accountId)
        return ("-1", 401)

    account["state"]["locked"] = True
    account["state"]["owner"] = businessId
    unLockItemInTable('accounts', accountId)
    log('getLock', businessId, accountId)
    return ('', 204)


@app.route("/unLock/<int:businessId>/<int:accountId>", methods=['POST'])
def unLock(businessId, accountId):
    createIfNotExistsItemInAccount(businessId, accountId)

    lockItemInTable('accounts', accountId)
    account = getValueInTableById('accounts', accountId)
    if(account["state"]["locked"] and account["state"]["owner"] != businessId):
        unLockItemInTable('accounts', accountId)
        return ("-1", 401)

    account["state"]["locked"] = False
    unLockItemInTable('accounts', accountId)
    log('unLock', businessId, accountId)
    return ('', 204)


@ app.route("/setAmount/<int:businessId>/<int:accountId>/<amount>", methods=['POST'])
def setAmount(businessId, accountId, amount):
    amount = float(amount)
    createIfNotExistsItemInAccount(businessId, accountId)

    lockItemInTable('accounts', accountId)
    account = getValueInTableById('accounts', accountId)
    if(not account["state"]["locked"] or account["state"]["owner"] != businessId):
        unLockItemInTable('accounts', accountId)
        return ("-1", 401)

    account["amount"] = amount
    unLockItemInTable('accounts', accountId)
    log('setAmount', businessId, accountId, amount)
    return ('', 204)


@ app.route("/getAmount/<int:businessId>/<int:accountId>", methods=['GET'])
def getAmount(businessId, accountId):
    createIfNotExistsItemInAccount(businessId, accountId)

    account = getValueInTableById('accounts', accountId)
    if(account["state"]["locked"] and account["state"]["owner"] != businessId):
        return ("-1", 401)

    log('getAmount', businessId, accountId)
    return str(account["amount"])


initAccounts()

if __name__ == "__main__":
    app.run()
