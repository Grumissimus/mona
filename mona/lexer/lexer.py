import mona.lexer.token as token
import mona.lexer.operator as operator
import mona.lexer.keyword as keyword
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
        while self.srcptr < self.srclen:
            if self.current().isnumeric():
                self.getNumber()
            elif self.current().isalpha() or self.current() == "_":
                self.getIdenOrKeyword()
            elif self.current() in "\"\'":
                self.getStringLiteral()
            elif self.current() == "`":
                self.getSpecialStringLiteral()
            elif not self.current().isalpha() and not self.current().isspace():
                self.getOperator()
            else:
                self.next()

    def read(self, condition):
        startInd = self.srcptr
        while True:
            self.next()
            if self.current() == '\0' or not condition(self):
                break;

        return self.source[startInd:self.srcptr]

    def current(self, n=0):
        return self.source[self.srcptr+n] if self.srcptr+n < self.srclen else '\0'

    def getNumber(self):
        number = self.read(
            lambda s : s.current().isalnum() or s.current() == "."
        )

        value = 0

        if number.startswith("0x") or number.startswith("0X"):
            try:
                value = int(number, 16)
            except ValueError:
                self.croak("Error: The hexadecimal number \'{}\' at the line {} has an incorrect format.".format(number, self.lineNum) )
        elif number.startswith("0b") or number.startswith("0B"):
            try:
                value = int(number, 2)
            except:
                self.croak("Error: The binary number \'{}\' at the line {} has an incorrect format.".format(number, self.lineNum) )
        elif number.startswith("0") and not number.startswith("0."):
            try:
                value = int(number, 8)
            except:
                self.croak("Error: The octal number \'{}\' at the line {} has an incorrect format.".format(number, self.lineNum) )
        elif "." in number:
            try:
                value = float(number)
            except:
                self.croak("Error: The floating-point number \'{}\' at the line {} has an incorrect format.".format(number, self.lineNum) )
        else:
            value = int(number, 10)

        return token.Float(value, self.lineNum) if isinstance(value, float) else token.Number(value, self.lineNum)

    def getIdenOrKeyword(self):
        value = self.read(
            lambda s: s.current() == "_" or s.current().isalnum()
        )

        if value in ["true", "false"]:
            return {
                "true": token.Boolean(True, self.lineNum),
                "false": token.Boolean(False, self.lineNum)
            }[value]

        try:
            return token.Keyword(keyword.keywordMap[value], self.lineNum)
        except KeyError:
            return token.Identifier(value, self.lineNum)

    def getStringLiteral(self):
        stringType = self.current()

        self.next() #Skip first "\'

        while self.current() != stringType and not self.current() in '\0\n':
            self.buffer.append( self.current() )
            self.next()

        if(self.srcptr == self.srclen or self.current() == '\n'):
            self.croak("Error: Unexpected EOF when parsing a string starting from the line {}", self.lineNum)

        self.next() #Skip second "\'

        return token.String("".join(self.buffer).encode('utf-8').decode('unicode_escape') if stringType == "\"" else "".join(self.buffer), self.lineNum)

    def getSpecialStringLiteral(self):
        self.next()  #Skip first `

        while((not self.current().isalnum() and not self.current().isspace()) and (not self.current() in '$@\'\"{}()[]`\0\n')):
            self.buffer.append( self.current() )
            self.next()

        if(self.srcptr == self.srclen or self.current() == '\n'):
            self.croak("Error: Unexpected EOF when parsing a string starting from the line {}", self.lineNum)

        self.next()  #Skip second `

        self.makeToken(token.TOKEN_IDENTIFIER, "".join(self.buffer), self.lineNum)
        return True

    def getOperator(self):
        if self.current() == ';':
            self.srcptr += 1
            while self.current() != "\n\0":
                self.next()
                return

        if self.current() in '()[]{}%^~/$@!':
            self.next()
            return token.Operator(operator.operatorMap[self.current()], self.lineNum)
        else:
            value = self.read( lambda s: re.fullmatch(r'[^\w\d$@\'\"{}()\[\]\`\0]', s.current) )

            try:
                return token.Operator(operator.operatorMap[value], self.lineNum)
            except:
                self.makeToken(token.TOKEN_IDENTIFIER, value, self.lineNum)
                return False
        return False

    def croak(self, errorMessage):
        print(errorMessage, file=sys.stderr)
        sys.exit()

    def next(self):
        if(self.srcptr < self.srclen):
            self.srcptr+=1
        if(self.current() == '\n'):
            self.lineNum += 1
