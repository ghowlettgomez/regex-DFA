""" This is a class that given a Regular Expression, 
	compiles a DFA that checks if a given string
	is within the Regular Language defined by that Regular
	Expression.
"""
class DFA(object):
	""" Right now, the special characters are limit to 
	the escape character, the plus character, the pipe 
	character, and the parentheses characters. They can
	be escaped with a backslash.
	"""
	special_chars = set(['*', '|', '(', ')'])

	def __init__(self, string):
		self.string = string
		self.garbage_node = Node()
		starting_nodes, finishing_nodes = self.build_dfa(string)
		for finishing_node in finishing_nodes:
			finishing_node.set_finishing_node(True)
		self.dfa = starting_nodes

	def build_dfa(self, string, given_starting_node=None):
		"""Actually builds a dfa from a given string"""
		if given_starting_node is None:
			starting_node = Node(given_garbage_node=self.garbage_node)
		else:
			starting_node = given_starting_node
		starting_nodes = [starting_node]
		finishing_nodes = []
		current_node = starting_node
		previous_node = None
		i = 0
		while i < len(string):
			character = string[i]
			if character == '|':
				new_starting_nodes, new_finishing_nodes = self.build_dfa(string[i+1:], 
					given_starting_node=given_starting_node)
				starting_nodes += new_starting_nodes
				finishing_nodes += new_finishing_nodes
				break
			elif character == '*':
				current_node.add_to_jumpdict(string[i-1], current_node)
				i += 1 
				if i == len(string):
					finishing_nodes.append(current_node)
					current_node = previous_node
				else:
					new_node = Node(given_garbage_node=self.garbage_node)
					current_node.add_to_jumpdict(string[i], new_node)
					previous_node.add_to_jumpdict(string[i], new_node)
					previous_node = current_node
					current_node = new_node
					i += 1
			elif character == ')':
				raise ValueError("Non matching parentheses")
			elif character == '(':
				substring, position = self.find_matching_paren(string[i:])
				i += position
				substart, subend = self.build_dfa(substring, given_starting_node=current_node)
				if i >= len(string):
					finishing_nodes += subend
					return starting_nodes, finishing_nodes
				else:
					new_char = string[i]
					auto_node = Node(given_garbage_node=self.garbage_node)
					new_node = Node(given_garbage_node=self.garbage_node)
					for subendnode in subend:
						subendnode.set_auto_move(auto_node)
					auto_node.add_to_jumpdict(new_char, new_node)
					if new_char == '*':
						for key in current_node.jumpdict:
							auto_node.add_to_jumpdict(key, current_node.jumpdict[key])
						i += 1
						if i == len(string):
							finishing_nodes.append(auto_node)
						else:
							new_node = Node(given_garbage_node=self.garbage_node)
							current_node.add_to_jumpdict(string[i], new_node)
							auto_node.add_to_jumpdict(string[i], new_node)
							previous_node = auto_node
							current_node = new_node
							i += 1
					else:
						current_node = new_node
						previous_node = auto_node
						i += 1
			else:
				new_node = Node(given_garbage_node=self.garbage_node)
				current_node.add_to_jumpdict(character, new_node)
				previous_node = current_node
				current_node = new_node
				i += 1
		finishing_nodes.append(current_node)
		return starting_nodes, finishing_nodes

	def evaluate_string(self, given_string):
		"""Evaluates if a given string is in the regular language
		defined by this dfa.
		"""
		current_nodes = self.dfa
		for character in given_string:
			current_nodes = [current_node.jump_to_node(character) for current_node in current_nodes]
		return any(current_node.valid for current_node in current_nodes)

	def find_matching_paren(self, given_string):
		paren_gap = 0
		for i in range(len(given_string)):
			char = given_string[i]
			if char == '(':
				paren_gap += 1
			elif char == ')':
				paren_gap -= 1
				if paren_gap == 0:
					return given_string[1:i], i+1
				if paren_gap < 0:
					raise ValueError("Non matching Parentheses")
		raise ValueError("Non matching Parentheses")


"""A node in the above DFA.
"""
class Node(object):

	def __init__(self, given_garbage_node=None, is_finishing_node=False):
		self._jumpdict = {}
		self._garbage_node = given_garbage_node
		self._finishing_node = is_finishing_node
		self._auto_move = None

	@property
	def jumpdict(self):
		return self._jumpdict
	

	@property
	def auto_move(self):
		if self._auto_move is None:
			return None
		else:
			return self._auto_move

	def set_auto_move(self, value):
		self._auto_move = value

	@property
	def garbage_node(self):
		if self._garbage_node is None:
			return self
		else:
			return self._garbage_node

	@property
	def valid(self):
		if self.auto_move is not None:
			return self.auto_move.valid
		if self._finishing_node:
			return True
		else:
			return False
 
	def set_finishing_node(self, value):
		self._finishing_node = value

	def add_to_jumpdict(self, character, Node):
		self._jumpdict[character] = Node

	def jump_to_node(self, character):
		if self.auto_move is not None:
			return self.auto_move.jump_to_node(character)
		if self._jumpdict.get(character):
			return self._jumpdict[character]
		else:
			return self.garbage_node

