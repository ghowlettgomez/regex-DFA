""" This is a class that given a Regular Expression, 
	compiles a DFA that checks if a given string
	is within the Regular Language defined by that Regular
	Expression.
	NOTE: Only handles alphanumeric characters right now.
"""
class DFA(object):
	""" Right now, the special characters are limit to 
	the escape character, the plus character, the pipe 
	character, and the parentheses characters. They can
	be escaped with a backslash.
	"""
	special_chars = set(['\\', '+', '|', '(', ')'])

	def __init__(self, string):
		self.string = string
		self.garbage_node = Node()
		self.dfa = self.build_dfa(string)

	def build_dfa(self, string):
		"""Actually builds a dfa from a given string"""
		starting_node = Node(given_garbage_node=self.garbage_node)
		current_node = starting_node
		string_len = len(string)
		for i in range(string_len):
			new_node = Node(given_garbage_node=self.garbage_node)
			current_node.add_to_jumpdict(string[i], new_node)
			current_node = new_node
		current_node.set_finishing_node(True)
		return starting_node

	def evaluate_string(self, given_string):
		"""Evaluates if a given string is in the regular language
		defined by this dfa.
		"""
		current_node = self.dfa
		for character in given_string:
			current_node = current_node.jump_to_node(character)
		return current_node.valid


"""A node in the above DFA.
"""
class Node(object):

	def __init__(self, given_garbage_node=None, is_finishing_node=False):
		self.jumpdict = {}
		self._garbage_node = given_garbage_node
		self._finishing_node = is_finishing_node

	@property
	def garbage_node(self):
		if self._garbage_node is None:
			return self
		else:
			return self._garbage_node

	@property
	def valid(self):
		if self._finishing_node:
			return True
		else:
			return False
 
	def set_finishing_node(self, value):
		self._finishing_node = value

	def add_to_jumpdict(self, character, Node):
		self.jumpdict[character] = Node

	def jump_to_node(self, character):
		if self.jumpdict.get(character):
			return self.jumpdict[character]
		else:
			return self.garbage_node

