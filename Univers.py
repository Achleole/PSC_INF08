from CPU import *
from Enregistrement import *
from math import *


TAILLE_MEMOIRE = 500
TAUX_MUTATION  = 0

class Univers:
	"Contient les CPU et le monde i.e les instructions a executer"
	#valeurs non contractuelles.
	b1=2 #nb bytes du nb de CPU et du numero du CPU considere actuellement.(limite leur nombre)
	b2=2 #nb bytes du nb de case memoire.(limite leur nombre)
	n2=6 #nb bit d'une case memoire
	n1=4*n2+n2+CPU.TAILLE_STACK*n2+ceil(log(CPU.TAILLE_STACK,2)) #nb bit d'un CPU
	TAILLE_MEMOIRE = 500
	def __init__(s):
		#code temporaire
		s.mutation 				   = TAUX_MUTATION #definit le taux de mutation de l'univers
		s.indice_cpu_actuel 	   = 0
		s.cpu_actuel 			   = None
	
		eve = charger_genome('eve')
		s.localisation_cpus = {}
		s.memoire 			= eve + [None]*(TAILLE_MEMOIRE-len(eve))
		s.liste_cpus 		= []

	def executer_cpus(s):
		"Cette fonction execute tous les CPU 1 fois\
		PRECISION IMPORTANTE : on parcourt la liste dans l'ordre des indices decroissant"
		indice_cpu_depart = (s.indice_cpu_actuel) #Contient le cpu auquel on devra s'arreter
		s.cpu_actuel 	  = s.liste_cpus[s.indice_cpu_actuel]
		s.executer_cpu(s.cpu_actuel)
		s.next_cpu()
		while s.indice_cpu_actuel != indice_cpu_depart:
			s.executer_cpu(s.cpu_actuel)
			s.next_cpu()

	def executer_cpu(s, cpu): 
		"Execute le CPU actuellement pointe SANS PASSER AU SUIVANT\
		i.e sans incrementer cpu_actuel"
			s.supprimer_cpu_localisation(s.cpu_actuel)
		cpu.execute()
		s.ajouter_cpu_localisation(s.cpu_actuel)

	def supprimer_cpu_localisation(s, cpu):
		"Prend en argument le pointeur vers un cpu et l'enleve du tableau localisation_cpus"
		try:
			s.localisation_cpus[cpu.ptr].remove(cpu)
		except Exception as e:
			print("Erreur de suppression de localisation !")
			print(e)
		if s.localisation_cpus[cpu.ptr] == []:
			del s.localisation_cpus[cpu.ptr]

	def ajouter_cpu_localisation(s, cpu):
		if not cpu.ptr in s.localisation_cpus:
			s.localisation_cpus[cpu.ptr] = []
		if not cpu in s.localisation_cpus[cpu.ptr]:
			s.localisation_cpus[cpu.ptr].append(cpu)

	def tuer_cpu(s, cpu):
		s.liste_cpus.remove(cpu)

	def tuer_cpu_actuel(s):
		liste.pop(s.cpu_actuel)

	def next_cpu(s):
		"Met a jour cpu_actuel pour pointer le suivant a executer"
		s.indice_cpu_actuel = (s.indice_cpu_actuel - 1)%(len(s.liste_cpus))
		s.cpu_actuel 		= s.liste_cpus[s.indice_cpu_actuel]

	def inserer_cpu(s, ptr):
		"Insere un nouveau CPU dans la liste juste apres celui actuellement pointe"
		nouveau_cpu = CPU(ptr, s)
		s.liste_cpus.insert(s.indice_cpu_actuel+1, nouveau_cpu)
		s.ajouter_cpu_localisation(nouveau_cpu)
	
	def addIndividual(self, index, indiv) :
		for i in range(len(indiv)) :
			self.memory[index + i % l] = indiv[i]
