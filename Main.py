import os 
import Univers
from CPU import *

class Main:

	def test(self):
		for i in range(len(self.U.liste_cpus)):
			print("Pointeur du CPU numero ", i, '=', self.U.liste_cpus[i].ptr)
			print("Valeur de ax du NPU numero", i, '=', self.U.liste_cpus[i].ax)
		print(' ')
		print(' NB DE CPU :', len(self.U.liste_cpus))

	def __init__(self):
		i = 0
		self.U = Univers.Univers()
		self.U.inserer_cpu(0) #initialiste un CPU au debut de l'univers
		while True:	
			os.system('clear')
			self.U.executer_cpus()
			self.test()
			s = raw_input()
			if s == "q":
				break
			if s == "d":
				print(self.U.memoire[0:10])
				print(self.U.memoire[47:51])
				raw_input()

Main()