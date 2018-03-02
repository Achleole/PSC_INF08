import os 
import Univers
import NextSite
from Enregistrement import *
from CPU import *
import Instructions
import CPU
import Statistiques
import NextSite

class Main:

	def test(self):
		print(len(self.U.liste_cpus))

	def __init__(self):
		self.i = 0

		nextSite = NextSite.NextSite()
		self.U = Univers.Univers(nextSite)
		self.stats = Statistiques.Statistiques(self.U)
		self.U.insDict.initialize(Instructions.instructions)
		eve = charger_genome('eve')
		ancestor = self.U.insDict.toInts(eve)
		self.U.addIndividual(0, ancestor)
		c = CPU.CPU(0, self.U)
		self.U.inserer_cpu(c)
		while self.i < 1000000:
			self.U.cycle()
			self.test()
			self.i += 1
Main()