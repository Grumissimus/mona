from typing import Generic, TypeVar, Callable
from abc import abstractmethod

T = TypeVar('T')
S = TypeVar('S')


class Monad(Generic[T]):
    def __init__(self, value: T):
        self.value = value

    def unit(self, value: T):
        return Monad[T](value)

    @abstractmethod
    def bind(self, func: Callable[[T], 'Monad[S]']) -> 'Monad[S]':
        return Monad[S](func(self.value))

    def __eq__(self, monad):
        if(monad is None):
            return False

        return self.value == monad.value

    def __neq__(self, monad):
        return not self.__eq__(self, monad)


class Id(Monad[T]):
    def bind(self, func: Callable[[T], 'S']) -> 'S':
        return func(self.value)

    def get(self):
        return self.bind(lambda x: x)
