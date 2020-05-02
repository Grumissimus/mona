from enum import Enum

Keyword = Enum('Keyword', 'LET TYPE IMPORT AS IN RETURN TRUE FALSE')

keywordMap = {
    "let": Keyword.LET,
    "type": Keyword.TYPE,
    "import": Keyword.IMPORT,
    "as": Keyword.AS,
    "return": Keyword.RETURN,
    "true": Keyword.TRUE,
    "false": Keyword.FALSE
}
