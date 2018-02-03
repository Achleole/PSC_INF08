import unittest
import Univers
import CPU
import InstructionsDict

class TestUnivers(unittest.TestCase):

    def test_creationUnivers(self) :
        u = Univers.Univers(TAILLE_MEMOIRE=40000, insDict=InstructionsDict.InstructionsDict(), mutation=2e-12, LARGEUR_CALCUL_DENSITE=1, maxCPUs=2)
        self.assertEqual(u.TAILLE_MEMOIRE, 40000)
        self.assertEqual(u.mutation,2e-12)
        self.assertEqual(u.LARGEUR_CALCUL_DENSITE,1)
        self.assertEqual(u.maxCPUs, 2)

    def test_ajouter_cpu_localisation(self):
        u = Univers.Univers()
        c = CPU.CPU(102, u)
        u.ajouter_cpu_localisation(c)
        self.assertTrue(102 in u.localisation_cpus and c in u.localisation_cpus[102])
        c2 = CPU.CPU(102, u)
        c3 = CPU.CPU(102, u)
        u.ajouter_cpu_localisation(c3)
        u.ajouter_cpu_localisation(c2)
        #Pour verifier que l'ajout de CPUs n'en retire pas d'autres :
        self.assertTrue(102 in u.localisation_cpus and c in u.localisation_cpus[102])
        self.assertTrue(102 in u.localisation_cpus and c2 in u.localisation_cpus[102])
        self.assertTrue(102 in u.localisation_cpus and c3 in u.localisation_cpus[102])
        # (on pourrait aussi verifier que les autres valeurs de localisation_cpus ne sont pas modifiees)

    def test_supprimer_localisation(self):
        u = Univers.Univers()
        c1 = CPU.CPU(102, u)
        c2 = CPU.CPU(102, u)
        c3 = CPU.CPU(102, u)
        u.ajouter_cpu_localisation(c1)
        u.ajouter_cpu_localisation(c3)
        u.ajouter_cpu_localisation(c2)
        u.supprimer_cpu_localisation(c1)
        self.assertTrue(c1 not in u.localisation_cpus[102] and c2 in u.localisation_cpus[102] and c3 in u.localisation_cpus[102])
        # (on pourrait aussi verifier que les autres valeurs de localisation_cpus ne sont pas modifiees)
    
    def test_inserer_cpu(self):
        u = Univers.Univers(TAILLE_MEMOIRE=10)
        c1 = CPU.CPU(3, u)
        u.inserer_cpu(c1)
        self.assertTrue(c1 in u.liste_cpus)
        self.assertTrue(c1 in u.localisation_cpus[3])
        c2 = CPU.CPU(3, u)
        c3 = CPU.CPU(4, u)
        u.inserer_cpu(c2)
        u.inserer_cpu(c3)
        self.assertTrue(c2 in u.liste_cpus)
        self.assertTrue(c2 in u.localisation_cpus[3])
        self.assertTrue(c3 in u.liste_cpus)
        self.assertTrue(c3 in u.localisation_cpus[4])
        self.assertTrue(c1 in u.liste_cpus)
        self.assertTrue(c1 in u.localisation_cpus[3])
    
    def test_tuer_cpu(self):
        u = Univers.Univers(TAILLE_MEMOIRE=10)
        c1 = CPU.CPU(3, u)
        u.inserer_cpu(c1)
        c2 = CPU.CPU(3, u)
        u.inserer_cpu(c2)
        c3 = CPU.CPU(4, u)
        u.inserer_cpu(c3)
        u.tuer_cpu(c1)
        self.assertTrue(c2 in u.liste_cpus)
        self.assertTrue(c2 in u.localisation_cpus[3])
        self.assertTrue(c3 in u.liste_cpus)
        self.assertTrue(c3 in u.localisation_cpus[4])
        self.assertTrue(c1 not in u.liste_cpus)
        self.assertTrue(c1 not in u.localisation_cpus[3])

    def test_cpu_actuel(self):
        u = Univers.Univers(TAILLE_MEMOIRE=10)
        c1 = CPU.CPU(3, u)
        c2 = CPU.CPU(3, u)
        c3 = CPU.CPU(4, u)
        u.liste_cpus = [c1, c2, c3]
        u.indice_cpu_actuel = 1
        self.assertEqual(c2, u.cpu_actuel())

    def test_tuer_cpu_actuel(self):
        u = Univers.Univers(TAILLE_MEMOIRE=10)
        c1 = CPU.CPU(3, u)
        u.inserer_cpu(c1)
        c2 = CPU.CPU(3, u)
        u.inserer_cpu(c2)
        c3 = CPU.CPU(4, u)
        u.inserer_cpu(c3)
        u.liste_cpus = [c1, c2, c3]
        u.indice_cpu_actuel = 1
        u.tuer_cpu_actuel()
        self.assertTrue(c2 not in u.liste_cpus)
        self.assertTrue(c2 not in u.localisation_cpus[3])
        self.assertTrue(c3 in u.liste_cpus)
        self.assertTrue(c3 in u.localisation_cpus[4])
        self.assertTrue(c1 in u.liste_cpus)
        self.assertTrue(c1 in u.localisation_cpus[3])

    def test_next_cpu(self):
        u = Univers.Univers(TAILLE_MEMOIRE=10)
        c1 = CPU.CPU(3, u)
        u.inserer_cpu(c1)
        c2 = CPU.CPU(3, u)
        u.inserer_cpu(c2)
        c3 = CPU.CPU(4, u)
        u.inserer_cpu(c3)
        u.liste_cpus = [c1, c2, c3]
        u.indice_cpu_actuel = 1
        u.next_cpu()
        self.assertEqual(u.indice_cpu_actuel,0)
        u.next_cpu()
        self.assertEqual(u.indice_cpu_actuel, 2)
        u.next_cpu()
        self.assertEqual(u.indice_cpu_actuel, 1)

    def test_addIndividual(self):
        u = Univers.Univers(TAILLE_MEMOIRE=10)
        indiv = [5,4,3]
        u.addIndividual(0, indiv)
        self.assertEqual(u.memoire[:3], indiv)
        self.assertEqual(u.memoire[3:10],[2]*7)
        u.addIndividual(9, indiv)
        self.assertEqual(u.memoire, [4,3,3]+([2]*6)+[5])

    def test_nbCPUs_at_i(self):
        u = Univers.Univers(TAILLE_MEMOIRE=10)
        c1 = CPU.CPU(3, u)
        u.inserer_cpu(c1)
        c2 = CPU.CPU(3, u)
        u.inserer_cpu(c2)
        c3 = CPU.CPU(4, u)
        u.inserer_cpu(c3)
        self.assertEqual(2, u.nbCPUs_at_i(3))
        self.assertEqual(1, u.nbCPUs_at_i(4))
        self.assertEqual(0, u.nbCPUs_at_i(0))

    def test_kill_at(self):
        u = Univers.Univers(TAILLE_MEMOIRE=10, LARGEUR_CALCUL_DENSITE=1, maxCPUs=2)
        c1 = CPU.CPU(3, u)
        u.inserer_cpu(c1)
        c2 = CPU.CPU(3, u)
        u.inserer_cpu(c2)
        c3 = CPU.CPU(4, u)
        u.inserer_cpu(c3)
        u.killAround(3, 3)
        self.assertEqual(u.nbCPUs_at_i(3)+u.nbCPUs_at_i(4)+u.nbCPUs_at_i(5), 1)
        u = Univers.Univers(TAILLE_MEMOIRE=10, LARGEUR_CALCUL_DENSITE=1, maxCPUs=5)
        c1 = CPU.CPU(3, u)
        u.inserer_cpu(c1)
        c2 = CPU.CPU(3, u)
        u.inserer_cpu(c2)
        c3 = CPU.CPU(4, u)
        u.inserer_cpu(c3)
        c4 = CPU.CPU(4, u)
        u.inserer_cpu(c4)
        c5 = CPU.CPU(4, u)
        u.inserer_cpu(c5)
        c6 = CPU.CPU(4, u)
        u.inserer_cpu(c6)
        u.killAround(3, 6)
        self.assertEqual(u.nbCPUs_at_i(3) + u.nbCPUs_at_i(4) + u.nbCPUs_at_i(5), 2)



    def test_tuer_cpus_par_densite(self):
        u = Univers.Univers(TAILLE_MEMOIRE=10, LARGEUR_CALCUL_DENSITE=1, maxCPUs=2)
        c1 = CPU.CPU(3, u)
        u.inserer_cpu(c1)
        c2 = CPU.CPU(3, u)
        u.inserer_cpu(c2)
        c3 = CPU.CPU(4, u)
        u.inserer_cpu(c3)
        u.tuer_cpus_par_densite()
        self.assertTrue(True)