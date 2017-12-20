from CPU import *
from Enregistrement import *


class Univers:
	"Contient les CPU et le monde i.e les instructions a executer"
	cpu_actuel 	   = 0
	#valeurs non contractuelles.
	b1=2 #nb bytes du nb de CPU et du numero du CPU considere actuellement.(limite leur nombre)
	n1=5 #nb bit d'un CPU
	b2=2 #nb bytes du nb de case memoire.(limite leur nombre)
	n2=6 #nb bit d'une case memoire
	TAILLE_MEMOIRE = 500
	def __init__(s):
		#code temporaire
		eve = charger_genome('eve')
		#s.memoire = eve + [None]*(TAILLE_MEMOIRE-len(eve))
		s.memoire= [2]*s.TAILLE_MEMOIRE
		s.liste_cpus 	= []

	def executer_cpus(s):
		"Cette fonction execute tous les CPU 1 fois\
		PRECISION IMPORTANTE : on parcourt la liste dans l'ordre des indices decroissant"
		cpu_depart = (s.cpu_actuel) #Contient le cpu auquel on devra s'arreter
		s.executer_cpu(s.cpu_actuel)
		s.next_cpu()
		while s.cpu_actuel != cpu_depart:
			s.executer_cpu(s.cpu_actuel)
			s.next_cpu()

	def executer_cpu(s, cpu): 
		"Execute le CPU actuellement pointe SANS PASSER AU SUIVANT\
		i.e sans incrementer cpu_actuel"
		s.liste_cpus[cpu].execute()


	def tuer_cpu(s, cpu):
		s.liste_cpus.remove(cpu)

	def tuer_cpu_actuel(s):
		liste.pop(s.cpu_actuel)

	def next_cpu(s):
		"Met a jour cpu_actuel pour pointer le suivant a executer"
		s.cpu_actuel = (s.cpu_actuel - 1) % len(s.liste_cpus)

	def inserer_cpu(s, ptr):
		"Insere un nouveau CPU dans la liste juste apres celui actuellement pointe"
		s.liste_cpus.insert(s.cpu_actuel+1, CPU(ptr, s))
	
	def addIndividual(self, index, indiv) :
		for i in range(len(indiv)) :
			self.memory[index + i % l] = indiv[i]
