
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
        while(k>=8):
            k -= 8
            f.write(chr(a>>k & 0b11111111))
        temp=a<<8-k
        a=len(CPU)
        k=n2+8-k
        while(k>=8):
            k -= 8
            f.write(a>>k & 0b11111111)
    