
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
    def save(self,file):
        """Ecrit son etat dans le fichier donné en argument. Remplace le fichier s'il existait déjà"""
        n1=0 #nb bit du nb de CPU
        n2=0 #nb bit d'un CPU
        n3=0 #nb bit d'une case memoire
        f=open(file,w)
        a=len(CPU)
        k=n1
        while(k<=n1-8):
            f.write(a>>k & 0b11111111)
            k += 8
        temp=a>>k
        
        
    ## functions for analysis
    def colonisationRate(self) :
        "renvoie le taux de cases remplies dans la liste Memoire[] de l'univers à la date t"
        instructionsNb = 0;
        for i in self.Memory :
            if i != None :
                instructionsNb += 1;
        return (instructionsNb/len(self.Memory)) ;


    def loopUnits(self) : # pas fini du tout !
        "??? en utilisant la méthose donnée par le tuteur : un CPU-test parcourt le code, on identifie un individu-boucle comme la plus grande boucle possible."
        # je ne sais plus s'il faut pouvoir retourner au début depuis la fin, où juste arriver à la fin depuis le début
        N = len(self.Memory);   # devrait être une variable globale ?
        origin = [None] * N;
        test = CPU() ;   #comment gérer les différences de contenu des registres etc ?
        for i in range(N) :
            if origin[i] == None :
                origin[i] = i;
                currentOrigin = i;
                test.index = i;
                while ?? :
                    test.execute();
                    origin[test.index] = currentOrigin;
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

        
    
