import unittest

import moves


# Test case:
class MoveTests(unittest.TestCase):
    # Tests must always begin with the word `test`.
    def test_five_plus_five(self):
        assert 5 + 5 == 10

    def test_one_plus_one(self):
        assert not 1 + 1 == 3

# Allow tests to be run directly via `python tests.py`.
if __name__ == '__main__':
    unittest.main()
