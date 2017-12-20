from math import *
from CPU import *
def charger_genome(fichier):
	genome = []
	"Renvoie sous forme de tableau de strings le genome specifie dans le fichier"
	f = open(fichier, 'r')
	for line in f:
		genome.append(line.strip())
	return genome
def CPUtoInt(cpu):
	k=ceil(log(CPU.TAILLE_STACK,2))
	resultat=cpu.ax
	resultat=(resultat<<cpu.univers.n2)+cpu.bx
	resultat=(resultat<<cpu.univers.n2)+cpu.cx
	resultat=(resultat<<cpu.univers.n2)+cpu.dx
	resultat=(resultat<<cpu.univers.n2)+cpu.ptr
	for i in cpu.stack:
		resultat=(resultat<<cpu.univers.n2)+i
	resultat=(resultat<<k)+cpu.stack_ptr
	return resultat
def intToCPU(entier,univers):
	k=ceil(log(CPU.TAILLE_STACK,2))
	bits0=0
	for i in range(univers.n2):
		bits0+=2**i
	bits1=0
	for i in range(k):
		bits1+=2**i
	stack_ptr=entier & bits1		
	stack=[]
	for i in range(CPU.TAILLE_STACK):
		stack.insert(0,(entier>>(k+i*cpu.univers.n2))&bits0)
	ptr=(entier>>(k+(CPU.TAILLE_STACK)*cpu.univers.n2))&bits0
	dx=(entier>>(k+(CPU.TAILLE_STACK+1)*cpu.univers.n2))&bits0
	cx=(entier>>(k+(CPU.TAILLE_STACK+2)*cpu.univers.n2))&bits0
	bx=(entier>>(k+(CPU.TAILLE_STACK+3)*cpu.univers.n2))&bits0
	ax=(entier>>(k+(CPU.TAILLE_STACK+4)*cpu.univers.n2))&bits0
	print(ax, bx, cx, dx,stack , stack_ptr)
	return CPU(ptr, Univers, ax, bx, cx, dx,stack , stack_ptr)
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
	n=ceil(k/8.)
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
	n=ceil(k/8)
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
	
	CPUs=f.read(ceil(univers.n1*lenCPU/8.))
	k1=0
	for k in range(lenCPU):
		temp=0
		while(k1<univers.n1*(k+1)):
			l=k1//8
			debut=k1-l*8
			nombreALire=min(univers.n1*(k+1)-k1,8-debut)
			temp= (temp<<nombreALire )+ ( (CPUs[l] << debut & 0b11111111)>>(8-nombreALire) ) & 0b11111111   #on veut lire de debut a debut+nombre a lire.
			k1+=nombreALire
		univers.liste_cpus.append(intToCPU(temp,univers))
	
	univers.memoire=[]
	
	lenMemoire=int.from_bytes(f.read(univers.b2),byteorder='big')
	memory=f.read(ceil(univers.n2*lenMemoire/8.))
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

