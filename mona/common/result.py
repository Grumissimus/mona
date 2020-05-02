from typing import Callable, TypeVar
from mona.common.monad import Monad, Id
from mona.common.error import Error

TSuccess = TypeVar('TSuccess')


class Ok(Id[TSuccess]):
    pass


class Fail(Id[Error]):
    pass


class Result(Monad[TSuccess]):
    def __init__(self, success: Ok = None, failure: Fail = None):
        self.value = (success, failure)

