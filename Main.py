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

	def __init__(selfself):
		exp = Experiment.Experiment(mut=0.001, insSet=1)
		exp.setLargeurCalculDensite(23)
		exp.setFolderName("experiences_18_mai")
		exp.experiment2([10000], 1, 1000000)
Main()
