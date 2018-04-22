import random

class NextSite:
    def __init__(self, memLen=50000):
        self.memLen = memLen

    def setMemSize(self, memLen):
        self.memLen = memLen

    def getNext(s, cpu=None):
        return random.randint(0, s.memLen-1)