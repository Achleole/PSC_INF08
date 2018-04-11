import unittest
import Experiment

class TestExperiment(unittest.TestCase):
	def test_compter_genomes_basique(self):
		e = Experiment.Experiment()
		test_code = [1, 2, 3]
		test_memoire = (test_code + [42])*10
		nombre = e.compter_genomes(test_code, test_memoire)
		print(nombre)
		self.assertTrue(nombre == 10)


if __name__ == "__main__":
	unittest.main()