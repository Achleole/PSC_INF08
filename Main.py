import os 
import Univers
import NextSite
from Enregistrement import *
from CPU import *
import Instructions

class Main:

	def test(self):
		print "Nombre de CPUs : ", len(self.U.liste_cpus), 
		print "Numero de l'instruction : ", self.i

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
		self.i = 0
		self.U = Univers.Univers(NextSite.NextSite())
		self.U.insDict.initialize(Instructions.instructions)
		eve = charger_genome('eve')
		ancestor = self.U.insDict.toInts(eve)
		self.U.addIndividual(0, ancestor)
		c = CPU(0, self.U)
		self.U.inserer_cpu(c)
		while self.i < 1000000:
			self.U.cycle()
			self.test()
			self.i += 1
				
Main()