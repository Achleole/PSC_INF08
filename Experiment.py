import os
import Univers
import NextSite
from Enregistrement import *
from CPU import *
import Instructions
import CPU
import Statistiques
import NextSite
import matplotlib.pyplot as plt
import numpy as np



class Experiment:

    def __init__(self):
        self.folderName = "defaultExperiment" #folderName est le nom du dossier dans lequel on enregistre les graphes
        return

    def test(self):
        return (self.stats.cpus_total, self.stats.cpus_crees)

    def run(self, iteration=0):
        while self.i < iteration:
            self.U.cycle()
            self.i += 1
        return self.test()

    def setUpForExp(self, m, taille_memoire):
        self.resultats = None #tableau contenant les resultats des experiences 
        "Initialise l'experience et ses variables"
        self.i = 0 #compte le nombre de cycles d'univers a executer
        nextSite = NextSite.NextSite()
        self.U = Univers.Univers(nextSite, TAILLE_MEMOIRE=taille_memoire, mutation=m)
        self.stats = Statistiques.Statistiques(self.U)
        self.U.insDict.initialize(Instructions.instructions) 
        eve = charger_genome('eve') #charge le genome eve
        ancestor = self.U.insDict.toInts(eve) #et convertit en instructions
        self.U.addIndividual(0, ancestor) #on ajoute le genome au debut de la memoire
        c = CPU.CPU(0, self.U)  #on ajoute un CPU pour lire le genome
        c.generation = 1
        self.U.inserer_cpu(c)

    def setFolderName(self, nom):
        self.folderName = nom

    def enregistrer_resultat(self, nom_fichier, taille_memoire, nombre_experiences, nombre_iterations, res):
        "Enregistre sous forme de tableau les resultats"
        if not os.path.exists(self.folderName):
            os.makedirs(self.folderName)

        nom_enregistrement = self.folderName + '/' + nom_fichier
        f = open(nom_enregistrement, 'w')
        np.savetxt(f, res) #bug a cet endroit : le format entre le tableau est incompatible avec le format utilise 
        #par la fonction
        f.write('NB_EXPERIENCES : ' + str(nombre_experiences) + 'NB_ITERATIONS' +   str(nombre_iterations))
        

    def enregistrer_graphe(self, nom_fichier, nombre_iterations, res):
        nom_enregistrement = self.folderName + '/' + nom_fichier
        if not os.path.exists(self.folderName):
            os.makedirs(self.folderName)
        abscisses = np.linspace(1, nombre_iterations, nombre_iterations)
        plt.clf()
        plt.plot(abscisses, res)
        plt.savefig(nom_enregistrement)
        plt.clf()


    def experiment1(self, TAILLE_MEMOIRE=None, NOMBRE_EXPERIENCES = 50, NOMBRE_ITERATIONS = 10000):
        if TAILLE_MEMOIRE == None :
            TAILLE_MEMOIRE 		= [250, 500, 1000, 2000, 3000, 4000] 
        #NOMBRE_EXPERIENCESnombre de fois qu'on va faire l'experience pour chaque taille memoire
        #NOMBRE_ITERATIONS meme nombre de cycles d'univers pour chaque experience

        for t_m in TAILLE_MEMOIRE:
            print("Taille memoire = ", t_m)
            ord1 = [0]*NOMBRE_ITERATIONS #stocke le nombre de cpus total
            ord2 = [0]*NOMBRE_ITERATIONS #stocje le nombre de cpus crees a chaque iteration

            for e in range(NOMBRE_EXPERIENCES):
                print('-> Experience numero ', str(e+1))
                self.SetUpForExp(0.0, t_m)
                total, crees = self.run(NOMBRE_ITERATIONS)
                for i in range(NOMBRE_ITERATIONS):
                    ord1[i] += total[i]
                    ord2[i] += crees[i]

            abscisses = np.linspace(1, NOMBRE_ITERATIONS, NOMBRE_ITERATIONS)
            ord1 = [float(x)/float(NOMBRE_EXPERIENCES) for x in ord1]
            ord2 = [float(x)/float(NOMBRE_EXPERIENCES) for x in ord2] #on fait la moyenne sur les experiences
            plt.clf()
            plt.plot(abscisses, ord1)
            plt.plot(abscisses, ord2)
            titre = "Nombre d'experiences = " + str(NOMBRE_EXPERIENCES) + ". Taille de la memoire = " + str(t_m)
            plt.title(titre)
            nom_fichier ="Resultats/cpus_total_mutation_0_taille_memoire_" + str(t_m) + ".png"
            plt.savefig(nom_fichier)

            print("Fini")

e = Experiment()
e.setFolderName("dossier_test")
res = np.array([42.0, 0.0])
e.enregistrer_resultat("fichier_test", 0, 0 ,0, res)
