import http_requester
import settings


def getCurrentAmountValueByAccount(accountId):
    (statusCode, responseObject) = getFromUrl(
        amountApiSettings["Url"] + "getAmount/" + businessId + "/" + accountId)
    if(not isSuccessfulResult(statusCode)):
        if(responseObject == -1):
            raise Exception("this item is locked by another business")
        else:
            raise Exception("something is wrong, unexpecetd error")
    else:
        return responseObject


def setAmountValueByAccount(accountId, amount):
    (statusCode, responseObject) = postFromUrl(
        amountApiSettings["Url"] + "setAmount/" + businessId + "/" + accountId + "/" + amount)
    if(not isSuccessfulResult(statusCode)):
        if(responseObject == -1):
            raise Exception("this item is locked by another business")
        else:
            raise Exception("something is wrong, unexpecetd error")
