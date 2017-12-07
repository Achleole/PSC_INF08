import instructions_tierra.py
import instructions_tierra as fonc

instructions_fonctions = 
{
	0: fonc.ifz,
	1: fonc.jmp,
	2: fonc.jmpb,
	3: fonc.call,
	4: fonc.ret,
	5: fonc.adrf,
	6: fonc.adrb,
	7: fonc.new,
	8: fonc.read,
	9: fonc.write,
	10: fonc.nop0,
	11: fonc.nop1,
	12: fonc.pushA,
	13: fonc.pushB,
	14: fonc.pushC,
	15: fonc.pushD,
	16: fonc.popA,
	17: fonc.popB,
	18: fonc.popC,
	19: fonc.popD,
	20: fonc.movCD,
	21: fonc.movAB,
	22: fonc.movii,
	23: fonc.subCAB,
	24: fonc.subAAC,
	25: fonc.incA,
	26: fonc.incB,
	27: fonc.incC,
	28: fonc.incD,
	29: fonc.decC,
	30: fonc.zero,
	31: fonc.not0,
	32: fonc.shl,
	33: fonc.rand
}

class CPU:
	def __init__(self, universe, index):
		""" Initialise les registres a 0"""
		self.ax = self.bx = self.cx = self.dx = 0
		self.universe = universe #Pointeur vers l'univers qui vient de le creer
		self.index = index #index designe l'adresse couramment lue par le CPU
		self.stack = []

	def execute(self):
		"""execute l'instruction actuellement pointee par le CPU"""
		i = self.universe.memoire[self.index]
		try:
			instructions_fonctions[i](self) #execute la fonction representee 
		#par le code i
		except:
			print("Probleme d'execution de l'instruction")

	def kill(self):
		"""La fonction kill fait supprimer le CPU de l'univers"""
		self.universe.kill() # ne serait-ce pas plutôt self.universe.killCPU(self) ?

	
