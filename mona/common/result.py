from typing import Generic, TypeVar, Tuple
from mona.common.monad import Monad, Id
from mona.common.error import Error

TSuccess = TypeVar('TSuccess')


class Ok(Id[TSuccess]):
    pass


class Fail(Id[Error]):
    pass


class Result():
    pass
