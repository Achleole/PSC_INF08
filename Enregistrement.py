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
    k = ceil(log(CPU.TAILLE_STACK, 2))
    # if cpu.ax>2**(cpu.univers.n3):
    # 	print("erreur ax")
    # if cpu.bx>2**(cpu.univers.n3):
    # 	print("erreur bx")
    # if cpu.cx>2**(cpu.univers.n3):
    # 	print("erreur cx")
    # if cpu.dx>2**(cpu.univers.n3):
    # 	print("erreur dx")
    # if cpu.ptr>2**(cpu.univers.n3):
    # 	print("erreur ptr")
    resultat = cpu.ax
    resultat = (resultat << cpu.univers.n3) + cpu.bx
    resultat = (resultat << cpu.univers.n3) + cpu.cx
    resultat = (resultat << cpu.univers.n3) + cpu.dx
    resultat = (resultat << cpu.univers.n3) + cpu.ptr
    for i in cpu.stack:
        resultat = (resultat << cpu.univers.n2) + i
    resultat = (resultat << k) + cpu.stack_ptr
    return resultat


def intToCPU(entier, univers):
    k = ceil(log(CPU.TAILLE_STACK, 2))
    bits0 = 0
    for i in range(univers.n3):
        bits0 += 2 ** i
    bits1 = 0
    for i in range(k):
        bits1 += 2 ** i
    bits2 = 0
    for i in range(univers.n2):
        bits2 += 2 ** i
    stack_ptr = entier & bits1
    stack = []
    for i in range(CPU.TAILLE_STACK):
        stack.insert(0, (entier >> (k + i * univers.n2)) & bits2)
    ptr = (entier >> (k + (CPU.TAILLE_STACK) * univers.n2)) & bits0
    dx = (entier >> (k + CPU.TAILLE_STACK * univers.n2 + 1 * univers.n3)) & bits0
    cx = (entier >> (k + CPU.TAILLE_STACK * univers.n2 + 2 * univers.n3)) & bits0
    bx = (entier >> (k + CPU.TAILLE_STACK * univers.n2 + 3 * univers.n3)) & bits0
    ax = (entier >> (k + CPU.TAILLE_STACK * univers.n2 + 4 * univers.n3)) & bits0
    return CPU(ptr, univers, ax, bx, cx, dx, stack, stack_ptr)

