import unittest
import Univers
import CPU
import utests.NextSiteTest as NextSiteTest
import utests.CheckCPU as CheckCPU

class TestCPU(unittest.TestCase):
    def setUp(self):
        self.u = Univers.Univers(NextSiteTest.NextSiteTest())

    def test_creationCPU(self) :
        stack = [i for i in range(CPU.TAILLE_STACK)]
        c = CPU.CPU(102, self.u, 3,7,9,11, stack,2)
        CheckCPU.checkCPU(self, c, 102, 3,7,9,11,2, stack)
        c2 = CPU.CPU(101, self.u)
        CheckCPU.checkCPU(self, c2, 101, 0, 0, 0, 0, 0, [0]*CPU.TAILLE_STACK)

    def test_incr_stack(self) :
        c = CPU.CPU(102, self.u)
        p = c.stack_ptr
        c.incrementer_stack_ptr()
        self.assertTrue(c.stack_ptr==p+1or(c.stack_ptr==0&p==CPU.TAILLE_STACK-1))
        c.stack_ptr = 1
        c.incrementer_stack_ptr()
        self.assertEqual(c.stack_ptr, 2)

    def test_incr_ptr(self) :
        c = CPU.CPU(102, self.u)
        p = c.ptr
        c.incrementer_ptr()
        if p==len(self.u.memoire)-1 :
            self.assertEqual(c.ptr,0)
        else :
            self.assertEqual(c.ptr,p+1)
        c.ptr = len(self.u.memoire)-1
        p = c.ptr
        c.incrementer_ptr()
        self.assertEqual(c.ptr, 0)

    def test_decr_stack(self) :
        c = CPU.CPU(102, self.u)
        p = c.stack_ptr
        c.decrementer_stack_ptr()
        if p == 0 :
            self.assertEqual(c.stack_ptr, CPU.TAILLE_STACK - 1)
        else :
            self.assertEqual(c.stack_ptr, p - 1)
        c.stack_ptr = 1
        c.incrementer_stack_ptr()
        self.assertEqual(c.stack_ptr, 2)

    def test_die(self) :
        c1 = CPU.CPU(102, self.u)
        c2 = CPU.CPU(0, self.u)
        c3 = CPU.CPU(101, self.u)
        c4 = CPU.CPU(102, self.u)
        self.u.inserer_cpu(c1)
        self.u.inserer_cpu(c2)
        self.u.inserer_cpu(c3)
        self.u.inserer_cpu(c4)
        c1.die()
        self.assertFalse(c1 in self.u.liste_cpus)
        self.assertTrue((c1.ptr not in self.u.localisation_cpus) or (c1 not in self.u.localisation_cpus[c1.ptr]))
        c2.die()
        self.assertFalse(c2 in self.u.liste_cpus)
        self.assertTrue((c2.ptr not in self.u.localisation_cpus) or (c2 not in self.u.localisation_cpus[c2.ptr]))
        c4.die()
        self.assertFalse(c4 in self.u.liste_cpus)
        self.assertTrue((c4.ptr not in self.u.localisation_cpus) or (c4 not in self.u.localisation_cpus[c4.ptr]))
        c3.die()
        self.assertFalse(c3 in self.u.liste_cpus)
        self.assertTrue((c3.ptr not in self.u.localisation_cpus) or (c3 not in self.u.localisation_cpus[c3.ptr]))

    def test_push_stack(self) :
        c = CPU.CPU(102, self.u)
        c.push_stack(3)
        self.assertEqual(c.stack_ptr,0)
        self.assertEqual(c.stack[c.stack_ptr],3)
        c.push_stack(2)
        for i in range(1,CPU.TAILLE_STACK) :
            self.assertEqual(c.stack[i],0)
        self.assertEqual(c.stack_ptr, 0)
        self.assertEqual(c.stack[c.stack_ptr], 2)
        c.incrementer_stack_ptr()
        c.push_stack(-5)
        self.assertEqual(c.stack_ptr, 1)
        self.assertEqual(c.stack[c.stack_ptr], -5)

    def test_pop_stack(self):
        c = CPU.CPU(102, self.u, stack=[0]*CPU.TAILLE_STACK)
        self.assertEqual(0,c.pop_stack())
        c.stack = [i for i in range(CPU.TAILLE_STACK)]
        self.assertEqual(CPU.TAILLE_STACK-1, c.pop_stack()) #On verifie que pop_stack renvoie la bonne valeur...
        for i in range(CPU.TAILLE_STACK) :# ...et qu'il ne change pas les valeurs
            self.assertEqual(i, c.stack[i])
        c.push_stack(3)
        self.assertEqual(CPU.TAILLE_STACK - 1, c.pop_stack())
        c.incrementer_stack_ptr()
        self.assertEqual(c.stack_ptr, 1)
        self.assertEqual(3, c.pop_stack())
        self.assertEqual(c.stack_ptr, 1)


    # Comment tester execute ??