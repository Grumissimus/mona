from typing import TypeVar, Generic
from mona.lexer.operator import Operator as OperatorEnum
from mona.lexer.keyword import Keyword as KeywordEnum

T = TypeVar('T')


class Token(Generic[T]):
    def __init__(self, value: T, line: int):
        self.value = value
        self.line = line

    def __str__(self):
        return "token type: {0}\nvalue: {1}\nline: {2}".format(
            self.__class__.__name__,
            self.value,
            self.line)


class Identifier(Token[str]):
    pass


class Keyword(Token[KeywordEnum]):
    pass


class Number(Token[int]):
    pass


class String(Token[str]):
    pass


class Float(Token[float]):
    pass


class Boolean(Token[bool]):
    pass


class Operator(Token[OperatorEnum]):
    pass


class Separator(Operator):
    pass
