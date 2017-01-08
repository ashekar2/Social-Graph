import unittest
from prefix_tree import *

class TestPrefixTree(unittest.TestCase):
	def test_insert_new_string(self):
		p = PrefixTree()
		p.insert_new_string('ajay')
		self.assertEqual('a' in p.root.children, True)

	def test_insert_new_string2(self):
		p = PrefixTree()
		p.insert_new_string('ajay')
		self.assertEqual(p.root.children['a'].children['aj'].curr_string, 'aj')

	def test_insert_new_string3(self):
		p = PrefixTree()
		p.insert_new_string('ajay')
		p.insert_new_string('akay')
		self.assertEqual('a' in p.root.children, True)

	def test_insert_new_string4(self):
		p = PrefixTree()
		p.insert_new_string('ajay')
		p.insert_new_string('akay')
		self.assertEqual('aj' in p.root.children['a'].children, True)
		self.assertEqual('ak' in p.root.children['a'].children, True)

	def test_build_prefix_tree(self):
		p = PrefixTree()
		p.build_prefix_tree(['ajay', 'akay'])
		self.assertEqual('aj' in p.root.children['a'].children, True)
		self.assertEqual('ak' in p.root.children['a'].children, True)

	def test_get_all_leaf_nodes(self):
		p = PrefixTree()
		p.build_prefix_tree(['ajay', 'akay'])
		leaves = []
		p.get_all_leaf_nodes(p.root, leaves)
		self.assertEqual('ajay' in leaves, True)
		self.assertEqual('akay' in leaves, True)

	def test_get_all_possible_words(self):
		p = PrefixTree()
		p.build_prefix_tree(['ajay', 'akay'])
		leaves = []
		r1 = p.get_all_possible_words('a')
		r2 = p.get_all_possible_words('aj')
		r3 = p.get_all_possible_words('ajakjhs')
		self.assertEqual('ajay' in r1, True)
		self.assertEqual('akay' in r1, True)
		self.assertEqual('ajay' in r2, True)
		self.assertEqual(r3 == [], True)

if __name__ == '__main__':
    unittest.main()