import math
import CPU.py
class Universe:
    def __init__(self):
        self.CPU=[]
        self.CPUsuivant=-1
        self.memoire=[]
    def roundSlicer(self):
        self.mainLoop(len(self.CPU))
    def forward(self,N):
        """ fait executer N intruction"""
        for i in range(N):
            self.execute()
    def execute(self):
        """ fait executer une intruction par un processeur"""
        self.CPU[self.CPUsuivant].execute()
        self.CPUsuivant+=1
    def killCPU(self,cpu):
        """ Tue le processeur donné en argupent"""
        #à améliorer
        killed = False
        i = 0
        while not killed:
            if self.CPU[i] is cpu:
                self.CPU=self.CPU[:i]+self.CPU[i+1:]
                CPUsuivant -= (i < CPUsuivant)
                killed = True
            i += 1
    def kill(self):
        self.CPU=self.CPU[:CPUsuivant]+self.CPU[CPUsuivant+1:]
        CPUsuivant -= 1
    def createCPU(self):
        """ Rajoute un  processeur dans le slicer, juste avant le processeur actif"""
        nouveau = CPU()
        self.CPU=self.CPU[self.CPUsuivant:]+[nouveau]+self.CPU[:self.CPUsuivant]
        self.CPUsuivant+=1
    def photo(self,file):
        """Ecrit son etat dans le fichier donné en argument. Remplace le fichier s'il existait déjà"""
        b1=2 #nb bytes du nb de CPU et du numero du CPU considéré actuellement.
        n1=5 #nb bit d'un CPU
        b2=2 #nb bytes du nb de case memoire.
        n2=5 #nb bit d'une case memoire
        #Dans l'ordre : nb CPUs, nuero CPU suivant, CPUs,nbCaseMemoire,Memoire
        donnees=len(self.CPU).to_bytes(b1,byteorder='big')
        donnees+=self.CPUsuivant.to_bytes(b1,byteorder='big')
        
        nextToSave=0
        while 8 < len(self.CPU) - nextToSave:
            temp=0
            for i in range(8):
                temp=(temp<<n1)+self.CPU[nextToSave].toBits()
                nextToSave += 1
            donnees+=temp.to_bytes(n1,byteorder='big')
        temp=0
        for i in range(nextToSave,len(self.CPU)):
            temp=(temp<<n1)+self.CPU[i].toBits()
        k=(len(self.CPU)-nextToSave)*n1
        n=math.ceil(k/8.)
        print("n :",n,"/",temp)
        donnees+=(temp<<(8*n-k)).to_bytes(n,byteorder='big')


        donnees+=len(self.memoire).to_bytes(b2,byteorder='big')
            
        nextToSave=0
        while 8 < len(self.memoire) - nextToSave:
            temp=0
            for i in range(8):
                temp=(temp<<n2)+self.memoire[nextToSave]
                nextToSave += 1
            donnees+=temp.to_bytes(n2,byteorder='big')
        
        temp=0
        for i in range(nextToSave,len(self.memoire)):
            temp=(temp<<n2)+self.memoire[i]
        k=(len(self.memoire)-nextToSave)*n2
        n=math.ceil(k/8)
        donnees+=(temp<<(8*n-k)).to_bytes(n,byteorder='big')
        

        f=open(file,'wb')
        f.write(donnees)
        print(len(donnees),donnees)
        f.close()
    def loadPhoto(self,file):
        """Lit un etat dans le fichier donné en argument."""
        b1=2 #nb bytes du nb de CPU et du numero du CPU considéré actuellement.
        n1=5 #nb bit d'un CPU
        b2=2 #nb bytes du nb de case memoire.
        n2=5 #nb bit d'une case memoire
        #Dans l'ordre : nb CPUs, nuero CPU suivant, CPUs,nbCaseMemoire,Memoire
        self.CPU=[]
        f=open(file,'rb')
        
        lenCPU=int.from_bytes(f.read(b1),byteorder='big')
        self.CPUsuivant=int.from_bytes(f.read(b1),byteorder='big')
        
        CPUs=f.read(math.ceil(n1*lenCPU/8.))
        k1=0
        for k in range(lenCPU):
            temp=0
            while(k1<n1*(k+1)):
                l=k1//8
                debut=k1-l*8
                nombreALire=min(n1*(k+1)-k1,8-debut)
                temp= (temp<<nombreALire )+ ( (CPUs[l] << debut & 0b11111111)>>(8-nombreALire) ) & 0b11111111   #on veut lire de debut a debut+nombre a lire.
                k1+=nombreALire
            self.CPU.append(CPU(temp))
        
        self.memoire=[]
        
        lenMemoire=int.from_bytes(f.read(b1),byteorder='big')
        memoire=f.read(math.ceil(n2*lenMemoire/8.))
        print(memoire)
        k1=0
        for k in range(lenMemoire):
            temp=0
            while(k1<n2*(k+1)):
                l=k1//8
                debut=k1-l*8
                nombreALire=min(n2*(k+1)-k1,8-debut)
                temp= (temp<<nombreALire )+ ( (memoire[l] << debut & 0b11111111)>>(8-nombreALire) ) & 0b11111111   #on veut lire de debut a debut+nombre a lire.
                k1+=nombreALire
            self.memoire.append(temp)
        f.close()



    ## functions for analysis
    def colonisationRate(self) :
        "renvoie le taux de cases remplies dans la liste Memoire[] de l'univers à la date t"
        instructionsNb = 0;
        for i in self.Memory :
            if i != None :
                instructionsNb += 1;
        return (instructionsNb/len(self.Memory)) ;


    def loopUnits(self) : 
        "Détermine les 'unités' en utilisant la méthose donnée par le tuteur : un CPU-test parcourt le code, on identifie une 'unité' comme la plus grande boucle possible. Retourne un tableau de la taille de self.Memoire contenant, à l'indice i, l'indice du 'début' de l'unité à laquelle appartient l'instruction située en i dans Memoire."
        # je ne sais plus s'il faut pouvoir retourner au début depuis la fin, où juste arriver à la fin depuis le début
        # qu'arrive-t-il aux instructions mortes ?
        self = reconstitue(t);
        N = len(self.Memoire);   # devrait être une variable globale ?
        loopStart = [None] * N;
        for i in range(N) :
            test = CPU() ;
            if self.Memoire != None & loopStart[i] == None :
                test.index = i;
                while loopStart[test.index] !=  i:
                    loopStart[test.index] = i;
                    if test.execute() == "Error" : #Attention à l'implémentation de l'erreur #se peut-il que l'exécution n'incrémente pas (ou en tout cas ne fasse pas changer) test.index ? si oui alors la condition du while n'est pas suffisante
                        break;
        return loopStart;


    def rateCreationCPUs(self, interval) :
        "retourne le nombre moyen de CPUs créés par CPU existant et par an pendant l'intervalle de temps de longueur interval et commençant à l'état présent"
        nbCreated = 0;
        date = 0;
        currentCPUnumber = len(self.CPU);
        while date < interval :
            self.roundSlicer() ;
            nbCreated += len(self.CPU)/currentCPUnumber - 1 ; # ou faire une fonction qui calcule le nb de CPUs crées à la date t ?
            currentCPUnumber = len(self.CPU);
        return (nb_created/interval) ;


    def CPUdensity(self, t) :
        "affiche et renvoie la densite de CPU par site d'instruction occupé" #on pourrait faire par site d'instruction tout court ?
        d = len(self.CPU) / (self.colonisationRate()*len(self.Memory)) ;
        print("La densité de CPU est {}, soit 1 CPU pour {} instructions".format(d, 1/d));
        return d;


    def nbLoopUnits(self) : #devrait être fait en même temps que loopUnits ??
        "renvoie le nombre d' 'unités'"
        loopStart = self.loopUnits() ;
        loopUnitsList = [];
        for i in range(len(loopStart)) :
            if loopStart[i] == i:
                loopUnitsList.append(i) ;
        return len(loopUnitsList) ;

    def nbSpecies(t) :
        "renvoie le nombre de codes différents parmi tous les individus-boucles identifiés"

    def speciesDistance() :
        "renvoie la distance d'édition entre les codes des deux espèces données en paramètre"
