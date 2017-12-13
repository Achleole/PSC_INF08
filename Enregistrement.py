def charger_genome(fichier):
	genome = []
	"Renvoie sous forme de tableau de strings le genome specifie dans le fichier"
	f = open(fichier, 'r')
	for line in f:
		genome.append(line.strip())
	return genome
