import unittest
import Univers
import CPU
import NextSiteTest
import Instructions
import Enregistrement

class TestFrontiere(unittest.TestCase):
    def setUp(self):
        self.U = Univers.Univers(NextSiteTest.NextSiteTest(memLen=120), TAILLE_MEMOIRE=120)
        self.U.insDict.initialize(Instructions.instructions)
        eve = Enregistrement.charger_genome('eve')
        self.ancestor = self.U.insDict.toInts(eve)
        self.U.addIndividual(0, self.ancestor)
        self.c = CPU.CPU(0, self.U)
        self.U.inserer_cpu(self.c)

    def test_copieSimple(self) :
        for i in range(502):
            self.c.execute()
        self.assertEqual(self.U.memoire, (self.ancestor+[2,2])*2+[2]*20)

    def test_copieDepasse(self) :
        for i in range(999):
            self.c.execute()
        expectedRes = self.ancestor[20:] + self.ancestor[28:] + [2,2] + self.ancestor + [2,2] + self.ancestor[:20]
        self.assertEqual(self.U.memoire, expectedRes)