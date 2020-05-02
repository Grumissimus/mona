from enum import Enum

InternalError = [
    "Unknown"
]

LexerError = [
    "IncorrectHexadecimalNumberFormat",
    "IncorrectBinaryNumberFormat",
    "IncorrectOctalNumberFormat",
    "IncorrectFloatingPointNumberFormat",
    "SuddenEOF"
]

ParserError = [

]

SemanticError = [

]

AllErrors = InternalError + LexerError + ParserError + SemanticError

ErrorType = Enum('ErrorType', " ".join(AllErrors))


class Error():
    def __init__(self, errorType: ErrorType, message: str):
        self.errorType = errorType
        self.message = message

    def __str__(self):
        return self.message


class ErrorMessageBuilder():
    def __init__(self):
        self.rowline = 0
        self.colline = 0
        self.errorType = None
        self.message = ""
        self.messageFormat = "{0}:{1} {2}: {3}"

    def setRowline(self, rowline: int):
        self.rowline = rowline
        return self

    def setColline(self, colline: int):
        self.colline = colline
        return self

    def setErrorType(self, errType: ErrorType):
        self.errorType = errType
        return self

    def setMessage(self, msg):
        self.message = msg
        return self

    def build(self):
        return self.messageFormat.format(
            self.rowline,
            self.colline,
            self.errorType.name,
            self.message
        )


class ErrorFactory():
    def IncorrectHexadecimalNumberFormat(self, rowline, colline) -> Error:
        errType = ErrorType.IncorrectHexadecimalNumberFormat
        message = ErrorMessageBuilder() \
            .setRowline(rowline) \
            .setColline(colline) \
            .setErrorType(errType) \
            .setMessage("The hexadecimal integer has incorrect format") \
            .build()

        return Error(errType, message)
