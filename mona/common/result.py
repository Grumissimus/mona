from mona.common.monad import Monad


class Result(Monad):
    def __new__(cls, value, isRight=True):
        if isRight:
            return super(Result, cls).__new__(Ok)
        else:
            return super(Result, cls).__new__(Fail)

    def __init__(self, value, isRight):
        pass

    def bind(self, func):
        try:
            return Result(func(self.value), True)
        except BaseException as e:
            return Result(e, False)


class Ok(Result):
    def __init__(self, value, isRight=True):
        self.value = value


class Fail(Result):
    def __init__(self, value, isRight=False):
        self.value = value

    def bind(self, func):
        return self
