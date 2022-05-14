from business.infra.http_utils import *
from settings import lockApiSettings, businessId


class LockRepository:

    def __init__(self):
        self.businessId = businessId
        self.url = lockApiSettings["Url"]
        self.authenticationKey = lockApiSettings["AuthenticationKey"]

    def lockAccount(self, accountId):
        (statusCode, responseObject) = postFromUrl(
            self.url + "getLock/"+str(self.businessId)+"/"+str(accountId))
        if(not isSuccessfulResult(statusCode)):
            if(responseObject == -1):
                raise Exception("this item is already locked")
            else:
                raise Exception("something is wrong, unexpected error")

    def unLockAccount(self, accountId):
        (statusCode, responseObject) = postFromUrl(
            self.url + "unLock/"+str(self.businessId)+"/"+str(accountId))
        if(not isSuccessfulResult(statusCode)):
            if(responseObject == -1):
                raise Exception("this item is locked by another business")
            else:
                raise Exception("something is wrong, unexpecetd error")
