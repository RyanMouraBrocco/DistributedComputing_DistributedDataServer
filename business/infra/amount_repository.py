from infra.http_utils import getFromUrl, isSuccessfulResult, postFromUrl
from settings import amountApiSettings, businessId


class AmountRepository:

    def __init__(self):
        self.businessId = businessId
        self.url = amountApiSettings["Url"]
        self.authenticationHeader = {
            "auth": amountApiSettings["AuthenticationKey"]}

    def getCurrentAmountValueByAccount(self, accountId):
        (statusCode, responseObject) = getFromUrl(
            self.url + "getAmount/" + str(self.businessId) + "/" + str(accountId), self.authenticationHeader)
        if(not isSuccessfulResult(statusCode)):
            if(responseObject == -1):
                raise Exception("this item is locked by another business")
            else:
                raise Exception("something is wrong, unexpecetd error")
        else:
            return responseObject

    def setAmountValueByAccount(self, accountId, amount):
        (statusCode, responseObject) = postFromUrl(
            self.url + "setAmount/" + str(self.businessId) + "/" + str(accountId) + "/" + str(amount), headers=self.authenticationHeader)
        if(not isSuccessfulResult(statusCode)):
            if(responseObject == -1):
                raise Exception("this item is locked by another business")
            else:
                raise Exception("something is wrong, unexpecetd error")
