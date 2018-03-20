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
        return

    def test(self):
        return (self.stats.cpus_total, self.stats.cpus_crees)

    def run(self, iteration=0):
        while self.i < iteration:
            self.U.cycle()
            self.i += 1
        return self.test()

    def setUpForExp(self, m, taille_memoire):
        self.i = 0
        nextSite = NextSite.NextSite()
        self.U = Univers.Univers(nextSite, TAILLE_MEMOIRE=taille_memoire, mutation=m)
        self.stats = Statistiques.Statistiques(self.U)
        self.U.insDict.initialize(Instructions.instructions)
        eve = charger_genome('eve')
        ancestor = self.U.insDict.toInts(eve)
        self.U.addIndividual(0, ancestor)
        c = CPU.CPU(0, self.U)
        c.generation = 1
        self.U.inserer_cpu(c)

    def exeriment1(self, TAILLE_MEMOIRE=None, NOMBRE_EXPERIENCES = 50, NOMBRE_ITERATIONS 	= 10000):
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