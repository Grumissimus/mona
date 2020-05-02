from mona.common.monad import Monad
from typing import TypeVar, Callable

TMaybe = TypeVar('TMaybe')
SMaybe = TypeVar('SMaybe')


class Maybe(Monad[TMaybe]):
    def __new__(cls, value):
        if value is not None:
            return super(Maybe, cls).__new__(Just)
        else:
            return super(Maybe, cls).__new__(Nothing)

    def __init__(self, value):
        pass


class Just(Maybe[TMaybe]):
    def __init__(self, value):
        self.value = value

    def bind(self, func: Callable[[TMaybe], Maybe[SMaybe]]) -> Maybe[SMaybe]:
        return Maybe(func(self.value))


class Nothing(Maybe[TMaybe]):
    def __init__(self, value=None):
        self.value = None

    def bind(self, func: Callable[[TMaybe], Maybe[SMaybe]]) -> Maybe[SMaybe]:
        return self
