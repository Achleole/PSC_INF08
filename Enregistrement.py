from math import *
import CPU
import Univers

def charger_genome(fichier):
    genome = []
    "Renvoie sous forme de tableau de strings le genome specifie dans le fichier"
    f = open(fichier, 'r')
    for line in f:
        genome.append(line.strip())
    f.close()
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
    # 	print("erreur ptr")l=cpu.id.split("/")
    l = cpu.id.split("/")
    resultat = int(l[-1])
    parent=(int(l[-2]) if len(l)>1 else 2**(cpu.univers.b1 *8)-1)
    resultat = (resultat << cpu.univers.b1*8)+parent
    resultat = (resultat << cpu.univers.n3) + cpu.ax
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
    bits1 = 2**k-1
    bits2 = 2**(univers.n2)-1
    bits3 = 2**(univers.b1 *8)-1
    stack_ptr = entier & bits1
    stack = []
    for i in range(CPU.TAILLE_STACK):
        stack.insert(0, (entier >> (k + i * univers.n2)) & bits2)
    ptr = (entier >> (k + (CPU.TAILLE_STACK) * univers.n2)) & bits0
    dx = (entier >> (k + CPU.TAILLE_STACK * univers.n2 + 1 * univers.n3)) & bits0
    cx = (entier >> (k + CPU.TAILLE_STACK * univers.n2 + 2 * univers.n3)) & bits0
    bx = (entier >> (k + CPU.TAILLE_STACK * univers.n2 + 3 * univers.n3)) & bits0
    ax = (entier >> (k + CPU.TAILLE_STACK * univers.n2 + 4 * univers.n3)) & bits0
    parent = (entier >> (k + CPU.TAILLE_STACK * univers.n2 + 5 * univers.n3)) & bits3
    id = (entier >> (k + CPU.TAILLE_STACK * univers.n2 + univers.b1 * 8 + 5 * univers.n3)) & bits3
    id_final =(str(id) if parent==2**(univers.b1 *8)-1 else str(parent)+"/"+str(id))
    return CPU.CPU(ptr, univers, ax, bx, cx, dx, stack, stack_ptr, None, id_final)

