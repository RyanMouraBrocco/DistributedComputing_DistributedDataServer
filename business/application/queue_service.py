from queue import Queue

class QueueMessageServer:
    def __init__(self):
        self.queue = Queue(maxsize=10)

    def enqueue(self, action, *actionParameters):
        self.queue.put({"method": action, "parameters": actionParameters})

    def executeWhenNeeded(self):
        if(self.queue.qsize() >= 5):
            for i in range(0, 5):
                nextAction = self.queue.get()
                nextAction['action'](nextAction['parameters'])
