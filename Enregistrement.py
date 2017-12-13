import math
def charger_genome(fichier):
	genome = []
	"Renvoie sous forme de tableau de strings le genome specifie dans le fichier"
	f = open(fichier, 'r')
	for line in f:
		genome.append(line.strip())
	return genome
def CPUtoInt(cpu):
	return 0
def intToCPU(entier):
	return CPU()
def photo(univers,file):
	"""Ecrit son etat dans le fichier done en argument. Remplace le fichier s'il existait deja"""
	#Dans l'ordre : nb CPUs, nuero CPU suivant, CPUs,nbCaseMemoire,Memoire
	donnees=len(univers.liste_cpus).to_bytes(univers.b1,byteorder='big')
	donnees+=univers.cpu_actuel.to_bytes(univers.b1,byteorder='big')
	
	nextToSave=0
	while 8 < len(univers.liste_cpus) - nextToSave:
		temp=0
		for i in range(8):
			temp=CPUtoInt((temp<<univers.n1)+univers.liste_cpus[nextToSave])
			nextToSave += 1
		donnees+=temp.to_bytes(univers.n1,byteorder='big')
	temp=0
	for i in range(nextToSave,len(univers.liste_cpus)):
		temp=(temp<<univers.n1)+CPUtoInt(univers.liste_cpus[i])
	k=(len(univers.liste_cpus)-nextToSave)*univers.n1
	n=math.ceil(k/8.)
	print("n :",n,"/",temp)
	donnees+=(temp<<(8*n-k)).to_bytes(n,byteorder='big')


	donnees+=len(univers.memoire).to_bytes(univers.b2,byteorder='big')
		
	nextToSave=0
	while 8 < len(univers.memoire) - nextToSave:
		temp=0
		for i in range(8):
			temp=(temp<<univers.n2)+univers.memoire[nextToSave]
			nextToSave += 1
		donnees+=temp.to_bytes(univers.n2,byteorder='big')
	
	temp=0
	for i in range(nextToSave,len(univers.memoire)):
		temp=(temp<<univers.n2)+univers.memoire[i]
	k=(len(univers.memoire)-nextToSave)*univers.n2
	n=math.ceil(k/8)
	donnees+=(temp<<(8*n-k)).to_bytes(n,byteorder='big')
	

	f=open(file,'wb')
	f.write(donnees)
	print(len(donnees),donnees)
	f.close()
	
def loadPhoto(univers,file):
	"""Lit un etat dans le fichier donne en argument."""
	#Dans l'ordre : nb CPUs, nuero CPU suivant, CPUs,nbCaseMemoire,Memoire
	univers.liste_cpus=[]
	f=open(file,'rb')
	
	lenCPU=int.from_bytes(f.read(univers.b1),byteorder='big')
	univers.cpu_actuel=int.from_bytes(f.read(univers.b1),byteorder='big')
	
	CPUs=f.read(math.ceil(univers.n1*lenCPU/8.))
	k1=0
	for k in range(lenCPU):
		temp=0
		while(k1<univers.n1*(k+1)):
			l=k1//8
			debut=k1-l*8
			nombreALire=min(univers.n1*(k+1)-k1,8-debut)
			temp= (temp<<nombreALire )+ ( (CPUs[l] << debut & 0b11111111)>>(8-nombreALire) ) & 0b11111111   #on veut lire de debut a debut+nombre a lire.
			k1+=nombreALire
		univers.liste_cpus.append(intToCPU(temp))
	
	univers.memoire=[]
	
	lenMemoire=int.from_bytes(f.read(univers.b2),byteorder='big')
	memory=f.read(math.ceil(univers.n2*lenMemoire/8.))
	print(memory)
	k1=0
	for k in range(lenMemoire):
		temp=0
		while(k1<univers.n2*(k+1)):
			l=k1//8
			debut=k1-l*8
			nombreALire=min(univers.n2*(k+1)-k1,8-debut)
			temp= (temp<<nombreALire )+ ( (memory[l] << debut & 0b11111111)>>(8-nombreALire) ) & 0b11111111   #on veut lire de debut a debut+nombre a lire.
			k1+=nombreALire
		univers.memoire.append(temp)
	f.close()

