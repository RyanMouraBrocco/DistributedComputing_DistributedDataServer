from queue import Queue


class QueueMessageServer:
    def __init__(self):
        self.queue = Queue(maxsize=10)

    def enqueue(self, action, *actionParameters):
        self.queue.put({"method": action, "parameters": actionParameters})

    def executeWhenNeeded(self):
        while(self.queue.qsize() >= 5):
            for i in range(0, 5):
                self.runNextAction()

    def runNextAction(self):
        tryAgain = True
        nextAction = self.queue.get()
        while tryAgain:
            try:
                parameters = nextAction['parameters']
                parametersLen = len(parameters)
                if(parametersLen == 1):
                    nextAction['method'](parametersLen[0])
                elif(parametersLen == 2):
                    nextAction['method'](parameters[0], parameters[1])
                elif(parametersLen == 3):
                    nextAction['method'](
                        parameters[0], parameters[1], parameters[2])
                else:
                    nextAction['method'](parameters)

                tryAgain = False
            except Exception as e:
                if('is locked' not in str(e)):
                    tryAgain = False
