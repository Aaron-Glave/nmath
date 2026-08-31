import unittest
from factorized import Factorized


class TestFactorize(unittest.TestCase):
    def test_neg1(self):
        factored = Factorized(-1)
        self.assertEqual('-1 ^ 1', str(factored))

    def test_12(self):
        factored = Factorized(12)
        self.assertEqual('2 ^ 2 * 3 ^ 1', str(factored))

    def test_48(self):
        factored = Factorized(48)
        self.assertEqual('2 ^ 4 * 3 ^ 1', str(factored))

    def test_1776384(self):
        factored = Factorized(1776384)
        self.assertEqual('2 ^ 8 * 3 ^ 3 * 257 ^ 1', str(factored))



if __name__ == '__main__':
    unittest.main()
