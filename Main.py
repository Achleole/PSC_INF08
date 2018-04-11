import os 
import Univers
import NextSite
from CPU import *
import Instructions
import CPU
import Statistiques
import NextSite
import Enregistrement
import Experiment

class Main:

	def test(self):
		print(len(self.U.liste_cpus))

	def __initancien__(self):
		nextSite = NextSite.NextSite()
		self.U = Univers.Univers(nextSite)
		self.stats = Statistiques.Statistiques(self.U)
		self.U.insDict.initialize(Instructions.instructions)
		eve = charger_genome('eve')
		ancestor = self.U.insDict.toInts(eve)
		self.U.addIndividual(0, ancestor)
		c = CPU.CPU(0, self.U)
		self.U.inserer_cpu(c)
		self.replay = Enregistrement.Replay()
		self.replay.univers = self.U
		nom = "Enregs/enreg"
		print(ancestor)
		for i in range(100):
			self.replay.openWrite(nom+str(i))
			self.replay.runAndSave(5000)
			self.test()

	def __init__(selfself):
		exp = Experiment.Experiment()
		exp.experiment1(TAILLE_MEMOIRE=[10000, 20000])
Main()