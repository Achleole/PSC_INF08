import unittest
import Univers
import NextSite
from Enregistrement import *
import CPU
import Instructions
import CPU
import Statistiques
import NextSite
import random

class TestCPU(unittest.TestCase):
    def setUp(self):
        self.i = 0
        self.U = Univers.Univers( NextSite.NextSite())
        self.U.insDict.initialize(Instructions.instructions)
        self.U.addIndividual(0, self.U.insDict.toInts(charger_genome('eve')))
        self.U.inserer_cpu(CPU.CPU(0, self.U))
        self.N=random.randint(100,200)
        self.replay=Replay()
    def test_conversion_CPU(self):
        for i in range(self.N):
            self.U.cycle()

        for cpu in self.U.liste_cpus:
            print(cpu.id, intToCPU(CPUtoInt(cpu),self.U).id)
            self.assertTrue(cpu == intToCPU(CPUtoInt(cpu),self.U))
        self.setUp()
    def test_photo(self):
        fichier = "temp.tierra"
        self.replay.univers=self.U
        self.replay.openWrite(fichier)
        self.replay.univers=self.U.copy()
        self.replay.photo()
        self.replay.openLoad(fichier)
        self.assertTrue(self.replay.loadPhoto()==self.U)
    def test_univers_copy(self):
        for i in range(10):
            for i in range(100):
                self.U.cycle()
            self.assertTrue(self.U == self.U.copy())
        self.setUp()
    def test_sauvegarde(self):
        fichier = "temp.tierra"
        self.replay.univers=self.U
        memoire=[self.U.copy()]
        self.replay.openWrite(fichier)
        for i in range(self.N):
            self.replay.runAndSave(1)
            memoire.append(self.replay.univers.copy())
        self.U=self.replay.univers.copy()
        nouveau=[]
        self.replay.openLoad(fichier)
        for i in range(self.N):
            self.replay.forward(1)
            nouveau.append(self.replay.univers.copy())
            if not(self.replay.univers==memoire[i+1]):
                print("je sers a rien")

        self.assertTrue(self.replay.univers==self.U)