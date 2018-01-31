from CPU import *
from Enregistrement import *
from math import *
import copy
import InstructionsDict


#TAILLE_MEMOIRE = 50000
#TAUX_MUTATION  = 0
#LARGEUR_CALCUL_DENSITE = 0
#SEUIL_DENSITE		   = 1.5

class Univers:
    "Contient les CPU et le monde i.e les instructions a executer"
    #valeurs non contractuelles.
    b1=2 #nb bytes du nb de CPU et du numero du CPU considere actuellement.
    b2=2 #nb bytes du nb de case memoire.
    n2=6 #nb bit d'une case memoire
    n3=16 #nb de bit d'un registre du CPU
    n1=5*n3+CPU.TAILLE_STACK*n2+ceil(log(CPU.TAILLE_STACK,2)) #nb bit d'un CPU
    #TAILLE_MEMOIRE = 500
    def __init__(s, TAILLE_MEMOIRE=50000, insDict=InstructionsDict.InstructionsDict(), mutation=0, LARGEUR_CALCUL_DENSITE=0, SEUIL_DENSITE=1.5):
        #code temporaire
        #eve = charger_genome('eve')
        s.statistiques             = None #Pointeur vers l'instance de la classe statistiques 
                                            #qui va recuperer les donnees de l'univers
        s.cpus_crees               = 0 #Contient le nombre de cpus crees lors du cycle termine
        s.TAILLE_MEMOIRE           = TAILLE_MEMOIRE
        s.memoire                  = [2]*(s.TAILLE_MEMOIRE)
        s.liste_cpus 	           = []     # ne pourrait-on pas gagner de l'efficacite en en faisant une liste chainee ?
        s.insDict                  = insDict
        s.mutation 				   = mutation #definit le taux de mutation de l'univers
        s.indice_cpu_actuel 	   = 0
        s.localisation_cpus        = {} # dictionnaire dont les clefs sont des adresses memoire, qui contient la liste des CPUs
        s.LARGEUR_CALCUL_DENSITE   = LARGEUR_CALCUL_DENSITE
        s.SEUIL_DENSITE            = SEUIL_DENSITE

    def set_statistiques(s, stats):
        "Initialisation des stats"
        s.statistiques = stats

    def cpu_actuel(s):
        "Renvoie un pointeur vers le CPU actuel"
        if len(s.liste_cpus)==0 :
            return None
        return s.liste_cpus[s.indice_cpu_actuel]

    def retourner_copie_memoire(self):
        return copy.copy(s.memoire)

    def incremente_cpus_crees(s):
        s.cpus_crees += 1

    def reinitialise_cpus_crees(s):
        s.cpus_crees = 0

    def retourner_cpus_crees(s):
        return s.cpus_crees

    def retourner_cpus_total(s):
        return len(s.liste_cpus)

    def cycle(s):
        "Execute les CPUs, met a jour les statistiques puit les tue par densite"
        try:
            s.executer_cpus()
            s.tuer_cpus_par_densite()
            if s.statistiques != None:
                s.statistiques.mettre_a_jour()
            s.reinitialise_cpus_crees()
        except Exception as e:
            print(e)
            raise

    def executer_cpus(s):
        "Cette fonction execute tous les CPU 1 fois\
        PRECISION IMPORTANTE : on parcourt la liste dans l'ordre des indices decroissant"
        if len(s.liste_cpus) == 0:
            raise NoCPUException()
        indice_cpu_depart = (s.indice_cpu_actuel) #Contient le cpu auquel on devra s'arreter
        cpu_actuel 	  = s.cpu_actuel()
        s.executer_cpu_actuel()
        s.next_cpu()
        while s.indice_cpu_actuel != indice_cpu_depart:
            s.executer_cpu_actuel()
            s.next_cpu()

    def executer_cpu_actuel(s):
        "Execute le CPU actuellement pointe SANS PASSER AU SUIVANT\
        i.e sans incrementer cpu_actuel"
        cpu = s.cpu_actuel()
        s.supprimer_cpu_localisation(cpu)
        cpu.execute()
        s.ajouter_cpu_localisation(cpu)

    def supprimer_cpu_localisation(s, cpu):
        "Prend en argument le pointeur vers un cpu et l'enleve du dictionnaire localisation_cpus"
        try:
            s.localisation_cpus[cpu.ptr].remove(cpu)
            if s.localisation_cpus[cpu.ptr] == []:
                del s.localisation_cpus[cpu.ptr]
        except Exception as e:
            print("Erreur de suppression de localisation !")
            print(e)

    def ajouter_cpu_localisation(s, cpu):
        if not cpu.ptr in s.localisation_cpus:
            s.localisation_cpus[cpu.ptr] = []
        if not cpu in s.localisation_cpus[cpu.ptr]:
            s.localisation_cpus[cpu.ptr].append(cpu)

    def tuer_cpu(s, cpu):
        s.liste_cpus.remove(cpu)
        s.supprimer_cpu_localisation(cpu)

    def tuer_cpu_actuel(s):
        s.tuer_cpu(s.cpu_actuel())

    def next_cpu(s):
        "Met a jour cpu_actuel pour pointer le suivant a executer"
        s.indice_cpu_actuel = (s.indice_cpu_actuel - 1)%(len(s.liste_cpus))

    def inserer_cpu(s, c):
       "Insere le nouveau CPU c dans la liste juste apres celui actuellement pointe"
       s.liste_cpus.insert(s.indice_cpu_actuel + 1, c)
       s.ajouter_cpu_localisation(c)
       s.incremente_cpus_crees()

    def addIndividual(self, index, indiv) :
        for i in range(len(indiv)) :
            self.memoire[index + i % len(self.memoire)] = indiv[i]


    def calculer_densite(s, position):
        #Calcule la densite de CPU a la position donnee
        nombre = 0
        for i in range(position - s.LARGEUR_CALCUL_DENSITE, position + s.LARGEUR_CALCUL_DENSITE+1):
            if i in s.localisation_cpus:
                nombre += len(s.localisation_cpus[i])
        return float(nombre)/float((2*s.LARGEUR_CALCUL_DENSITE+1))

    def tuer_cpus_par_densite(s):
        "Tue tous les CPUs qui sont dans un endroit trop dense\
        Par mesure d'egalite, tous les cpus a tuer le seront en meme temps\
        Dans ce but, on les stocke un par un dans le tableau liste_tues"
        #FONCTION NON TESTEE
        liste_tues = []
        for c in s.liste_cpus:
            densite = s.calculer_densite(c.ptr)
            if densite >= s.SEUIL_DENSITE:
                liste_tues.append(c)
        for i in range(len(liste_tues)-1):
            s.tuer_cpu(liste_tues[i])

    def afficher(self):
        print("===============")
        print("memoire :", self.memoire)
        print("liste CPU :")
        for cpu in self.liste_cpus:
            cpu.afficher_etat()
        print("indice_cpu_actuel :", self.indice_cpu_actuel)
