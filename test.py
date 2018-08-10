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

if __name__ == "__main__":
	unittest.main()