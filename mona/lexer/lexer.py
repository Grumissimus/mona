import mona.lexer.token as token
import mona.lexer.operator as operator
import mona.lexer.keyword as keyword
from mona.common.error import ErrorFactory
import sys
import re


class Lexer():
    def __init__(self, src=""):
        self.tokens = []
        self.source = src
        self.srclen = len(src)
        self.srcptr = 0
        self.lineNum = 1

    def run(self):
        dispatch = [
            (r'\d', self.getNumber),
            (r'[\w_]', self.getIdenOrKeyword),
            (r'\"', self.getEscapedString),
            (r'\'', self.getUnescapedString),
            (r';', self.skipComment),
            (r'[^\w\d\s]', self.getOperator)
        ]

        while self.srcptr < self.srclen:
            Token = None

            for i in dispatch:
                if re.fullmatch(i[0], self.current()):
                    Token = i[1]()
                    break

            if Token is not None:
                self.tokens.append(Token)
            else:
                self.next()

    def read(self, condition):
        startInd = self.srcptr
        while True:
            self.next()
            if self.current() == '\0' or not condition(self):
                break

        return self.source[startInd:self.srcptr]

    def current(self, n=0):
        return self.source[self.srcptr+n] if self.srcptr+n < self.srclen else '\0'

    def getNumber(self):
        value = self.read(lambda s: re.match(r'[\w\d\.]', self.current()))
        number = 0

        dispatch = [
            (r'0[xX][\dA-Fa-f]+', lambda x: int(x, 16)),
            (r'0[bB][01]+', lambda x: int(x, 2)),
            (r'0[^.][0-7]+', lambda x: int(x, 8)),
            (r'(0?|[1-9]\d+)*\.\d+', lambda x: float(x)),
            (r'(0|[1-9]\d*)', lambda x: int(x, 10))
        ]

        for i in dispatch:
            if re.fullmatch(i[0], value) is not None:
                number = i[1](value)
                break

        if isinstance(value, float):
            return token.Float(number, self.lineNum)
        else:
            return token.Number(number, self.lineNum)

    def getIdenOrKeyword(self):
        value = self.read(lambda s: re.match(r'[\w\d_]', s.current()))

        booleanDispatch = [
            ("true", True),
            ("false", False)
        ]

        for i in booleanDispatch:
            if value == i[0]:
                return token.Boolean(i[1], self.lineNum)

        try:
            return token.Keyword(keyword.keywordMap[value], self.lineNum)
        except KeyError:
            return token.Identifier(value, self.lineNum)

    def _readString(self, stop):
        value = self.read(
            lambda s: self.current() != '\n' or not (self.current() == stop and self.current(-1) != '\\')
        )

        dispatch = [
            (
                lambda: self.current() == '\n',
                "Error: Unexpected end of the string at the line {}"
            ),
            (
                lambda: self.current() == '\0' and value[-1] != "\"",
                "Error: Unexpected EOF at the line {}"
            )
        ]

        for i in dispatch:
            if i[0]():
                self.croak(i[1].format(self.lineNum))

        return value

    def getEscapedString(self):
        value = self._readString('\"')
        value = value.encode('utf-8').decode('unicode_escape')

        return token.String(value, self.lineNum)

    def getUnescapedString(self):
        value = self._readString('\'')

        return token.String(value, self.lineNum)

    def skipComment(self):
        self.read(lambda x: x.current() != '\n' )

    def getOperator(self):
        if self.current() in '()[]{}':
            value = self.current()
            self.next()
            return token.Separator(operator.operatorMap[value], self.lineNum)
        else:
            value = self.read( lambda s: re.fullmatch(r'[^\w\d\s\'\"{}()\[\]]', s.current()))

            try:
                return token.Operator(operator.operatorMap[value], self.lineNum)
            except Exception as e:
                print(e)
                return token.Identifier(value, self.lineNum)

    def croak(self, errorMessage):
        print(errorMessage, file=sys.stderr)
        sys.exit()

    def next(self):
        if(self.srcptr < self.srclen):
            self.srcptr += 1
        if(self.current() == '\n'):
            self.lineNum += 1
