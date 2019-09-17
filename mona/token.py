type = {
	"IDENTIFIER": 0,
	"KEYWORD": 1,
	"INTEGER": 2,
	"FLOATING_POINT": 3,
	"STRING_LITERAL": 4,
	"OPERATOR": 5,
	"DELIMITER": 6
}

keywordType = {
	"IF" : 0,
	"THEN" : 1,
	"ELSE" : 2,
	"LET" : 3
}

class Token():
	def __init__(self, type, value):
		self.type = type
		self.value = value