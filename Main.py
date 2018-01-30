import os 
import Univers
from Enregistrement import *
from CPU import *
import Instructions
import CPU
import Statistiques

class Main:

	def test(self):
		print(self.stats.cpus_total[-1], '/', len(self.U.liste_cpus))

	def __init__(self):
		self.U = Univers.Univers()
		self.U.insDict.initialize(Instructions.instructions)
		eve = charger_genome('eve')
		ancestor = self.U.insDict.toInts(eve)
		self.U.addIndividual(0, ancestor)
		self.stats = Statistiques.Statistiques(self.U)
		self.U.inserer_cpu(CPU.CPU(0, self.U))
		for i in range(5000):
			self.U.cycle()
			self.test()

Main()