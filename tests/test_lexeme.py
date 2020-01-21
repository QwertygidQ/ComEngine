import unittest
from comengine import Lexeme, string_lexeme, integer_lexeme, number_lexeme, ComEngineException


class TestLexemeCreation(unittest.TestCase):
    def test_creation_success(self):
        Lexeme(r'[a-z]')

    def test_creation_invalid_regex(self):
        self.assertRaises(Exception, Lexeme, '[')

    def test_creation_regex_not_str(self):
        self.assertRaises(TypeError, Lexeme, True)


class TestLexemeEat(unittest.TestCase):
    def setUp(self):
        self.lexeme = Lexeme(r'[+-]?\d+')  # integer

    def test_eat_success(self):
        self.assertEqual(self.lexeme.eat('-3abc'), (True, '-3', 'abc'))
        self.assertEqual(self.lexeme.eat(' -3  5abc '), (True, '-3', '5abc '))

    def test_eat_empty(self):
        self.assertFalse(self.lexeme.eat(''))

    def test_eat_not_string(self):
        self.assertRaises(TypeError, self.lexeme.eat, None)

    def test_eat_match_failure(self):
        self.assertFalse(self.lexeme.eat('.3ASHDb-3+500'))


class TestLexemeRepr(unittest.TestCase):
    def test_repr_success(self):
        lexeme = Lexeme(r'[a-z]')
        self.assertEqual(repr(lexeme), '<Lexeme regex=' + repr(lexeme.regex) + '>')
        self.assertEqual(repr(number_lexeme), '<Lexeme regex=' + repr(number_lexeme.regex) + '>')
        self.assertEqual(repr(string_lexeme), '<Lexeme regex=' + repr(string_lexeme.regex) + '>')
        self.assertEqual(repr(integer_lexeme), '<Lexeme regex=' + repr(integer_lexeme.regex) + '>')
