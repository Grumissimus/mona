import unittest
import sys
sys.path.append('../../mona/')
from mona.common.monad import Monad, Id


class TestMonad(unittest.TestCase):
    def test_monad_number(self):
        monad = Monad(2)
        self.assertIsInstance(monad, Monad)
        self.assertEqual(monad.value, 2)

    def test_monad_number_type_error(self):
        monad: Monad[int] = Monad("A")
        self.assertRaises(TypeError)

    def test_bind_number(self):
        monad = Monad(3)
        monad = monad.bind(lambda x: x + 1)
        self.assertEqual(monad.value, 4)

    def test_multiple_bind(self):
        monad = Monad(2)
        monad = monad.bind(lambda x: x + 1) \
        .bind(lambda x : str(x)) \
        .bind(lambda x : x + "1")

        self.assertIsInstance(monad, Monad)
        self.assertIsInstance(monad.value, str)
        self.assertEqual(monad.value, "31")


class TestId(unittest.TestCase):
    def setUp(self):
        self.idMonad = Id(5)

    def test_id_constructor(self):
        self.assertIsInstance(self.idMonad, Id)
        self.assertIsInstance(self.idMonad, Monad)
        self.assertEqual(self.idMonad.value, 5)

    def test_id_bind(self):
        value = self.idMonad.bind(lambda x: x + 1)
        self.assertEqual(self.idMonad.value, 5)
        self.assertEqual(value, 6)

    def test_id_get(self):
        value = self.idMonad.get()
        self.assertEqual(value, 5)


if __name__ == "__main__":
    unittest.main()
