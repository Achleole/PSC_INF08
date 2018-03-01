import unittest
import Univers
import CPU
import NextSiteTest
import Enregistrement
import Instructions
import CheckCPU

class TestInstructions(unittest.TestCase):
    def setUp(self):
        self.u = Univers.Univers(NextSiteTest.NextSiteTest(memLen=26000), TAILLE_MEMOIRE=26000)
        self.u.insDict.initialize(Instructions.instructions)
        eve = Enregistrement.charger_genome('eve')
        self.ancestor = self.u.insDict.toInts(eve)
        self.u.addIndividual(0, self.ancestor)
        self.c = CPU.CPU(0, self.u)
        CheckCPU.checkCPU(self, self.c, 0, 0, 0, 0, 0, 0, [0]*CPU.TAILLE_STACK)
        self.u.inserer_cpu(self.c)

    def test_recopies(self):
        for i in range(502*9) : #il faut que toutes les lignees de CPUs aient le temps de se recopier 9 fois
            self.u.executer_cpus()
        self.assertEqual(len(self.u.liste_cpus), 2**9)

    def test_cycles(self):
        for i in range(502*9) : #il faut que toutes les lignees de CPUs aient le temps de se recopier 9 fois
            self.u.cycle()
        self.assertEqual(len(self.u.liste_cpus), 2**9)

    def test_pas_a_pas(self) :
        s = [0]*CPU.TAILLE_STACK
        CheckCPU.checkCPU(self, self.c, 0,0,0,0,0,0, s)
        for i in range(5) :
            self.c.execute() #nop0
        CheckCPU.checkCPU(self, self.c, 5, 0, 0, 0, 0, 0, s)
        self.c.execute() #pushB
        CheckCPU.checkCPU(self, self.c, 6, 0, 0, 0, 0, 1, s)
        self.c.execute()  # rand
        CheckCPU.checkCPU(self, self.c, 7, 50, 0, 0, 0, 1, s)
        self.c.execute()  # pushA
        s[1] = 50
        CheckCPU.checkCPU(self, self.c, 8, 50, 0, 0, 0, 2, s)
        self.c.execute()  # popD
        CheckCPU.checkCPU(self, self.c, 9, 50, 0, 0, 50, 1, s)
        self.c.execute()  # zero
        CheckCPU.checkCPU(self, self.c, 10, 50, 0, 0, 50, 1, s)
        self.c.execute()  # not0
        CheckCPU.checkCPU(self, self.c, 11, 50, 0, 1, 50, 1, s)
        self.c.execute()  # shl
        CheckCPU.checkCPU(self, self.c, 12, 50, 0, 2, 50, 1, s)
        self.c.execute()  # not0
        CheckCPU.checkCPU(self, self.c, 13, 50, 0, 3, 50, 1, s)
        for i in range(4) :
            self.c.execute()  # shl
            CheckCPU.checkCPU(self, self.c, 14+i, 50, 0, 3*(2**(i+1)), 50, 1, s)
        for i in range(3) :
            self.c.execute()  # nop
            CheckCPU.checkCPU(self, self.c, 18+i, 50, 0, 48, 50, 1, s)

        self.c.execute()  # read
        s[1] = 0
        CheckCPU.checkCPU(self, self.c, 21, 50, 0, 48, 50, 2, s)
        self.c.execute()  # write
        CheckCPU.checkCPU(self, self.c, 22, 50, 0, 48, 50, 1, s)
        self.assertEqual(self.u.memoire[self.c.ax], 0)
        self.c.execute()  # incA
        CheckCPU.checkCPU(self, self.c, 23, 51, 0, 48, 50, 1, s)
        self.c.execute()  # incB
        CheckCPU.checkCPU(self, self.c, 24, 51, 1, 48, 50, 1, s)
        #pas fini
