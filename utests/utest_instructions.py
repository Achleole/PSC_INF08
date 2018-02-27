import unittest
import Univers
import CPU
import NextSiteTest
import Enregistrement
import Instructions
import CheckCPU

class TestInstructions(unittest.TestCase):
    def setUp(self):
        self.u = Univers.Univers(NextSiteTest.NextSiteTest(memLen=300), TAILLE_MEMOIRE=300)
        self.u.insDict.initialize(Instructions.instructions)
        eve = Enregistrement.charger_genome('eve')
        self.ancestor = self.u.insDict.toInts(eve)
        self.u.addIndividual(0, self.ancestor)
        self.c = CPU.CPU(0, self.u)
        CheckCPU.checkCPU(self, self.c, 0, 0, 0, 0, 0, 0, [0]*CPU.TAILLE_STACK)
        self.u.inserer_cpu(self.c)

    def test_pas_a_pas(self) :
        s = [0]*CPU.TAILLE_STACK
        CheckCPU.checkCPU(self, self.c, 0,0,0,0,0,0, s)
