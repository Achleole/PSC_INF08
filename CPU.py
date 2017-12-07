import instructions_tierra
#a completer avec le nom du fichier de Pierre et Yueh : import  as fonc

""" CODE Incomplet, a completer 
quand il y aura le code de Pierre et Yueh
instructions_fonctions = 
{
	0: fonc.nop0,
	1: fonc.nop1,
	2: fonc.movdi,
	3: fonc.movid,
	4: fonc.movii,
	5: fonc.pushA,
	6: fonc.pushB,
	7: fonc.pushC,
	8: fonc.pushD,
	9: fonc.popA,
	10: fonc.popB,
	11: fonc.popC,
	12: fonc.popD,
	13: fonc.puticc,
	14: fonc.get,
	15: fonc.inc,
	16: fonc.dec,
	17: fonc.add,
	18: fonc.sub,
	19: fonc.zero,
	20: fonc.shl,
	21: fonc.not0,
	22: fonc.ifz,
	23: fonc.ifZ,
	24: fonc.jmpo,
	25: fonc.jmpb,
	26: fonc.call,
	27: fonc.adro,
	28: fonc.adrb,
	29: fonc.adrf,
	30: fonc.mal,
	#a partir de ce point on definit les nouvelles fonctions
	31: fonc.new,
	32: fonc.read,
	33: fonc.write
}
"""
#l'instruction mal n'existe plus
"""Ce tableau stocke les correspondances entre les
fonctions a appeler et leur code correspondant dans la
memoire.
Il reste a ajouter les nouvelles instructions"""

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
		instructions_fonctions[i](self) #execute la fonction representee 
		#par le code i

	def kill(self):
		"""La fonction kill fait supprimer le CPU de l'univers"""
		self.universe.kill() # ne serait-ce pas plutôt self.universe.killCPU(self) ?

	
