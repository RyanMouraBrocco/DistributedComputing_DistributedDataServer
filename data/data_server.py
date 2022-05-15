from shared.auth_middleware import authMiddleware
from threading import Lock
from flask import Flask
from settings import authKeys

app = Flask(__name__)

# this object is like a database with tables, then it has the lock in whole table and lock by id index
# in this case lock in table is just used to add new value, i can edit some value even the table is in lock
database = {
    "accounts": {
        "data": {},
        "lock": Lock()
    }
}

#app.wsgi_app = authMiddleware(app.wsgi_app, authKeys)


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


def createIfNotExistsItemInAccount(businessId, accountId):
    lockTable('accounts')

    if(not accountId in database["accounts"]["data"].keys()):
        database["accounts"]["data"][accountId] = {
            "amount": 0,
            "state": {"locked": False, "owner": businessId},
            "lock": Lock()
        }

    unLockTable('accounts')


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
    return ('', 204)


@ app.route("/getAmount/<int:businessId>/<int:accountId>", methods=['GET'])
def getAmount(businessId, accountId):
    createIfNotExistsItemInAccount(businessId, accountId)

    account = getValueInTableById('accounts', accountId)
    if(account["state"]["locked"] and account["state"]["owner"] != businessId):
        return ("-1", 401)

    return str(account["amount"])


if __name__ == "__main__":
    app.run()
