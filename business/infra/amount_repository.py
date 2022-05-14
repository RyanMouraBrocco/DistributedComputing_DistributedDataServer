from business.infra.http_utils import *
from settings import amountApiSettings, businessId


class AmountRepository:

    def __init__(self):
        self.businessId = businessId
        self.url = amountApiSettings["Url"]
        self.authenticationKey = amountApiSettings["AuthenticationKey"]

    def getCurrentAmountValueByAccount(self, accountId):
        (statusCode, responseObject) = getFromUrl(
            self.url + "getAmount/" + self.businessId + "/" + accountId)
        if(not isSuccessfulResult(statusCode)):
            if(responseObject == -1):
                raise Exception("this item is locked by another business")
            else:
                raise Exception("something is wrong, unexpecetd error")
        else:
            return responseObject

    def setAmountValueByAccount(self, accountId, amount):
        (statusCode, responseObject) = postFromUrl(
            self.url + "setAmount/" + self.businessId + "/" + accountId + "/" + amount)
        if(not isSuccessfulResult(statusCode)):
            if(responseObject == -1):
                raise Exception("this item is locked by another business")
            else:
                raise Exception("something is wrong, unexpecetd error")
