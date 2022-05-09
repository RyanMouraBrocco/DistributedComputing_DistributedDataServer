from flask import Flask
app = Flask(__name__)


# here for a simplify the implementation i will use a database lock in whole table always and not per index
database = {
    "accounts": {
        "data": {
            2: {
                "data": 200,
                "state": {"locked": False, "owner": 1}
            }
        },
        "lock": Lock()
    }
}


def getOrAddAccountInDictionary(businessId, accountId):
    database["accounts"]["lock"].acquire()

    if(database["accounts"]["data"][accountId] == None):
        database["accounts"][accountId] = {
            data: 0, state: {locked: False, owner: businessId}}

    database["accounts"]["lock"].release()

    return database["accounts"][accountId]


@app.route("/")
def getLock(businessId, accountId):
    currentItem = getOrAddAccountInDictionary(businessId, accountId)
    if(currentItem.state.locked)
    return -1

    currentItem.state.locked = True


@app.route("/")
def unLock(businessId, accountId):
    currentItem = getOrAddAccountInDictionary(businessId, accountId)
    if(currentItem.state.locked and currentItem.state.owner != businessId)
    return -1

    currentItem.state.locked = False


@app.route("/")
def setAmount(businessId, accountId):
    currentItem = getOrAddAccountInDictionary(businessId, accountId)
    if(currentItem.state.locked and currentItem.state.owner != businessId)
    return -1

    currentItem.state.locked = False


if __name__ == "__main__":
    app.run()
