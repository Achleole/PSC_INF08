import os 
import Univers
from Enregistrement import *
from CPU import *
import Instructions

class Main:

	def test(self):
		print(self.U.memoire[:10])
		for i in range(len(self.U.liste_cpus)):
			print("Pointeur du CPU numero ", i, '=', self.U.liste_cpus[i].ptr)
			print("Valeur de ax du NPU numero", i, '=', self.U.liste_cpus[i].ax)
		print(' ')
		print(' NB DE CPU :', len(self.U.liste_cpus))

	def init2(self):
		i = 0
		self.U = Univers.Univers()
		self.U.inserer_cpu(0) #initialiste un CPU au debut de l'univers
		compteur=0
		fichier="C:/Users/migli/Desktop/temporary.txt"
		while True:	
			self.U.executer_cpus()
			self.test()
			if compteur==100:
				s = input()
				compteur=0
			else:
				compteur+=1
				s=' '
			if s == "q":
				quit()
			if s == "s":
				photo(self.U,fichier)
			if s == "l":
				loadPhoto(self.U,fichier)
				
				
				
	def __init__(self):
	
		self.U = Univers.Univers()
		self.U.insDict.initialize(Instructions.instructions)
		eve = charger_genome('eve')
		ancestor = self.U.insDict.toInts(eve)
		self.U.addIndividual(0, ancestor)
		self.U.inserer_cpu(0)
		for i in range(1000) :
			self.U.executer_cpus()
			self.test()
				
Main()