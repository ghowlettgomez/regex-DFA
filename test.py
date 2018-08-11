import unittest
from compile import DFA

class DFATest(unittest.TestCase):

	def test_empty(self):
		dfa = DFA('')
		self.assertTrue(dfa.evaluate_string(''))
		self.assertFalse(dfa.evaluate_string('' + 'lol'))

	def test_normal0(self):
		dfa = DFA('lol')
		self.assertTrue(dfa.evaluate_string('lol'))
		self.assertFalse(dfa.evaluate_string('lol' + 'lollol'))
		self.assertFalse(dfa.evaluate_string(''))

	def test_normal1(self):
		dfa = DFA('hello world')
		self.assertTrue(dfa.evaluate_string('hello world'))
		self.assertFalse(dfa.evaluate_string('hello world' + 'lollol'))
		self.assertFalse(dfa.evaluate_string(''))

	def test_and0(self):
		dfa = DFA('hello|world')
		self.assertTrue(dfa.evaluate_string('hello'))
		self.assertFalse(dfa.evaluate_string('hello|world'))
		self.assertTrue(dfa.evaluate_string('world'))
		self.assertFalse(dfa.evaluate_string(''))

	def test_and1(self):
		dfa = DFA('hello|')
		self.assertTrue(dfa.evaluate_string('hello'))
		self.assertFalse(dfa.evaluate_string('hello|'))
		self.assertTrue(dfa.evaluate_string(''))

	def test_star0(self):
		dfa = DFA('a*')
		self.assertTrue(dfa.evaluate_string(''))
		self.assertTrue(dfa.evaluate_string('a'))
		self.assertTrue(dfa.evaluate_string('aa'))
		self.assertTrue(dfa.evaluate_string('aaaaaa'))
		self.assertTrue(dfa.evaluate_string('aaaaaaaa'))
		self.assertFalse(dfa.evaluate_string('b'))
		self.assertFalse(dfa.evaluate_string('aaabaa'))
		self.assertFalse(dfa.evaluate_string('aaab'))

	def test_star1(self):
		dfa = DFA('lola*lol')
		self.assertTrue(dfa.evaluate_string('lollol'))
		self.assertFalse(dfa.evaluate_string('lol'))
		self.assertFalse(dfa.evaluate_string('lola'))
		self.assertTrue(dfa.evaluate_string('lolaaaaaalol'))
		self.assertTrue(dfa.evaluate_string('lolalol'))

	def test_star2(self):
		dfa = DFA('lola*')
		self.assertFalse(dfa.evaluate_string('lollol'))
		self.assertTrue(dfa.evaluate_string('lol'))
		self.assertTrue(dfa.evaluate_string('lola'))
		self.assertTrue(dfa.evaluate_string('lolaaaaaa'))

	def test_paren0(self):
		dfa = DFA('(lol)')
		self.assertTrue(dfa.evaluate_string('lol'))
		self.assertFalse(dfa.evaluate_string('(lol)'))

	def test_paren1(self):
		dfa = DFA('(lol|big)')
		self.assertTrue(dfa.evaluate_string('lol'))
		self.assertTrue(dfa.evaluate_string('big'))
		self.assertFalse(dfa.evaluate_string('lol|big'))

	def test_paren2(self):
		dfa = DFA('(lola*)')
		self.assertFalse(dfa.evaluate_string('lollol'))
		self.assertTrue(dfa.evaluate_string('lol'))
		self.assertTrue(dfa.evaluate_string('lola'))
		self.assertTrue(dfa.evaluate_string('lolaaaaaa'))

	def test_paren3(self):
		dfa = DFA('(lol)abc')
		self.assertTrue(dfa.evaluate_string('lolabc'))
		self.assertFalse(dfa.evaluate_string('(lol)'))
		self.assertFalse(dfa.evaluate_string('lol'))
		self.assertFalse(dfa.evaluate_string('abc'))

	def test_paren4(self):
		dfa = DFA('(lol)*')
		self.assertTrue(dfa.evaluate_string('lol'))
		self.assertTrue(dfa.evaluate_string(''))
		self.assertTrue(dfa.evaluate_string('lollol'))
		self.assertFalse(dfa.evaluate_string('loll'))

	def test_backslash(self):
		dfa = DFA('\\*')
		self.assertTrue(dfa.evaluate_string('*'))
		self.assertFalse(dfa.evaluate_string(''))
		self.assertFalse(dfa.evaluate_string('**'))

	def test_corner0(self):
		dfa = DFA('b(ahigh)*alow')
		self.assertTrue(dfa.evaluate_string('bahighalow'))
		self.assertTrue(dfa.evaluate_string('balow'))
		self.assertFalse(dfa.evaluate_string('bahigh'))
		self.assertTrue(dfa.evaluate_string('bahighahighalow'))

if __name__ == "__main__":
	unittest.main()