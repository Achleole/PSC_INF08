import os
import Univers
import NextSite
import Enregistrement
from CPU import *
import Instructions
import CPU
import Statistiques
import NextSite
import matplotlib.pyplot as plt
import numpy as np

import datetime #utilise pour donner un nom par defaut aux fichiers



class Experiment:

    def __init__(self):
        self.folderName = "defaultExperiment" #folderName est le nom du dossier dans lequel on enregistre les graphes
        self.current_ancestor = None
        return

    def test(self, nb_iterations):
        cpus_total, cpus_crees = (self.stats.cpus_total, self.stats.cpus_crees)
        """delta = nb_iterations - len(cpus_total)
        cpus_total += [-1]*delta
        delta = nb_iterations - len(cpus_crees)
        cpus_crees += [-1]*delta
        """
        return (cpus_total, cpus_crees)

    def run(self, iteration=0):
        while self.i < iteration:
            try:
                self.U.cycle()
            except Exception as e:
                print(e)
            self.i += 1
        return self.test(iteration)

    def run2(self, iteration=0):
        "Variation  de run, pour l'experience 2 : a chaque iteration on va compter le nombre d'occurences\
        puis les stocker dans un tableau"
        occurences = [0]*iteration
        while self.i < iteration:
            try:
                self.U.cycle()
            except Exception as e:
                print(e)
            occurences[self.i] = self.compter_genomes(self.current_ancestor, self.U.memoire)
            self.i += 1
        tmp = self.test(iteration)
        return (tmp[0], occurences)

    def setUpForExp(self, m, taille_memoire):
        self.resultats = None #tableau contenant les resultats des experiences 
        "Initialise l'experience et ses variables"
        self.i = 0 #compte le nombre de cycles d'univers a executer
        nextSite = NextSite.NextSite(memLen=taille_memoire)
        self.U = Univers.Univers(nextSite, TAILLE_MEMOIRE=taille_memoire, mutation=m)
        self.stats = Statistiques.Statistiques(self.U)
        self.U.insDict.initialize(Instructions.instructions) 
        eve = Enregistrement.charger_genome('eve') #charge le genome eve
        ancestor = self.U.insDict.toInts(eve) #et convertit en instructions
        self.U.addIndividual(0, ancestor) #on ajoute le genome au debut de la memoire
        c = CPU.CPU(0, self.U)  #on ajoute un CPU pour lire le genome
        c.generation = 1
        self.U.inserer_cpu(c)
        self.replay = Enregistrement.Replay()
        self.replay.univers = self.U

    def setFolderName(self, nom):
        "Change le nom du dossier dans lequell on enregistre les graphes et les resultats"
        self.folderName = nom

    def enregistrer_resultat(self, nom_fichier, taille_memoire, nombre_experiences, nombre_iterations, res):
        "Enregistre sous forme de tableau les resultats. Pour l'instant, on ne peut pas enregistrer dans le fichier\
        les infos de l'experience (taille memoire, nombre d'experiences, etc.) mais seulement le contenu des resultats"
        if not os.path.exists(self.folderName):
            os.makedirs(self.folderName)

        nom_enregistrement = self.folderName + '/' + nom_fichier
        np.save(nom_enregistrement, res)

    def enregistrer_graphe(self, nom_fichier, nombre_iterations, res, titre=""):
        "On enregistre ici les donnees qui sont en fonction de l'iteration donc la longueur de res\
        doit etre egale a nombre_iterations"
        assert len(res) == nombre_iterations
        assert type(titre) is str
        nom_enregistrement = self.folderName + '/' + nom_fichier
        if not os.path.exists(self.folderName):
            os.makedirs(self.folderName)
        abscisses = np.linspace(1, nombre_iterations, nombre_iterations)
        plt.clf()
        plt.plot(abscisses, res)
        if titre != "":
            plt.title(titre)
        else:
            now = datetime.datetime.now()
            titre = str(now.day) + '_' + str(now.month) + '_' + str(now.year) + '_at_' + str(now.hour) + '_' + str(now.minute) + '.png'
        plt.savefig(nom_enregistrement)
        plt.clf()

    def compter_genomes(self, code_genetique, memoire):
        "Compte le nombre d'instances du code passe en argument dans la memoire\
        Actuellement, ne prendra pas en compte un code qui chevaucherait la fin et le debut\
        de la memoire donc le resultat sera decale de 1. Pour l'instant c'est pas tres grave puisqu'on veut\
        faire des statistiques a temps long => beaucoup de codes a priori"
        nombre, l, i = 0, len(code_genetique), 0
        premier_i = 0 #stocke l'indice auquel commence le premier code qu'on a trouve
        #va servir a chercher le code si il chevauche la fin et le debut de la memoire
        res = 0
        #res stocke l'indice renvoye par KMP (et -1 si le code est pas trouve)

        while res != -1:
            res = knuth_morris_pratt(memoire, code_genetique, debut=i)
            i = res + l #on commencera la recherche juste apres la derniere recherche
            if res != -1:
                if nombre == 0:
                    premier_i = res
                nombre += 1
        return nombre

    def experiment1(self, TAILLE_MEMOIRE=None, NOMBRE_EXPERIENCES = 50, NOMBRE_ITERATIONS = 10000):
        if TAILLE_MEMOIRE == None :
            TAILLE_MEMOIRE 	= [250, 500, 1000, 2000, 3000, 4000] 
        #NOMBRE_EXPERIENCESnombre de fois qu'on va faire l'experience pour chaque taille memoire
        #NOMBRE_ITERATIONS meme nombre de cycles d'univers pour chaque experience

        for t_m in TAILLE_MEMOIRE:
            print("Taille memoire = ", t_m)
            ord1 = [0]*NOMBRE_ITERATIONS #stocke le nombre de cpus total
            ord2 = [0]*NOMBRE_ITERATIONS #stocje le nombre de cpus crees a chaque iteration

            for e in range(NOMBRE_EXPERIENCES):
                print('-> Experience numero ', str(e+1))
                self.setUpForExp(0.0, t_m)
                #total, crees = self.run(NOMBRE_ITERATIONS)
                nom = "Exp/exp1-nbexp"+str(NOMBRE_EXPERIENCES)+"-nbiter"+str(NOMBRE_ITERATIONS)+"-n"
                self.replay.openWrite(nom+str(e))
                self.replay.cycleAndSave(NOMBRE_ITERATIONS)
                for i in range(NOMBRE_ITERATIONS):
                    ord1[i] += self.stats.cpus_total[i]
                    ord2[i] += self.stats.cpus_crees[i]

            ord1 = [float(x)/NOMBRE_EXPERIENCES for x in ord1]
            ord2 = [float(y)/NOMBRE_EXPERIENCES for y in ord2]

            nom_fichier = "" + str(t_m) + "_crees"
            self.enregistrer_graphe(nom_fichier, NOMBRE_ITERATIONS, ord2)
            nom_fichier = "" + str(t_m) + "_total"
            plt.clf()
            self.enregistrer_graphe(nom_fichier, NOMBRE_ITERATIONS, ord1)

            print("Fini")

    def experiment2(self, TAILLE_MEMOIRE=None, NOMBRE_EXPERIENCES = 50, NOMBRE_ITERATIONS = 10000):
        "Dans cette experience, on va comparer l'evolution du nombre de CPUs en vie et le nombre"
        if TAILLE_MEMOIRE == None:
            TAILLE_MEMOIRE = [250, 500, 1000, 2000, 3000, 4000]

        for t_m in TAILLE_MEMOIRE:
            print("Taille memoire = ", t_m)
            ord1 = [0]*NOMBRE_ITERATIONS
            ord2 = [0]*NOMBRE_ITERATIONS

            for e in range(NOMBRE_EXPERIENCES):
                print('-> Experience numero ', str(e+1))
                self.setUpForExp(0.0, t_m)
                eve = Enregistrement.charger_genome("eve")
                self.current_ancestor = self.U.insDict.toInts(eve) #l'ancetre sera cherche dans la memoire dans la suite
                total, occurences = self.run2(NOMBRE_ITERATIONS)
                for i in range(NOMBRE_ITERATIONS):
                    ord1[i] += total[i]
                    ord2[i] += occurences[i]
                    #apres la i eme iteration

            ord1 = [float(x)/NOMBRE_EXPERIENCES for x in ord1]
            ord2 = [float(y)/NOMBRE_EXPERIENCES for y in ord2]

            nom_fichier = "" + str(t_m) + "_occurences"
            self.enregistrer_graphe(nom_fichier, NOMBRE_ITERATIONS, ord2)
            nom_fichier = "" + str(t_m) + "_total"
            plt.clf()
            self.enregistrer_graphe(nom_fichier, NOMBRE_ITERATIONS, ord1)

            print("Fini")   