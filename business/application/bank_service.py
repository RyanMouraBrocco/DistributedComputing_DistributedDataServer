from infra.lock_repository import LockRepository
from infra.amount_repository import AmountRepository
from shared.log_repository import LogRepository


class BankService:

    def __init__(self):
        self.amountRepository = AmountRepository()
        self.lockRepository = LockRepository()
        self.logRepository = LogRepository()

    def log(self, logName, accountId, targetAccountId=None, amount=None):
        amountString = str(amount) if amount != None else 'NULL'
        targetAccountIdString = str(
            targetAccountId) if targetAccountId != None else 'NULL'
        self.logRepository.log(
            logName + ',' + str(accountId) + ',' + targetAccountIdString + ',' + amountString)

    def deposit(self, accountId, amount):
        if(amount < 0):
            raise Exception("amount is not valid")

        currentAmout = self.amountRepository.getCurrentAmountValueByAccount(
            accountId)
        currentAmout += amount
        self.amountRepository.setAmountValueByAccount(accountId, currentAmout)

    def depositWithLock(self, accountId, amount):
        try:
            self.lockRepository.lockAccount(accountId)
            self.deposit(accountId, amount)
            self.log('deposit', accountId, amount=amount)
        except:
            raise
        finally:
            self.lockRepository.unLockAccount(accountId)

    def withdrawal(self, accountId, amount):
        if(amount < 0):
            raise Exception("amount is not valid")

        currentAmout = self.amountRepository.getCurrentAmountValueByAccount(
            accountId)
        if(currentAmout >= amount):
            currentAmout -= amount
            self.amountRepository.setAmountValueByAccount(
                accountId, currentAmout)
        else:
            raise Exception('not enough balance')

    def withdrawalWithLock(self, accountId, amount):
        try:
            self.lockRepository.lockAccount(accountId)
            self.withdrawal(accountId, amount)
            self.log('withdrawal', accountId, amount=amount)
        except:
            raise
        finally:
            self.lockRepository.unLockAccount(accountId)

    def getBalance(self, accountId):
        self.log('getBalance', accountId)
        return self.amountRepository.getCurrentAmountValueByAccount(accountId)

    def transfer(self, originAccountId, targetAccountId, amount):
        try:
            self.lockRepository.lockAccount(originAccountId)
            self.lockRepository.lockAccount(targetAccountId)
            self.withdrawal(originAccountId, amount)
            self.deposit(targetAccountId, amount)
            self.log('transfer', originAccountId,
                     targetAccountId, amount)
        except:
            raise
        finally:
            self.lockRepository.unLockAccount(originAccountId)
            self.lockRepository.unLockAccount(targetAccountId)