class Replay:
    def __init__(self):
        self.univers=None
        self.fichier=None
        self.f=None
        self.buffer=0
        self.nBits=0
        self.etat=''
        self.position=0
        self.debug=False

    def test(self,fichier,univers,k):
        self.univers=univers
        self.openWrite(fichier)
        memoire=[univers.copy()]
        for i in range(k):
            self.runAndSaveOne()
            memoire.append(self.univers.copy())
    def forward(self,n):
        if self.etat=="r":
            for i in range(n):
                self.readOne()

    def runAndSave(self,n):
        for i in range(n):
            self.runAndSaveOne()
    def runAndSaveOne(self):
        if self.etat=="w":
            if self.position%self.n: #si self.position n'est pas un multiple de self.n
                c = self.univers.cpu_actuel()
                instruction = self.univers.memoire[c.ptr]
                self.univers.execute(1)
                if instruction==36:
                    self.saveWrite(c.univers.memoire[c.ax])
                elif instruction==34:
                    self.saveRand(c.ax)
            else:
                if self.nBits>0:
                    saving = self.buffer << (8- self.nBits )
                    self.nBits = 0
                    self.buffer = 0
                    self.f.write(saving.to_bytes(1, byteorder='big'))
                self.univers.execute(1)
                self.photo()
            self.position+=1
    def cycleAndSave(self, n):
        for i in range(n):
            self.cycleAndSaveOne()
    def cycleAndSaveOne(self):
        nb = len(self.univers.liste_cpus)
        try:
            if nb == 0:
                raise CPU.NoCPUException()
            for i in range(nb):
                self.runAndSaveOne()
            self.univers.tuer_cpus_par_densite()
        except Exception as e:
            print(e)
            raise
        finally:
            if self.univers.statistiques != None:
                self.univers.statistiques.mettre_a_jour()
            self.univers.reinitialise_cpus_crees()
    def ForwardCycle(self,n):
        for i in range(n):
            self.ForwardCycleOne()
    def ForwardCycle(self):
        pass
    def openLoad(self,fichier):
        if self.etat!='':
            self.close()
        self.etat='r'
        self.fichier=fichier
        self.f=open(fichier,"rb")
        self.n=int.from_bytes(self.f.read(3),byteorder='big')
        self.position=0
        self.buffer=0
    def readOne(self):
        if self.etat=="r":
            if self.position%self.n==0:
                self.loadPhoto()
                k=2
            else:
                self.advance()
            self.position+=1
    def openWrite(self,fichier,n=100):
        if self.etat!='':
            self.close()
        self.etat='w'
        self.fichier=fichier
        self.f=open(fichier,"wb")
        self.n=n
        self.f.write(n.to_bytes(3,byteorder='big'))
        self.position=0
    def close(self):
        if self.etat=="w":
            self.viderBuffer()
        self.f.close()
    def viderBuffer(self):
        assert(self.nBits<8)
        if self.nBits>0:
            ecrire = self.buffer << (8 - self.nBits)
            self.f.write(ecrire.to_bytes(1, byteorder='big'))
            self.buffer=0
            self.nBits=0
    def saveWrite(self,case):
        if self.etat=='w':
            self.buffer=(self.buffer << Univers.Univers.n2)+case
            self.nBits+=Univers.Univers.n2
            while self.nBits>=8:
                saving=self.buffer>>(self.nBits-8)
                self.buffer-=saving<<(self.nBits-8)
                self.f.write(saving.to_bytes(1,byteorder='big'))
                self.nBits-=8
            if self.debug:
                print("write evolution :",case, "position :",self.position)
    def readEvolutionWrite(self):
        if self.etat=='r':
            while self.nBits< Univers.Univers.n2:
                self.buffer=(self.buffer<<8)+int.from_bytes(self.f.read(1),byteorder='big')
                self.nBits+=8
            case=self.buffer>>(self.nBits - Univers.Univers.n2)
            self.buffer-=case<<(self.nBits - Univers.Univers.n2)
            self.nBits-= Univers.Univers.n2
            if self.debug:
                print("read evolution :",case, "position :",self.position)
            return case
    def saveRand(self, ax):
        if self.etat == 'w':
            self.buffer = (self.buffer << (Univers.Univers.b2 * 8)) + ax
            self.nBits += Univers.Univers.b2 * 8
            nBytes = self.nBits//8
            while self.nBits >= 8:
                saving = self.buffer >> (self.nBits - 8*nBytes)
                self.buffer -= saving << (self.nBits - 8*nBytes)
                self.f.write(saving.to_bytes(nBytes, byteorder='big'))
                self.nBits -= 8*nBytes
            if self.debug:
                print("etatcriture rand :", ax, "position :",self.position)
    def readEvolutionRand(self):
        if self.etat=='r':
            while self.nBits< Univers.Univers.b2*8:
                self.buffer=(self.buffer<<8)+int.from_bytes(self.f.read(1), byteorder='big')
                self.nBits+=8
            case=self.buffer>>(self.nBits - Univers.Univers.b2 * 8)
            self.buffer-=case<<(self.nBits - Univers.Univers.b2*8)
            self.nBits-= Univers.Univers.b2*8
            if self.debug:
                print("lecture rand :",case, "position :",self.position)
            return case
    def advance(self):
        c=self.univers.cpu_actuel()
        if self.univers.memoire[c.ptr]==36:
            c.ax = c.univers.ind(c.ax)
            self.univers.execute(1)
            c.univers.memoire[c.ax] = self.readEvolutionWrite()
            # comme la fonction write mais qui ecrit la valeur case donnee en argument a la place de ce que le CPU devrait ecrire.
        elif self.univers.memoire[c.ptr]==34:
            self.univers.execute(1)
            c.ax = self.readEvolutionRand()
        else:
            self.univers.executer_cpu_actuel()
    def find_closest(self,nbtour):
        if len(self.positionsPhotos)==0:
            return None,0
        elif self.positionsPhotos[0][1]<nbtour:
            a=0
            b=len(self.positionsPhotos)-1
            while a<b:
                print(a,b)
                c=int((a+b+1)/2)
                if self.positionsPhotos[c][1]<nbtour:
                    a=c
                else:
                    b=c-1
            return self.positionsPhotos[a]
        else:
            return None
    def goto(self,n):
        pos,tours=self.find_closest(n)
        self.f.seek(pos)
        self.tour=tours
        self.position=0
        while self.tour<n:
            self.readOne()
        #la normalement c'est bon

    def nom_temp(self,memoire):
        if self.univers.memoire[self.univers.cpu_actuel().ptr] == 36:
            self.univers.executer_cpu_actuel()
            self.univers.memoire[self.univers.ind(self.univers.cpu_actuel().ax)]=memoire

        self.univers.executer_cpu_actuel()
        self.univers.next_cpu()

    def photo(self):
        if self.debug:
            print("photo, buffer :",self.buffer, "position :",self.position)
        """Ecrit son etat dans le fichier done en argument. Ajoute les donnees a la din du fichier s'il existait deja"""
        # Dans l'ordre : nb CPUs, nuero CPU suivant, CPUs, nbCaseMemoire,Memoire
        self.viderBuffer()
        donnees = len(self.univers.liste_cpus).to_bytes(self.univers.b1, byteorder='big')
        donnees += self.univers.indice_cpu_actuel.to_bytes(self.univers.b1, byteorder='big')

        nextToSave = 0
        while 8 < len(self.univers.liste_cpus) - nextToSave:
            temp = 0
            for i in range(8):
                temp = (temp << self.univers.n1) + CPUtoInt(self.univers.liste_cpus[nextToSave])
                nextToSave += 1
            donnees += temp.to_bytes(self.univers.n1, byteorder='big')
        temp = 0
        for i in range(nextToSave, len(self.univers.liste_cpus)):
            t = CPUtoInt(self.univers.liste_cpus[i])
            temp = (temp << self.univers.n1) + CPUtoInt(self.univers.liste_cpus[i])
        k = (len(self.univers.liste_cpus) - nextToSave) * self.univers.n1
        n = ceil(k / 8.)
        donnees += (temp << (8 * n - k)).to_bytes(n, byteorder='big')

        donnees += len(self.univers.memoire).to_bytes(self.univers.b2, byteorder='big')

        nextToSave = 0
        while 8 < len(self.univers.memoire) - nextToSave:
            temp = 0
            for i in range(8):
                temp = (temp << self.univers.n2) + self.univers.memoire[nextToSave]
                nextToSave += 1
            donnees += temp.to_bytes(self.univers.n2, byteorder='big')

        temp = 0
        for i in range(nextToSave, len(self.univers.memoire)):
            temp = (temp << self.univers.n2) + self.univers.memoire[i]
        k = (len(self.univers.memoire) - nextToSave) * self.univers.n2
        n = ceil(k / 8)
        donnees += (temp << (8 * n - k)).to_bytes(n, byteorder='big')

        self.f.write(donnees)
        self.univers.TAILLE_MEMOIRE = len(self.univers.memoire)

    def loadPhoto(self):
        if self.debug:
            print("load photo, buffer :",self.buffer)
        assert(self.buffer==0)
        self.nBits=0
        """Lit un etat dans le fichier donne en argument."""
        # Dans l'ordre : nb CPUs, nuero CPU suivant, CPUs,nbCaseMemoire,Memoire
        self.univers.liste_cpus = []
        lenCPU = int.from_bytes(self.f.read(self.univers.b1), byteorder='big')

        self.univers.indice_cpu_actuel = int.from_bytes(self.f.read(self.univers.b1), byteorder='big')

        CPUs = self.f.read(ceil(self.univers.n1 * lenCPU / 8.))
        k1 = 0
        for k in range(lenCPU):
            temp = 0
            while (k1 < self.univers.n1 * (k + 1)):
                l = k1 // 8
                debut = k1 - l * 8
                nombreALire = min(self.univers.n1 * (k + 1) - k1, 8 - debut)
                temp = (temp << nombreALire) + (((CPUs[l] << debut & 0b11111111) >> (
                        8 - nombreALire)) & 0b11111111)  # on veut lire de debut a debut+nombre a lire.
                k1 += nombreALire
            self.univers.liste_cpus.append(intToCPU(temp, self.univers))

        self.univers.memoire = []

        lenMemoire = int.from_bytes(self.f.read(self.univers.b2), byteorder='big')
        memory = self.f.read(ceil(self.univers.n2 * lenMemoire / 8.))
        k1 = 0
        for k in range(lenMemoire):
            temp = 0
            while (k1 < self.univers.n2 * (k + 1)):
                l = k1 // 8
                debut = k1 - l * 8
                nombreALire = min(self.univers.n2 * (k + 1) - k1, 8 - debut)
                temp = (temp << nombreALire) + ((memory[l] << debut & 0b11111111) >> (
                        8 - nombreALire)) & 0b11111111  # on veut lire de debut a debut+nombre a lire.
                k1 += nombreALire
            self.univers.memoire.append(temp)
        for cpu in self.univers.liste_cpus:
            self.univers.ajouter_cpu_localisation(cpu)
        return self.univers