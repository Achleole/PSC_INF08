class NextSiteTest:
    def __init__(self, memLen=50000, interval=50, lastSpot=0):
        self.interval = interval
        self.lastSpot = lastSpot
        self.memLen = memLen

    def getNext(s):
        s.lastSpot = (s.lastSpot + s.interval) % s.memLen
        return s.lastSpot