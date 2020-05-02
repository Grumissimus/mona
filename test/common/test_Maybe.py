import unittest
import sys
sys.path.append('../../mona/')
from mona.common.maybe import Maybe, Just, Nothing


class TestMaybe(unittest.TestCase):
    # m(x).bind(f) <-> f(x)
    def test_monad_first_law(self):
        square = lambda x: x * 2
        value = 2
        self.assertEqual(Maybe(value).bind(square).value, square(value))

    # m <=> m
    def test_monad_second_law(self):
        val = 1
        monad = Maybe(val)
        self.assertEqual(monad, monad.unit(val))

    # m.bind(f).bind(g) <=> f(g(a))
    def test_monad_third_law(self):
        value = 1
        monad = Maybe(value)
        foo = lambda x: x + 1
        bar = lambda y: y + 2
        self.assertEqual(
            monad.bind(foo).bind(bar).value,
            Maybe(value).bind(lambda x: bar(foo(x)))
        )

    def test_maybe_just(self):
        maybe = Maybe(5)
        self.assertIsInstance(maybe, Maybe)
        self.assertIsInstance(maybe, Just)
        self.assertEqual(maybe.value, 5)

    def test_maybe_none(self):
        maybe = Maybe(None)
        self.assertIsInstance(maybe, Maybe)
        self.assertIsInstance(maybe, Nothing)
        self.assertEqual(maybe.value, None)

    def test_maybe_just_bind(self):
        maybe = Maybe(5) \
            .bind(lambda x: x + 1) \
            .bind(lambda x: str(x)) \
            .bind(lambda x: x + "2")

        self.assertEqual(maybe.value, "62")

    def test_maybe_nothing_bind(self):
        maybe = Maybe(None) \
            .bind(lambda x: x + 1) \
            .bind(lambda x: x - 5)

        self.assertEqual(maybe.value, None)

if __name__ == "main":
    unittest.main()
