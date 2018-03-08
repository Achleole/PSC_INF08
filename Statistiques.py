"""
Classe servant a faire les stats sur l'univers et les CPUs
A ne pas utiliser pour l'instant (pas fonctionnel)
"""

from math import log

class Statistiques:
	def __init__(self, U):
		"Chaque instance va etre reliee a un Univers"
		self.univers 	= U
		U.set_statistiques(self)
		self.cpus_crees = [] #Enregistre le nombre de cpus crees a chaque iteration
		self.cpus_total = []
		self.historique_generations=[[],[]]
	
	def mettre_a_jour(self):
		#A appeler apres chaque cycle du CPUs
		self.recuperer_cpus_crees()
		self.recuperer_cpus_total()
		self.mettre_ajout_historique_gen_mut()

	def mettre_ajout_historique_gen_mut(self):
		"""
		Le tableau historique_generations[0 ou 1] contient la liste de cpus dans toute l'histoire 
		pour chaque generation
		"""
		tmp = self.univers.retourner_historique_gen_mut()
		conversion = {False: 0, True: 1}
		for gen, mut in tmp:
			i = conversion[mut] 
			while len(self.historique_generations[mut]) < gen:
				self.historique_generations[mut].append(0)
			self.historique_generations[mut][gen-1] += 1

	
	def recuperer_cpus_total(self):
		self.cpus_total.append(self.univers.retourner_cpus_total())
	
	def recuperer_cpus_crees(self):
		self.cpus_crees.append(self.univers.retourner_cpus_crees())

	def calculer_entropie(self):
		"Calcule l'entropie S des instructions de l'Univers"
		S = 0
		memoire = self.univers.retourner_copie_memoire()
		occurences = {}
		for x in memoire:
			if x in occurences:
				occurences[x] += 1
			else:
				occurences = 1
		for x in occurences:
			proba = float(occurences[x])/len(memoire)
			S += proba*log(proba)
		return S
		
