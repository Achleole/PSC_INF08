from CPU import *
from Enregistrement import *

TAILLE_MEMOIRE = 500
LARGEUR_DENSITE = 0

class Univers:
	"Contient les CPU et le monde i.e les instructions a executer"
	cpu_actuel 	   = 0
	#valeurs non contractuelles.
	b1=2 #nb bytes du nb de CPU et du numero du CPU considere actuellement.(limite leur nombre)
	n1=5 #nb bit d'un CPU
	b2=2 #nb bytes du nb de case memoire.(limite leur nombre)
	n2=6 #nb bit d'une case memoire
	
	def __init__(s):
		#code temporaire
		eve 					= charger_genome('eve')
		s.memoire 				= eve + [None]*(TAILLE_MEMOIRE-len(eve))
		s.liste_cpus 			= []
		s.localisation_cpus 	= {} #Cette variable associe a chaque indice, la liste des cpus qui sont 
		#en train de la litre 
		s.mutation				= 0 #Valeur temporaire

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
		cpu.die()

	def tuer_cpu_actuel(s):
		s.cpu_actuel.die()

	def enlever_cpu(s, cpu):
		"Ne pas APPELER DIRECTEMENT CETTE fonction dans le code ! Appeler plutot la fonction\
		 tuer CPU, car enlever_cpu de fait que l'enlever de la liste des cpus. Losqu'un CPU meurt\
		 il faut aussi qu'il soit enleve de la liste localisation_cpu"
		s.liste_cpus.remove(cpu)

	def enlever_cpu_actuel(s):
		liste.pop(s.cpu_actuel)

	def next_cpu(s):
		"Met a jour cpu_actuel pour pointer le suivant a executer"
		s.cpu_actuel = (s.cpu_actuel - 1) % len(s.liste_cpus)

	def inserer_cpu(s, ptr):
		"Insere un nouveau CPU dans la liste juste apres celui actuellement pointe"
		s.liste_cpus.insert(s.cpu_actuel+1, CPU(ptr, s))
	
	def ajouter_genome_memoire(self, index, indiv):
		"Place l'individu (sous forme de liste d'instructions)\
		dans la memoire a partir de l'indice index"
		for i in range(len(indiv)) :
			self.memory[index + i % l] = indiv[i]

	def calculer_densite_cpus(self, ptr):
		"Calcule le nombre de cpus par case dans les 2*LARGEUR_DENSITE cases alentours"
		total = 0
		for i in range(ptr-LARGEUR_DENSITE, ptr+LARGEUR_DENSITE+1):
			if(self.localisation_cpus.has_key(i)):
				total += len(self.localisation_cpus[i])
		return total/(float(2*LARGEUR_DENSITE + 1))

	def tuer_cpus_par_densite(self):
		"On va tuer tous les CPUS en meme temps pour pas donner\
		d'avantage a certains CPUs"
		pass #TODO
