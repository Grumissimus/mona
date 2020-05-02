import unittest
import sys
sys.path.append('../../mona/')
from mona.common.either import Either, Left, Right


class TestResult(unittest.TestCase):
    def test_either_left(self):
        either: Either[int, str] = Either(2)
        self.assertIsInstance(either, Left)
        self.assertEqual(either.value, 2)


if __name__ == "main":
    unittest.main()
