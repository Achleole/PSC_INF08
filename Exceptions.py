class PatternNotFoundException(Exception):
	"Cette classe permet de gerer quand le pattern situe apres l'instruction jmp/call/adr\
	existe mais n'a pas ete trouve par la suite"
	def __init__(self, l_pattern):
		super(PatternNotFoundException, self).__init__()
		self.l_pattern = l_pattern

class NoPatternException(Exception):
	"Cette classe set a gerer quand il n'y a pas de pattern apres l'instruction jmp/call/adr"
	def __init__(self):
		super(NoPatternException, self).__init__()

class NoCPUException(Exception):
	def __init__(self):
		super(NoCPUException, self).__init__()