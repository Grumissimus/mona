#wrapper for type's graph
class TypeGraph(object):
	def __init__(self):
		self.types = {}
	
	def getType(self, name):
		try:
			return self.types[name]
		except KeyError:
			return None

class Type(object):
	pass

#your normal type without any shenanigans
class NormalType(Type):
	def __init__(self, name):
		self.name = name
		self.super = {}
	
	def addSuper(self,type):
		self.super[type.name] = type
		
	def __str__(self):
		return self.name
		
#algebraic data type
class CompositeType(Type):
	def __init__(self,name):
		self.name = name
		
		self.required = {}
		self.accepted = {}
		self.notAccepted = {}
		
	def addRequired(self,type):
		self.required[type.name] = type
		
	def addAccepted(self,type):
		self.accepted[type.name] = type
		
	def addNotAccepted(self,type):
		self.notAccepted[type.name] = type
		
	def __str__(self):
		return self.name
		
#range-based type
class RangeType(Type):
	def __init__(self, name, min, max):
		self.name = name
		
		if min > max:
			raise ValueError
			
		self.min = min
		self.max = max
	
	def withinRange(self, value):
		return min <= value <= max
	
	def addSuper(self,type):
		self.super[type.name] = type
		
	def __str__(self):
		return self.name

#type with templates i.e. Array<Integer>
class ParametrizedType(Type):
	def __init__(self, name, parameters):
		self.name = name
		self.parameters = parameters
		self.super = {}
		
	def addSuper(self,type):
		self.super[type.name] = type
		
	def __str__(self):
		return self.name

#Useful for semantic analysis		
def constructDefaultGraph():
	graph = TypeGraph()
	any = NormalType('Any')
	graph.types['Any'] = any
		
	none = NormalType('None')
	graph.types['Any'] = none

	NormalType('Integer').addSuper(any)
	NormalType('Float').addSuper(any)
	NormalType('String').addSuper(any)
	NormalType('Boolean').addSuper(any)
	NormalType('Array').addSuper(any)
	NormalType('Function').addSuper(any)
	NormalType('Block').addSuper(any)
		
	return graph