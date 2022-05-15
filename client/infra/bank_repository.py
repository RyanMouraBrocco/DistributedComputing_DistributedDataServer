from shared.http_utils import getFromUrl, isSuccessfulResult, postFromUrl
from settings import bankApiSettings


class BankRepository:
    def __init__(self, authKey):
        self.url = bankApiSettings["Url"]
        self.authenticationHeader = {"auth": authKey}

    def deposit(self, accountId, amount):
        (statusCode, responseObject) = postFromUrl(
            self.url + "deposit/" + str(accountId) + '/' + str(amount), headers=self.authenticationHeader)
        if(not isSuccessfulResult(statusCode)):
            raise Exception("something is wrong, unexpecetd error")
        else:
            return responseObject

    def withdrawal(self, accountId, amount):
        (statusCode, responseObject) = postFromUrl(
            self.url + "withdrawal/" + str(accountId) + '/' + str(amount), headers=self.authenticationHeader)
        if(not isSuccessfulResult(statusCode)):
            raise Exception("something is wrong, unexpecetd error")
        else:
            return responseObject

    def transfer(self, originAccountId, targetAccountId, amount):
        (statusCode, responseObject) = postFromUrl(
            self.url + "transfer/" + str(originAccountId) + '/' + str(targetAccountId) + '/' + str(amount), headers=self.authenticationHeader)
        if(not isSuccessfulResult(statusCode)):
            raise Exception("something is wrong, unexpecetd error")
        else:
            return responseObject

    def getBalance(self, accountId):
        (statusCode, responseObject) = getFromUrl(
            self.url + "balance/" + str(accountId), self.authenticationHeader)
        if(not isSuccessfulResult(statusCode)):
            raise Exception("something is wrong, unexpecetd error")
        else:
            return responseObject
