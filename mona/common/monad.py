from typing import Generic, TypeVar, Callable
from abc import abstractmethod

T = TypeVar('T')
S = TypeVar('S')


class Monad(Generic[T]):
    def __init__(self, value: T):
        self.value = value

    @abstractmethod
    def value(self):
        return

    @abstractmethod
    def bind(self, func: Callable[[T], 'Monad[S]']) -> 'Monad[S]':
        return Monad[S](func(self.value))


class Id(Monad[T]):
    def bind(self, func: Callable[[T], 'S']) -> 'S':
        return func(self.value)

    def get(self):
        return self.bind(lambda x: x)
