import datetime
from threading import Lock


class LogRepository():

    def __init__(self):
        self.fileName = 'log.txt'
        self.lock = Lock()
        self.operation = 1

    def log(self, message):
        self.lock.acquire()

        try:
            with open(self.fileName, "a") as file:
                file.write(self.getBaseLogsInfos(self) + message)
            self.operation += 1
        except:
            print('Error to save log')
        finally:
            self.lock.release()

    def getBaseLogsInfos(self):
        return str(datetime.timestamp(datetime.now())) + ',' + str(self.operation) + ','
