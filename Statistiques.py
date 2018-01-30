"""
Classe servant a faire les stats sur l'univers et les CPUs
A ne pas utiliser pour l'instant (pas fonctionnel)
"""

class Statistique:
	def __init__(self, U):
		"Chaque instance va etre reliee a un Univers"
		self.univers 	= U
		self.cpus_crees = [] #Enregistre le nombre de cpus crees a chaque iteration 

	def mettre_a_jour(self):
		"A appeler apres chaque cycle du CPUs"
		self.recuperer_cpus_crees()

	def recuperer_cpus_crees(self):
		self.cpus_crees.append(self.univers.cpus_crees()) #A IMPLEMENTER DANS LA CLASSE UNIVERS : self.univers.cpus_crees() pour 
		#renvoyer le nombre de cpus qui ont etes crees durant le cycle passe
	