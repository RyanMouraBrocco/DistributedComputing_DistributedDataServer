from business.infra.lock_repository import LockRepository
from business.infra.amount_repository import AmountRepository
from business.presentation.business_server import deposit, withdrawal


class BankService:

    def __init__(self):
        self.amountRepository = AmountRepository()
        self.lockRepository = LockRepository()

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
            deposit(accountId, amount)
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
            withdrawal(accountId, amount)
        except:
            raise
        finally:
            self.lockRepository.unLockAccount(accountId)

    def getBalance(self, accountId):
        return self.amountRepository.getCurrentAmountValueByAccount(accountId)

    def transfer(self, originAccountId, targetAccountId, amount):
        try:
            self.lockRepository.lockAccount(originAccountId)
            self.lockRepository.lockAccount(targetAccountId)
            withdrawal(originAccountId, amount)
            deposit(targetAccountId, amount)
        except:
            raise
        finally:
            self.lockRepository.unLockAccount(originAccountId)
            self.lockRepository.unLockAccount(targetAccountId)
