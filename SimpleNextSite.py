DELTA_SITE = 43 #entre l'instruction rand et la fin du genome : 43 instructions

import NextSite

class SimpleNextSite:
	def __init__(self, memLen):
		self.setMemSize(memLen)

	def setMemSize(self, memLen):
		self.memLen = memLen

	def getNext(s, cpu=None):
		if cpu.ptr >= cpu.univers.TAILLE_MEMOIRE - DELTA_SITE or cpu.ptr < -DELTA_SITE :
			return cpu.univers.ind(cpu.ptr + DELTA_SITE)
		else:
			return cpu.ptr + DELTA_SITE