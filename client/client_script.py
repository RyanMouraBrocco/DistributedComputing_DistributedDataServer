import threading
from infra.bank_repository import BankRepository
from settings import bankApiSettings

clientAuthKey = bankApiSettings["AuthenticationKey"]


def printTestResult(test, accountId, succeessfulMessage):
    try:
        test(accountId)
        print(succeessfulMessage)
    except Exception as e:
        print(str(e))


def tryRequestWithoutAuthenticaiton(accountId):
    bankRepository = BankRepository(url, "")
    try:
        bankRepository.deposit(accountId, 10)
    except:
        return

    raise Exception('[fail]: access api without authentication')


def checkIfOnlyIn5ActionSaveInformations(accountId):
    bankRepository = BankRepository(url, clientAuthKey)
    initialAmount = bankRepository.getBalance(accountId)
    for i in range(5):
        bankRepository.deposit(accountId, 10)
        currentAmout = bankRepository.getBalance(accountId)
        if(i != 4 and currentAmout != initialAmount):
            raise Exception(
                '[fail]: in less than 5 actions the values was changed')
        elif(i == 4 and currentAmout != initialAmount + 50):
            raise Exception(
                '[fail]: the value returned is not expected in 5 action')


def checkDeposits(accountId):
    bankRepository = BankRepository(url, clientAuthKey)
    initialAmount = bankRepository.getBalance(accountId)
    for i in range(5):
        bankRepository.deposit(accountId, 10)

    currentAmout = bankRepository.getBalance(accountId)
    if(currentAmout != initialAmount + 50):
        raise Exception(
            '[fail]: deposit not working')


def checkWithdrawal(accountId):
    bankRepository = BankRepository(url, clientAuthKey)
    bankRepository.deposit(accountId, 40)
    initialAmount = bankRepository.getBalance(accountId)
    for i in range(4):
        bankRepository.withdrawal(accountId, 10)

    currentAmount = bankRepository.getBalance(accountId)
    if(currentAmount != initialAmount - 40):
        raise Exception(
            '[fail]: withdrawal not working')


def checkWithdrawal(accountId):
    bankRepository = BankRepository(url, clientAuthKey)
    initialAmount = bankRepository.getBalance(accountId)
    bankRepository.deposit(accountId, 40)
    for i in range(4):
        bankRepository.withdrawal(accountId, 10)

    currentAmount = bankRepository.getBalance(accountId)
    if(currentAmount != initialAmount):
        raise Exception(
            '[fail]: withdrawal not working')


def checkInvalidWithdrawal(accountId):
    bankRepository = BankRepository(url, clientAuthKey)
    initialAmount = bankRepository.getBalance(accountId)
    for i in range(5):
        bankRepository.withdrawal(accountId, int(initialAmount + 1))

    currentAmount = bankRepository.getBalance(accountId)
    if(currentAmount != initialAmount or currentAmount < 0):
        raise Exception(
            '[fail]: withdrawal more than possible')


def checkTransfer(accountId):
    bankRepository = BankRepository(url, clientAuthKey)
    initialAmountOrigin = bankRepository.getBalance(accountId)
    initialAmountTarget = bankRepository.getBalance(accountId + 1)
    bankRepository.deposit(accountId, 40)

    for i in range(4):
        bankRepository.transfer(accountId, accountId + 1, 10)

    currentAmountOrigin = bankRepository.getBalance(accountId)
    currentAmountTarget = bankRepository.getBalance(accountId + 1)

    if(initialAmountOrigin != currentAmountOrigin or initialAmountTarget + 40 != currentAmountTarget):
        raise Exception(
            '[fail]: transfer not working')


def tryToTransferMoreThanOriginHad(accountId):
    bankRepository = BankRepository(url, clientAuthKey)
    initialAmountOrigin = bankRepository.getBalance(accountId)
    initialAmountTarget = bankRepository.getBalance(accountId + 1)
    for i in range(5):
        bankRepository.transfer(accountId, accountId +
                                1, int(initialAmountOrigin + 1))

    currentAmountOrigin = bankRepository.getBalance(accountId)
    currentAmountTarget = bankRepository.getBalance(accountId + 1)

    if(initialAmountOrigin != currentAmountOrigin or initialAmountTarget != currentAmountTarget):
        raise Exception(
            '[fail]: unexpect transfer')


semaphore = threading.Semaphore(100)


def concurrentRequests(accountId):
    bankRepository = BankRepository(url, clientAuthKey)
    initialAmout = bankRepository.getBalance(accountId)

    for i in range(500):
        operationsThatNotChangeTheFinalAmount(accountId)

    currentAmount = bankRepository.getBalance(accountId)
    if(initialAmout != currentAmount):
        raise Exception('[fail]: some parallel operation didnt work')


def operationsThatNotChangeTheFinalAmount(accountId):
    bankRepository = BankRepository(url, clientAuthKey)
    bankRepository.deposit(accountId, 200)
    bankRepository.withdrawal(accountId, 100)
    bankRepository.deposit(accountId, 50)
    bankRepository.withdrawal(accountId, 50)
    bankRepository.transfer(accountId, accountId + 1, 100)


print('select the type, type 1 func test, type 2 cocurrent test')
type = int(input())

print('write the accountid')
accountId = int(input())

print('write url')
url = input()



if type == 1:
    # auth test
    printTestResult(tryRequestWithoutAuthenticaiton,
                    accountId, '[success]: authentication is necessary')

    # operations test

    printTestResult(checkIfOnlyIn5ActionSaveInformations, accountId,
                    '[success]: in check if only in 5 action the business api would save the information')
    printTestResult(checkDeposits, accountId, '[success]: deposit works')
    printTestResult(checkWithdrawal, accountId, '[success]: withdrawal works')
    printTestResult(checkInvalidWithdrawal, accountId,
                    '[success]: limit in withdrawal works')
    printTestResult(checkTransfer, accountId, '[success]: transfer works')
    printTestResult(tryToTransferMoreThanOriginHad, accountId,
                    '[success]: not transfer if origin not have enough amount')
elif type == 2:
    # concurrency test
    printTestResult(concurrentRequests, accountId,
                    '[success]: concurrent test is ok')
else:
    print('invalid type')
