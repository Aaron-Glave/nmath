import unittest
class SampleTests(unittest.TestCase):
    def is_even(self, numtoguess: int = 2) -> None:
        self.assertEqual(numtoguess % 2, 0, msg=f"{numtoguess} isn't an even number.")
    def test_passes(self):
        self.is_even(2)

    def test_example_fails(self):
        self.is_even(3)

if __name__ == '__main__':
    unittest.main()
