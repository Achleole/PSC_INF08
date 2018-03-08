import os 
import Univers
import NextSite
from Enregistrement import *
from CPU import *
import Instructions
import CPU
import Statistiques
import NextSite

import matplotlib.pyplot as plt
import numpy as np

class Main:

	def test(self):
		return self.stats.historique_generations

	def afficher_statistiques(self):
		T = len(self.stats.cpus_total)

		abscisse = np.linspace(1, T, T)
		ordonee  = self.stats.cpus_total

		plt.plot(abscisse, ordonee)
		plt.show()

	def lister_codes(self):
		liste_codes = []
		code_actuel = []
		for c in self.U.memoire:
			if c != 2:
				code_actuel.append(c)
			elif code_actuel != []:
				liste_codes.append(code_actuel)
				print(code_actuel)
				code_actuel = []

	def run(self):
		while self.i < 4000:
			self.U.cycle()
			self.i += 1
		return self.test()

	def __init__(self, m):
		self.i = 0

		nextSite = NextSite.NextSite()
		self.U = Univers.Univers(nextSite)
		self.U.mutation = m
		self.stats = Statistiques.Statistiques(self.U)
		self.U.insDict.initialize(Instructions.instructions)
		eve = charger_genome('eve')
		ancestor = self.U.insDict.toInts(eve)
		self.U.addIndividual(0, ancestor)
		c = CPU.CPU(0, self.U)
		c.generation = 1
		self.U.inserer_cpu(c)
		

main = Main(0.01)
main.run()
print(main.test())