class Node:
	"""
	Class that defines a node in a tree
	"""
	def __init__(self, curr_string):
		"""
		curr_string: string at current node level
		"""
		self.curr_string = curr_string
		self.complete_string = False
		self.children = {}

class PrefixTree:
	def __init__(self):
		self.root = Node('')

	def insert_new_string(self, new_string):
		"""
		Function to insert new string into prefix tree
		"""
		curr_node = self.root
		curr_string = ''
		chars = list(new_string)
		for c in chars:
			curr_string += c
			if curr_string in curr_node.children:
				curr_node = curr_node.children[curr_string]
			else:
				new_node = Node(curr_string)
				if curr_string == new_string:
					new_node.complete_string = True
				curr_node.children[curr_string] = new_node
				curr_node = new_node

	def build_prefix_tree(self, list_of_words):
		"""
		Function that build a prefix tree for a list of words
		"""
		for word in list_of_words:
			self.insert_new_string(word)

	def get_all_leaf_nodes(self, curr_node, result):
		"""
		Function to get all leaf nodes in the prefix tree
		"""
		if curr_node.complete_string == True:
			result.append(curr_node.curr_string)
		for k,v in curr_node.children.iteritems():
			self.get_all_leaf_nodes(v, result)

	def get_all_possible_words(self, prefix):
		"""
		Function that gets a list of all possible words given a prefix
		"""
		curr_node = self.root
		curr_string = ''
		chars = list(prefix)
		result = []
		for c in chars:
			curr_string += c
			if not(curr_string in curr_node.children):
				return []
			else:
				curr_node = curr_node.children[curr_string]
		#need to find all leaf nodes from curr_node
		if curr_node.complete_string == True:
			result.append(curr_node.curr_string)
		self.get_all_leaf_nodes(curr_node, result)
		return result