class Replay:
    def __init__(self):
        self.univers=None
        self.fichier=None
        self.f=None
        self.buffer=0
        self.nBits=0
        self.etat=''
    def openLoad(self,fichier):
        if self.etat!='':
            self.f.close()
        self.etat='r'
        self.fichier=fichier
        self.f=open(fichier,'r')
        self.n=int(self.f.readline())
    def openWrite(self,fichier,n=100):
        self.etat='w'
        self.fichier=fichier
        self.f=open(fichier)
        self.n=n
        self.f.write('n\n')
        self.f.close()
    def saveEvolution(self,case):
        if self.etat=='w':
            self.buffer=(self.buffer<<Univers.n2)+case
            self.nBits+=Univers.n2
            while self.nBits>=8:
                saving=self.buffer>>(self.nBits-8)
                self.buffer-=saving<<(self.nBits-8)
                self.f.write(saving.to_bytes(1,byteorder='big'))
                self.nBits-=8
    def simulate(self):
        if self.etat=='r':

            while self.nBits<Univers.n2:
                self.buffer=(self.buffer<<8)+int.from_bytes(self.f.read(1), byteorder='big')
                self.nBits+=8
            case=self.buffer>>(self.nBits-Univers.n2)
            self.buffer-=case<<(self.nBits-Univers.n2)
            self.nBits-=Univers.n2
    def nom_temp(self,memoire):
        self.supprimer_cpu_localisation(self.cpu_actuel())
        if self.univers.memoire[self.univers.cpu_actuel().ptr] == 36:
            self.univers.executer_cpu_actuel()
            self.univers.memoire[self.univers.ind(self.univers.cpu_actuel().ax)]=memoire

        self.univers.executer_cpu_actuel()
        self.univers.ajouter_cpu_localisation(self.cpu_actuel())
        self.univers.next_cpu()

    def photo(self,univers,mode='w'):
        """Ecrit son etat dans le fichier done en argument. Ajoute les données a la din du fichier s'il existait deja"""
        # Dans l'ordre : nb CPUs, nuero CPU suivant, CPUs, nbCaseMemoire,Memoire
        donnees = len(univers.liste_cpus).to_bytes(univers.b1, byteorder='big')
        donnees += univers.indice_cpu_actuel.to_bytes(univers.b1, byteorder='big')

        nextToSave = 0
        while 8 < len(univers.liste_cpus) - nextToSave:
            temp = 0
            for i in range(8):
                temp = (temp << univers.n1) + CPUtoInt(univers.liste_cpus[nextToSave])
                nextToSave += 1
            donnees += temp.to_bytes(univers.n1, byteorder='big')
        temp = 0
        for i in range(nextToSave, len(univers.liste_cpus)):
            t = CPUtoInt(univers.liste_cpus[i])
            temp = (temp << univers.n1) + CPUtoInt(univers.liste_cpus[i])
        k = (len(univers.liste_cpus) - nextToSave) * univers.n1
        n = ceil(k / 8.)
        # print("n :",n,"/",k,log(temp,2))
        donnees += (temp << (8 * n - k)).to_bytes(n, byteorder='big')

        donnees += len(univers.memoire).to_bytes(univers.b2, byteorder='big')

        nextToSave = 0
        while 8 < len(univers.memoire) - nextToSave:
            temp = 0
            for i in range(8):
                temp = (temp << univers.n2) + univers.memoire[nextToSave]
                nextToSave += 1
            donnees += temp.to_bytes(univers.n2, byteorder='big')

        temp = 0
        for i in range(nextToSave, len(univers.memoire)):
            temp = (temp << univers.n2) + univers.memoire[i]
        k = (len(univers.memoire) - nextToSave) * univers.n2
        n = ceil(k / 8)
        donnees += (temp << (8 * n - k)).to_bytes(n, byteorder='big')

        f = open(self.fichier, mode+'b')
        f.write(donnees)
        # print(len(donnees),donnees)
        f.close()

    def loadPhoto(self,univers):
        """Lit un etat dans le fichier donne en argument."""
        # Dans l'ordre : nb CPUs, nuero CPU suivant, CPUs,nbCaseMemoire,Memoire
        univers.liste_cpus = []
        f = open(self.fichier, 'rb')
        lenCPU = int.from_bytes(f.read(univers.b1), byteorder='big')

        univers.indice_cpu_actuel = int.from_bytes(f.read(univers.b1), byteorder='big')

        CPUs = f.read(ceil(univers.n1 * lenCPU / 8.))
        k1 = 0
        for k in range(lenCPU):
            temp = 0
            while (k1 < univers.n1 * (k + 1)):
                l = k1 // 8
                debut = k1 - l * 8
                nombreALire = min(univers.n1 * (k + 1) - k1, 8 - debut)
                temp = (temp << nombreALire) + (((CPUs[l] << debut & 0b11111111) >> (
                        8 - nombreALire)) & 0b11111111)  # on veut lire de debut a debut+nombre a lire.
                k1 += nombreALire
            univers.liste_cpus.append(intToCPU(temp, univers))

        univers.memoire = []

        lenMemoire = int.from_bytes(f.read(univers.b2), byteorder='big')
        memory = f.read(ceil(univers.n2 * lenMemoire / 8.))
        # print(memory)
        k1 = 0
        for k in range(lenMemoire):
            temp = 0
            while (k1 < univers.n2 * (k + 1)):
                l = k1 // 8
                debut = k1 - l * 8
                nombreALire = min(univers.n2 * (k + 1) - k1, 8 - debut)
                temp = (temp << nombreALire) + ((memory[l] << debut & 0b11111111) >> (
                        8 - nombreALire)) & 0b11111111  # on veut lire de debut a debut+nombre a lire.
                k1 += nombreALire
            univers.memoire.append(temp)
        f.close()
        for cpu in univers.liste_cpus:
            univers.ajouter_cpu_localisation(cpu)
        return univers