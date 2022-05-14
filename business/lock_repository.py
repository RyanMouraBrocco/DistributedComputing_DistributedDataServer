import http_requester
import settings


def lockAccount(accountId):
    (statusCode, responseObject) = postFromUrl(
        lockApiSettings["Url"] + "getLock/"+str(businessId)+"/"+str(accountId))
    if(not isSuccessfulResult(statusCode)):
        if(responseObject == -1):
            raise Exception("this item is already locked")
        else:
            raise Exception("something is wrong, unexpected error")


def unLockAccount(accountId):
    (statusCode, responseObject) = postFromUrl(
        lockApiSettings["Url"] + "unLock/"+str(businessId)+"/"+str(accountId))
    if(not isSuccessfulResult(statusCode)):
        if(responseObject == -1):
            raise Exception("this item is locked by another business")
        else:
            raise Exception("something is wrong, unexpecetd error")
