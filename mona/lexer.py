import mona.token as token
import mona.operator as operator
import mona.keyword as keyword
import sys


class Lexer():
    def __init__(self, src=""):
        self.tokens = []
        self.source = src
        self.srclen = len(src)
        self.srcptr = 0
        self.buffer = []
        self.lineNum = 1


    def run(self):
        while self.srcptr < self.srclen:
            if self.curChar().isnumeric():
                self.getNumber()
            elif self.curChar().isalpha() or self.curChar() == "_":
                self.getIdenOrKeyword()
            elif self.curChar() in "\"\'":
                self.getStringLiteral()
            elif self.curChar() == "`":
                self.getSpecialStringLiteral()
            elif not self.curChar().isalpha() and not self.curChar().isspace():
                self.getOperator()
            else:
                self.next()


    def makeToken(self, type, value, line):
        self.tokens.append(token.Token(type, value, line))
        self.buffer = []


    def curChar(self, n = 0):
        return self.source[self.srcptr+n] if self.srcptr+n < self.srclen else '\0'


    def getNumber(self):
        while (self.curChar().isalnum() or self.curChar() == "."):
            self.buffer.append( self.curChar() )
            self.next()

        number = "".join(self.buffer)
        value = 0

        if number.startswith("0x") or number.startswith("0X"):
            try:
                value = int( number, 16 )
            except:
                self.croak("Error: The hexadecimal number \'{}\' at the line {} has an incorrect format.".format(number, self.lineNum) )
        elif number.startswith("0b") or number.startswith("0B"):
            try:
                value = int( number, 2 )
            except:
                self.croak("Error: The binary number \'{}\' at the line {} has an incorrect format.".format(number, self.lineNum) )
        elif number.startswith("0") and not number.startswith("0."):
            try:
                value = int( number, 8 )
            except:
                self.croak("Error: The octal number \'{}\' at the line {} has an incorrect format.".format(number, self.lineNum) )
        elif "." in number:
            try:
                value = float( number )
            except:
                self.croak("Error: The floating-point number \'{}\' at the line {} has an incorrect format.".format(number, self.lineNum) )
        else:
            value = int( number, 10 )


        self.makeToken(token.TOKEN_FLOAT if isinstance(value, float) else token.TOKEN_NUMBER, value, self.lineNum)
        return True


    def getIdenOrKeyword(self):
        while self.curChar() == "_" or self.curChar().isalnum():
            self.buffer.append( self.curChar() )
            self.next()

        value = "".join(self.buffer)

        if value == "true" or value == "false":
            self.makeToken(token.TOKEN_BOOLEAN, True if value == "true" else False, self.lineNum);
            return True

        try:
            self.makeToken(token.TOKEN_KEYWORD, keyword.keywordMap[value], self.lineNum)
            return True
        except KeyError:
            self.makeToken(token.TOKEN_IDENTIFIER, value, self.lineNum)
            return True


    def getStringLiteral(self):
        stringType = self.curChar()

        self.next() #Skip first "\'

        while self.curChar() != stringType and not self.curChar() in '\0\n':
            self.buffer.append( self.curChar() )
            self.next()

        if(self.srcptr == self.srclen or self.curChar() == '\n'):
            self.croak("Error: Unexpected EOF when parsing a string starting from the line {}", self.lineNum)

        self.next() #Skip second "\'

        self.makeToken(token.TOKEN_STRING, "".join(self.buffer).encode('utf-8').decode('unicode_escape') if stringType == "\"" else "".join(self.buffer), self.lineNum)
        return True


    def getSpecialStringLiteral(self):
        self.next() #Skip first `

        while((not self.curChar().isalnum() and not self.curChar().isspace()) and (not self.curChar() in '$@\'\"{}()[]`\0\n')):
            self.buffer.append( self.curChar() )
            self.next()

        if(self.srcptr == self.srclen or self.curChar() == '\n'):
            self.croak("Error: Unexpected EOF when parsing a string starting from the line {}", self.lineNum)

        self.next() #Skip second `

        self.makeToken(token.TOKEN_IDENTIFIER, "".join(self.buffer), self.lineNum)
        return True


    def getOperator(self):
        if self.curChar() == ';':
            self.srcptr += 1
            while( self.curChar() != "\n\0" ):
                self.next()
            return True

        if self.curChar() in '()[]{}%^~/$@!':
            self.makeToken(token.TOKEN_NONALPHA, operator.operatorMap[self.curChar()], self.lineNum)
            self.next()
            return True
        else:
            while((not self.curChar().isalnum() and not self.curChar().isspace()) and (not self.curChar() in '$@\'\"{}()[]`') and self.curChar() != '\0'):
                self.buffer.append( self.curChar() )
                self.next()

            try:
                self.makeToken(token.TOKEN_NONALPHA, operator.operatorMap["".join(self.buffer)], self.lineNum)
                return True
            except:
                self.makeToken(token.TOKEN_IDENTIFIER, "".join(self.buffer), self.lineNum)
                return False


        return False


    def croak(self,errorMessage):
        print(errorMessage, file=sys.stderr);
        sys.exit()


    def next(self):
        if(self.srcptr < self.srclen):
            self.srcptr+=1;
        if(self.curChar() == '\n'):
            self.lineNum += 1
