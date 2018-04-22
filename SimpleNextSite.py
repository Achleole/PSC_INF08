DELTA_SITE = 43 #entre l'instruction rand et la fin du genome : 43 instructions

import NextSite

class SimpleNextSite:
	def __init__(self, memLen):
		self.setMemSize(memLen)

	def setMemSize(self, memLen):
		self.memLen = memLen

	def getNext(s, cpu=None):
		return cpu.ptr + DELTA_SITE