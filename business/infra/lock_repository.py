from shared.http_utils import isSuccessfulResult, postFromUrl
from settings import lockApiSettings, businessId


class LockRepository:

    def __init__(self):
        self.businessId = businessId
        self.url = lockApiSettings["Url"]
        self.authenticationHeader = {
            "auth": lockApiSettings["AuthenticationKey"]}

    def lockAccount(self, accountId):
        (statusCode, responseObject) = postFromUrl(
            self.url + "getLock/"+str(self.businessId)+"/"+str(accountId), headers=self.authenticationHeader)
        if(not isSuccessfulResult(statusCode)):
            if(responseObject == -1):
                raise Exception("this item is already locked")
            else:
                raise Exception("something is wrong, unexpected error")

    def unLockAccount(self, accountId):
        (statusCode, responseObject) = postFromUrl(
            self.url + "unLock/"+str(self.businessId)+"/"+str(accountId), headers=self.authenticationHeader)
        if(not isSuccessfulResult(statusCode)):
            if(responseObject == -1):
                raise Exception("this item is locked by another business")
            else:
                raise Exception("something is wrong, unexpecetd error")
