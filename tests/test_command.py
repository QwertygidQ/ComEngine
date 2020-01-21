import unittest
import functools
from comengine import string_lexeme, integer_lexeme, Command


class TestCommandCreation(unittest.TestCase):
    def test_command_creation_success(self):
        Command('command', lambda arg_list: True)
        Command('command', lambda arg_list: True, [string_lexeme, integer_lexeme])

    def test_command_creation_command_word_not_str(self):
        self.assertRaises(TypeError,
                          Command, string_lexeme, lambda arg_list: True,
                          [string_lexeme, integer_lexeme])

    def test_command_creation_command_word_empty(self):
        self.assertRaises(TypeError,
                          Command, '', lambda arg_list: True,
                          [string_lexeme, integer_lexeme])

    def test_command_creation_func_not_callable(self):
        self.assertRaises(TypeError,
                          Command, 'command', Command)

    def test_command_creation_func_builtin(self):
        Command('command', open)

    def test_command_creation_func_partial(self):
        f = functools.partial(int, base=2)
        Command('command', f)

    def test_command_creation_func_type(self):
        Command('command', type)

    def test_command_creation_expects_not_list(self):
        self.assertRaises(TypeError,
                          Command, 'command', lambda arg_list: None,
                          self.test_command_creation_func_type)


class TestCommandRemoveCW(unittest.TestCase):
    def setUp(self):
        self.command = Command('teleport-to', lambda arg_list: arg_list,
                               [string_lexeme, string_lexeme])

    def test_command_remove_CW_success(self):
        self.assertEqual(self.command.try_remove_command_word('teleport-to u1 u2'), (True, 'u1 u2'))
        self.assertEqual(self.command.try_remove_command_word('   teleport-to  u1   u2   '), (True, 'u1   u2   '))

    def test_command_remove_CW_string_not_str(self):
        self.assertRaises(TypeError, self.command.try_remove_command_word, 12)

    def test_command_remove_CW_string_less_than_CW(self):
        self.assertFalse(self.command.try_remove_command_word('telep'))
        self.assertFalse(self.command.try_remove_command_word('   telep'))

    def test_command_remove_CW_no_CW(self):
        self.assertFalse(self.command.try_remove_command_word('teleport-ta'))
        self.assertFalse(self.command.try_remove_command_word('   teleport-ta'))


class TestCommandRepr(unittest.TestCase):
    def test_command_repr_success(self):
        command = Command('teleport-to', lambda arg_list: arg_list,
                          [string_lexeme, integer_lexeme])
        self.assertEqual(repr(command), '<Command command_word=' + repr(command.command_word) + ' func=' +
                         repr(command.func) + ' expects=' + repr(command.expects) + '>')
