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

import InstructionsSuperrwshll


class Main:

	def __init__(self):
		pass

	def run_test_validite_eve(self):
		exp = Experiment.Experiment()
		exp.setFolderName("experiences_18_mai")
		exp.setLargeurCalculDensite(100)
		TM = [20000]
		for t in TM:
			print('TAILLE MEMOIRE : ', t)
			exp.experiment_comparaison_genomes(TAILLE_MEMOIRE=t, NOMBRE_ITERATIONS=50000)

m = Main()
m.run_test_validite_eve()