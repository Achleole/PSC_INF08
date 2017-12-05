
class Universe:
    def __init__(self):
        self.CPU=[]
        self.CPUsuivant=None
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
        self.CPU=[self.CPU[self.CPUsuivant:]+[nouveau]+self.CPU[:self.CPUsuivant]]
        self.CPUsuivant+=1
    def photo(self,file):
        """Ecrit son etat dans le fichier donné en argument. Remplace le fichier s'il existait déjà"""
        n1=0 #nb bit du nb de CPU, multiple de 8
        n2=0 #nb bit d'un CPU
        n3=0 #nb bit du nb de case memoire, multiple de 8
        n4=0 #nb bit d'une case memoire
        #Dans l'ordre : nb CPUs, nuero CPU suivant, CPUs,nbCaseMemoire,Memoire
        f=open(file,'w')
        a=len(self.CPU)
        k=n1
        while(k>=0):
            f.write(chr(a>>k & 0b1111111))
            k -= 8
        a=self.CPUsuivant
        k=n1
        while(k>=0):
            f.write(a>>k & 0b11111111)
<<<<<<< HEAD
            k -= 8
        nextToSave=0
        while 8 < len(self.CPU) - nextToSave:
            temp=0
            for i in range(8):
                temp=temp<<n2+CPU[nextToSave].toBits()
                nextToSave += 1
            k=8*n2
            while(k>=0):
                f.write(chr(temp>>k & 0b11111111))
                k -= 8
        for i in range(nextToSave,len(self.CPU)):
            temp=(temp<<n2)+CPU[i].toBits()
        k=(len(self.CPU)-nextToSave)*n2
        while(k>=0):
            f.write(chr(temp>>k & 0b11111111))
            k -= 8
        f.write(chr(temp<<(-1*k) & 0b11111111))

        a=len(self.memoire)
        k=n3
        while(k>=0):
            f.write(chr(a>>k & 0b1111111))
            k -= 8
            
        nextToSave=0
        while 8 < len(self.memoire) - nextToSave:
            temp=0
            for i in range(8):
                temp=temp<<n2+memoire[nextToSave]
                nextToSave += 1
            k=8*n4
            while(k>=0):
                f.write(chr(temp>>k & 0b11111111))
                k -= 8
        for i in range(nextToSave,len(self.memoire)):
            temp=(temp<<n2)+memoire[i]
        k=(len(self.memoire)-nextToSave)*n4
        while(k>=0):
            f.write(chr(temp>>k & 0b11111111))
            k -= 8
        f.write(chr(temp<<(-1*k) & 0b11111111))
    def loadPhoto(self,fichier):
        """Lit un etat dans le fichier donné en argument."""
        n1=0 #nb bit du nb de CPU, multiple de 8
        n2=0 #nb bit d'un CPU
        n3=0 #nb bit du nb de case memoire, multiple de 8
        n4=0 #nb bit d'une case memoire
        #Dans l'ordre : nb CPUs, nuero CPU suivant, CPUs,nbCaseMemoire,Memoire
        f=open(file,'r')
        temp=f.read(n1//8)
        
        
        k=n1
        while(k>=0):
            f.write(a>>k & 0b11111111)
            k -= 8
        nextToSave=0
        while 8 < len(self.CPU) - nextToSave:
            temp=0
            for i in range(8):
                temp=temp<<n2+CPU[nextToSave].toBits()
                nextToSave += 1
            k=8*n2
            while(k>=0):
                f.write(chr(temp>>k & 0b11111111))
                k -= 8
        for i in range(nextToSave,len(self.CPU)):
            temp=(temp<<n2)+CPU[i].toBits()
        k=(len(self.CPU)-nextToSave)*n2
        while(k>=0):
            f.write(chr(temp>>k & 0b11111111))
            k -= 8
        f.write(chr(temp<<(-1*k) & 0b11111111))

        a=len(self.memoire)
        k=n3
        while(k>=0):
            f.write(chr(a>>k & 0b1111111))
            k -= 8
            
        nextToSave=0
        while 8 < len(self.memoire) - nextToSave:
            temp=0
            for i in range(8):
                temp=temp<<n2+memoire[nextToSave]
                nextToSave += 1
            k=8*n4
            while(k>=0):
                f.write(chr(temp>>k & 0b11111111))
                k -= 8
        for i in range(nextToSave,len(self.memoire)):
            temp=(temp<<n2)+memoire[i]
        k=(len(self.memoire)-nextToSave)*n4
        while(k>=0):
            f.write(chr(temp>>k & 0b11111111))
            k -= 8
        f.write(chr(temp<<(-1*k) & 0b11111111))
        
    ## functions for analysis
    def colonisationRate(self) :
        "renvoie le taux de cases remplies dans la liste Memoire[] de l'univers à la date t"
        instructionsNb = 0;
        for i in self.Memory :
            if i != None :
                instructionsNb += 1;
        return (instructionsNb/len(self.Memory)) ;


    def individus_boucles(t) : # pas fini du tout !
        "??? en utilisant la méthose donnée par le tuteur : un CPU-test parcourt le code, on identifie un individu-boucle comme la plus grande boucle possible."
        # je ne sais plus s'il faut pouvoir retourner au début depuis la fin, où juste arriver à la fin depuis le début
        self = reconstitue(t);
        N = len(self.Memoire);   # devrait être une variable globale ?
        loopStart = [None] * N;
        test = CPU() ;
        for i in range(N) :
            if loopStart[i] == None :
                loopStart[i] = i;
                debut_courant = i;
                test.index = i;
                while ?? :
                    test.execute();
                    if ?? :
                        debut_boucle[test.index] = debut_courant;
                test.clear() ; #si cette méthode n'existe pas, on peut juste remplacer par test=CPU();
        return debut_boucle;


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


    def nbIndividuals(t) :
        "renvoie le nombre d'individus-boucles"

    def nbSpecies(t) :
        "renvoie le nombre de codes différents parmi tous les individus-boucles identifiés"

    def speciesDistance(??) :
        "renvoie la distance d'édition entre les codes des deux espèces données en paramètre"

        
<<<<<<< HEAD
=======
        
    ## functions for analysis
    def colonisationRate(self) :
        "renvoie le taux de cases remplies dans la liste Memoire[] de l'univers à la date t"
        instructionsNb = 0;
        for i in self.Memory :
            if i != None :
                instructionsNb += 1;
        return (instructionsNb/len(self.Memory)) ;


    def individus_boucles(t) : # pas fini du tout !
        "??? en utilisant la méthose donnée par le tuteur : un CPU-test parcourt le code, on identifie un individu-boucle comme la plus grande boucle possible."
        # je ne sais plus s'il faut pouvoir retourner au début depuis la fin, où juste arriver à la fin depuis le début
        self = reconstitue(t);
        N = len(self.Memoire);   # devrait être une variable globale ?
        loopStart = [None] * N;
        test = CPU() ;
        for i in range(N) :
            if loopStart[i] == None :
                loopStart[i] = i;
                debut_courant = i;
                test.index = i;
                while ?? :
                    test.execute();
                    if ?? :
                        debut_boucle[test.index] = debut_courant;
                test.clear() ; #si cette méthode n'existe pas, on peut juste remplacer par test=CPU();
        return debut_boucle;


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


    def nbIndividuals(t) :
        "renvoie le nombre d'individus-boucles"

    def nbSpecies(t) :
        "renvoie le nombre de codes différents parmi tous les individus-boucles identifiés"

    def speciesDistance(??) :
        "renvoie la distance d'édition entre les codes des deux espèces données en paramètre"

        
    
>>>>>>> 9d1876b65e4bb70d1d872b3fcec6df62f5e45a41
