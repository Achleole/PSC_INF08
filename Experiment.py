import os
import Univers
import NextSite
import SimpleNextSite
import Enregistrement
from CPU import *
import Instructions
import CPU
import Statistiques
import NextSite
import matplotlib.pyplot as plt
import numpy as np

import InstructionsSuperrwshll

import datetime #utilise pour donner un nom par defaut aux fichiers



class Experiment:

    def __init__(self, dossier="defaultExperiment", enregistrerBool=False):

        self.folderName = dossier #folderName est le nom du dossier dans lequel on enregistre les graphes
        self.current_ancestor = None
        self.lcd = 23 #23 : valeur par defaut de la largeur de LARGEUR_CALCUL_DENSITE
        self.enregistrerBool = enregistrerBool #est-ce qu'on enregistre les experiences ou non ?
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
            if self.i % 100 == 0:
                print("iteration numero ", self.i, "Nombre de CPU", len(self.univers.liste_cpus))
        return self.test(iteration)

    def run2(self, iteration=0, genome=None):
        if genome == None:
            genome = self.current_ancestor
        print("genome : ", genome)

        "Variation  de run, pour l'experience 2 : a chaque iteration on va compter le nombre d'occurences\
        puis les stocker dans un tableau"
        occurences = [0]*iteration
        while self.i < iteration:
            try:
                self.U.cycle()
            except Exception as e:
                print(e)
            occurences[self.i] = self.compter_genomes(genome, self.U.memoire)
            self.i += 1
        tmp = self.test(iteration)
        return (tmp[0], occurences)

    def setUpForExp(self, m, taille_memoire, nextsiteclasse, fichier='eve', InstFichier=Instructions, posInit=0):
        #nextsiteclasse est la classe NextSite qu'on utilise : ca peut etre NextSite.NextSite ou NextSite.SimpleNextSite
        # m est le taux de mutation
        self.resultats = None #tableau contenant les resultats des experiences 
        "Initialise l'experience et ses variables"
        self.i = 0 #compte le nombre de cycles d'univers a executer
        nextSite = nextsiteclasse(memLen=taille_memoire)
        self.U = Univers.Univers(nextSite, TAILLE_MEMOIRE=taille_memoire, mutation=m)
        self.U.LARGEUR_CALCUL_DENSITE = self.lcd
        self.stats = Statistiques.Statistiques(self.U)
        self.U.insDict.initialize(InstFichier.instructions) 
        eve = Enregistrement.charger_genome(fichier) #charge le genome eve
        ancestor = self.U.insDict.toInts(eve) #et convertit en instructions
        self.current_ancestor = ancestor
        self.U.addIndividual(posInit , ancestor) #on ajoute le genome au debut de la memoire
        c = CPU.CPU(posInit, self.U)  #on ajoute un CPU pour lire le genome
        c.generation = 1
        self.U.inserer_cpu(c)
        self.replay = Enregistrement.Replay()
        self.replay.univers = self.U

    def setFolderName(self, nom):
        "Change le nom du dossier dans lequell on enregistre les graphes et les resultats"
        self.folderName = nom

    def setLargeurCalculDensite(self, lcd):
        "A apeller avant les fonctions des experiences "
        self.lcd = lcd

    def setEnregistrerBool(self, b):
        self.enregistrerBool = b

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

    def compter_instruction(self, instru, memoire):
        total = 0
        for c in memoire:
            if c == instru:
                total += 1
        return total

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

    def run_experiment_1(self, TAILLE_MEMOIRE, NOMBRE_EXPERIENCES, NOMBRE_ITERATIONS, nextsitefonction, fichier_gene, fichier_ins):
        #nextsite : fonction nextsite qu'on utilise (la normale ou SimpleNextSite)
        for t_m in TAILLE_MEMOIRE:
            print("Taille memoire = ", t_m)
            ord1 = [0]*NOMBRE_ITERATIONS #stocke le nombre de cpus total
            ord2 = [0]*NOMBRE_ITERATIONS #stocke le nombre de cpus crees a chaque iteration

            for e in range(NOMBRE_EXPERIENCES):
                print('-> Experience numero ', str(e+1))
                self.setUpForExp(0.0, t_m, nextsitefonction, fichier=fichier_gene, InstFichier=fichier_ins)
                
                #total, crees = self.run(NOMBRE_ITERATIONS)
                
                if self.enregistrerBool:
                    nom = self.folderName + "/exp1-nbexp"+str(NOMBRE_EXPERIENCES)+"-nbiter"+str(NOMBRE_ITERATIONS)+"-n"
                    self.replay.openWrite(nom+str(e))
                    self.replay.cycleAndSave(NOMBRE_ITERATIONS)
                else:
                    self.run(NOMBRE_ITERATIONS) #experience 1 -> on appelle la fonction run
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

    def run_experiment_2(self, TAILLE_MEMOIRE, NOMBRE_EXPERIENCES, NOMBRE_ITERATIONS, nextsitefonction, fichier_gene, fichier_ins):
        eve = Enregistrement.charger_genome("eve")
        for t_m in TAILLE_MEMOIRE:
            print("Taille memoire = ", t_m)
            ord1 = [0]*NOMBRE_ITERATIONS #stocke le nombre de cpus total
            ord2 = [0]*NOMBRE_ITERATIONS #stocje le nombre de cpus crees a chaque iteration

            for e in range(NOMBRE_EXPERIENCES):
                print('-> Experience numero ', str(e+1))
                self.setUpForExp(0.0, t_m, nextsitefonction, fichier=fichier_gene, InstFichier=fichier_ins)
                if self.enregistrerBool:
                    total = []
                    occurences = []
                    nom = self.folderName + "/exp2-nbexp" + str(NOMBRE_EXPERIENCES) + "-nbiter" + str(NOMBRE_ITERATIONS) + "-n"
                    self.replay.openWrite(nom + str(e))
                    for i in range(NOMBRE_ITERATIONS):
                        self.replay.cycleAndSave(1)
                        total.append(len(self.U.liste_cpus))
                        occurences.append(self.compter_genomes(ancestor, self.U.memoire))
                else:
                        total, occurences = self.run2(NOMBRE_ITERATIONS)

                for i in range(NOMBRE_ITERATIONS):
                    ord1[i] += total[i]
                    ord2[i] += occurences[i]


            ord1 = [float(x)/NOMBRE_EXPERIENCES for x in ord1]
            ord2 = [float(y)/NOMBRE_EXPERIENCES for y in ord2]

            nom_fichier = "" + str(t_m) + "_crees"
            self.enregistrer_graphe(nom_fichier, NOMBRE_ITERATIONS, ord2)
            nom_fichier = "" + str(t_m) + "_occurences"
            plt.clf()
            self.enregistrer_graphe(nom_fichier, NOMBRE_ITERATIONS, ord1)

            print("Fini")

    def experiment1(self, TAILLE_MEMOIRE=None, NOMBRE_EXPERIENCES = 50, NOMBRE_ITERATIONS = 10000, fichier_gene='eve', fichier_ins=Instructions):
        if TAILLE_MEMOIRE == None :
            TAILLE_MEMOIRE 	= [250, 500, 1000, 2000, 3000, 4000] 
        #NOMBRE_EXPERIENCESnombre de fois qu'on va faire l'experience pour chaque taille memoire
        #NOMBRE_ITERATIONS meme nombre de cycles d'univers pour chaque experience
        self.run_experiment_1(TAILLE_MEMOIRE, NOMBRE_EXPERIENCES, NOMBRE_ITERATIONS, NextSite.NextSite, fichier_gene, fichier_ins)


    def experiment2(self, TAILLE_MEMOIRE=None, NOMBRE_EXPERIENCES = 50, NOMBRE_ITERATIONS = 10000, fichier_gene='eve', fichier_ins=Instructions):
        "Dans cette experience, on va comparer l'evolution du nombre de CPUs en vie et le nombre"
        if TAILLE_MEMOIRE == None:
            TAILLE_MEMOIRE = [250, 500, 1000, 2000, 3000, 4000]
        self.run_experiment_2(TAILLE_MEMOIRE, NOMBRE_EXPERIENCES, NOMBRE_ITERATIONS, NextSite.NextSite, fichier_gene, fichier_ins)
  

    def experimentSimpleNextSite(self, TAILLE_MEMOIRE=None, NOMBRE_EXPERIENCES = 50, NOMBRE_ITERATIONS = 10000, fichier_gene='eve', fichier_ins=Instructions):

        if TAILLE_MEMOIRE == None :
            TAILLE_MEMOIRE  = [250, 500, 1000, 2000, 3000, 4000] 
        self.run_experiment_1(TAILLE_MEMOIRE, NOMBRE_EXPERIENCES, NOMBRE_ITERATIONS, SimpleNextSite.SimpleNextSite, fichier_gene, fichier_ins)

    def experiment2SimpleNextSite(self, TAILLE_MEMOIRE=None, NOMBRE_EXPERIENCES = 50, NOMBRE_ITERATIONS = 10000, fichier_gene='eve', fichier_ins=Instructions):
        "Dans cette experience, on va comparer l'evolution du nombre de CPUs en vie et le nombre"
        if TAILLE_MEMOIRE == None:
            TAILLE_MEMOIRE = [250, 500, 1000, 2000, 3000, 4000]

        self.run_experiment_2(TAILLE_MEMOIRE, NOMBRE_EXPERIENCES, NOMBRE_ITERATIONS, SimpleNextSite.SimpleNextSite, fichier_gene, fichier_ins)



    def setUpForExp_Comparaison_Genomes(self, t_m, nb_eve, nb_eve_meilleur):
        "On va ajouter un certain nombre de copies du code genetique de base et voir l'evolution"
        self.resultats = None
        "Initialise l'experience et ses variables"
        self.i = 0 
        nextSite = NextSite.NextSite(memLen=t_m) #on va toujours utiliser le NextSite
        self.U = Univers.Univers(nextSite, TAILLE_MEMOIRE=t_m, mutation=0.0)
        self.U.LARGEUR_CALCUL_DENSITE = self.lcd
        self.stats = Statistiques.Statistiques(self.U)
        self.U.insDict.initialize(InstructionsSuperrwshll.instructions) #on va utiliser le set d'instructions dote des deux
        #instructions en plus
        eve = Enregistrement.charger_genome('eve') 
        eve_meilleur = Enregistrement.charger_genome('eve_meilleur') #on charge aussi le genome "ameliore"
        self.ancestor_eve = self.U.insDict.toInts(eve) 
        self.ancestor_eve_meilleur = self.U.insDict.toInts(eve_meilleur)

        #on va placer les genomes les uns a la suite des autres avec un peu d'espacement, car de toute 
        #facon la recopie se fait de maniere aleatoire

        longueur_eve = 50
        for i in range(nb_eve):
            indice = 2*i*longueur_eve
            self.U.addIndividual(indice, self.ancestor_eve) #on met un facteur deux pour bien pouvoir separer les genomes
            c = CPU.CPU(indice, self.U)
            self.U.inserer_cpu(c)
        for i in range(nb_eve_meilleur):
            indice = 2*i*longueur_eve + (t_m//2) #on les place a peu pres a la moitie de la memoire
            self.U.addIndividual(indice, self.ancestor_eve_meilleur)
            c = CPU.CPU(indice, self.U)
            self.U.inserer_cpu(c)

    def run_comparaison_genomes(self, NOMBRE_ITERATIONS):
        occurences_eve = []
        occurences_eve_meilleur = []
        for self.i in range(NOMBRE_ITERATIONS):
            self.U.cycle()
            if self.i % 250 == 0:
                print("Iteration numero :", self.i)
                print("--> Nombre de CPUs : ", len(self.U.liste_cpus))
                occurences_eve.append(self.compter_genomes(self.eve_ancestor, self.U.memoire))
                occurences_eve_meilleur.append(self.compter_genomes(self.ancestor_eve_meilleur, self.U.memoire)) #38 correspond a l'instruction rw, il y en a autant ici grosso modo) que de 
                #copies du genome. On va prendre un tres gros espace memoire pour etre sur  

            #on ne va compter les occurences que toutes les 250 iterations puisqu'il faut environ 500
            #pour se reproduire, ca ne sert donc a rien de mesurer trop souvent
        return (occurences_eve, occurences_eve_meilleur)

    def experiment_comparaison_genomes(self, TAILLE_MEMOIRE=50000, NOMBRE_ITERATIONS=20000, nb_eve=1, nb_eve_meilleur=1):
        "Ici, on ne va faire qu'une seule experience car on ne veut pas faire de resultats avec bcp d'experiences, ca va prendre trop de temps \
        Dans un premier temps, on ne va pas mettre de taux de mutation"
        self.setUpForExp_Comparaison_Genomes(TAILLE_MEMOIRE, nb_eve, nb_eve_meilleur)

        #on va charger en memoire les genomes pour pouvoir les compter ensuite
        eve = Enregistrement.charger_genome('eve') 
        eve_meilleur = Enregistrement.charger_genome('eve_meilleur') #on charge aussi le genome "ameliore"
        self.eve_ancestor = self.U.insDict.toInts(eve) 
        self.ancestor_meilleur = self.U.insDict.toInts(eve_meilleur)

        occurences_eve, occurences_eve_meilleur = self.run_comparaison_genomes(NOMBRE_ITERATIONS)
        ab = np.linspace(1, len(occurences_eve), len(occurences_eve))
        plt.plot(ab, occurences_eve, label='eve')
        plt.plot(ab, occurences_eve_meilleur, label='eve_meilleur')
        plt.legend(loc='upper left')
        if not os.path.exists(self.folderName):
            os.makedirs(self.folderName)
        plt.savefig(self.folderName + '/comparaison_genomes_' + str(TAILLE_MEMOIRE) + '_' + str(NOMBRE_ITERATIONS))