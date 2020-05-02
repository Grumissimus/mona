from mona.common.monad import Monad, Id
from typing import TypeVar, Callable, Generic

TLeft = TypeVar('TLeft')
TRight = TypeVar('TRight')
TNeither = TypeVar('TNeither')


class Either(Monad, Generic[TLeft,TRight]):
    def __new__(cls, value):
        print(TLeft.__args__)
        if type(value) == TLeft:
            return Left[TLeft](value)
        elif type(value) == TRight:
            return Right[TRight](value)
        else:
            return Neither[type(value)](value)

    def __init__(self, value):
        pass


class Right(Monad[TRight]):
    pass


class Left(Monad[TLeft]):
    pass


class Neither(Id[TNeither]):
    pass

