import instructions

class CPU:
	def __init__(self, universe, adr):
		""" Initialise les registres a 0"""
		self.ax = self.bx = self.cx = self.dx = 0
		self.universe = universe #Pointeur vers l'univers qui vient de le creer
		self.adr = adr #adr designe l'adresse couramment lue par le CPU
		self.stack = []

	def execute(self):
		instruction = self.univers.memoire[ptr]
		instructions.execute(instruction, self) #On fait l'hypothese que dans le fichier
		#instructions, il y a une fonction execute qui prend en argument le CPU et
		#l'instruction et execute la fonction de cette derniere.

	def kill(self):
		"""La fonction kill fait supprimer le CPU de l'univers"""
		self.univers.kill()

	