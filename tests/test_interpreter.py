import unittest
from comengine import Interpreter, Command, string_lexeme, number_lexeme, ComEngineException


class TestInterpreterCreation(unittest.TestCase):
    def setUp(self):
        self.command = Command('command1', lambda arg_list: arg_list)
        self.command2 = Command('command2', lambda arg_list: arg_list[::-1])

    def test_interpreter_creation_success(self):
        Interpreter([self.command])
        Interpreter([self.command, self.command2])
        Interpreter([self.command], command_char='!')
        Interpreter([self.command], trim_strings=False)
        Interpreter([self.command], disallowed_chars=r'[a-z]')

    def test_interpreter_creation_commands_not_list(self):
        self.assertRaises(TypeError, Interpreter, bool)

    def test_interpreter_creation_commands_not_all_commands(self):
        self.assertRaises(TypeError, Interpreter, [self.command, .1])

    def test_interpreter_creation_CC_not_len_1(self):
        self.assertRaises(TypeError, Interpreter, [self.command], command_char='!?')

    def test_interpreter_creation_CC_not_str(self):
        self.assertRaises(TypeError, Interpreter, [self.command], command_char=10)

    def test_interpreter_creation_trim_not_bool(self):
        self.assertRaises(TypeError, Interpreter, [self.command], trim_strings='YES')

    def test_interpreter_creation_disallowed_not_str(self):
        self.assertRaises(TypeError, Interpreter, [self.command], disallowed_chars=False)

    def test_interpreter_creation_disallowed_invalid(self):
        self.assertRaises(Exception, Interpreter, [self.command], disallowed_chars=r'[')


class TestInterpreterInterpret(unittest.TestCase):
    def setUp(self):
        self.command = Command('command1', lambda arg_list: arg_list, [string_lexeme, string_lexeme])
        self.command2 = Command('command2', lambda arg_list: arg_list[::-1], [string_lexeme, number_lexeme])
        self.interpreter = Interpreter([self.command, self.command2])
        self.interpreter2 = Interpreter([self.command, self.command2], trim_strings=False)
        self.interpreter3 = Interpreter([self.command, self.command2], disallowed_chars=r'[a-z]')

    def test_interpret_success(self):
        self.assertEqual(self.interpreter.interpret('/command1 string123 -.5'),
                         ('command', self.command, ['string123', '-.5']))

        self.assertEqual(self.interpreter.interpret('  /command2   string123    -.5  '),
                         ('command', self.command2, ['-.5', 'string123']))

    def test_interpret_string_not_str(self):
        self.assertRaises(TypeError, self.interpreter.interpret, None)

    def test_interpret_trim(self):
        self.assertEqual(self.interpreter.interpret('    Not a command         '),
                         ('string', 'Not a command'))
        self.assertEqual(self.interpreter2.interpret('    Not a command         '),
                         ('string', '    Not a command         '))

    def test_interpret_disallowed(self):
        self.assertRaises(ComEngineException, self.interpreter3.interpret, 'We\'re doomed!')

    def test_interpret_empty(self):
        self.assertEqual(self.interpreter.interpret(''), ('string', ''))
        self.assertEqual(self.interpreter.interpret('        '), ('string', ''))
        self.assertEqual(self.interpreter2.interpret('        '), ('string', '        '))

    def test_interpret_unknown_command(self):
        self.assertRaises(ComEngineException, self.interpreter.interpret, '/not-a-command arg1')

    def test_interpret_wrong_arg(self):
        self.assertRaises(ComEngineException, self.interpreter.interpret, '/command2 arg1 arg2')

    def test_interpreter_not_enough_args(self):
        self.assertRaises(ComEngineException, self.interpreter.interpret, '/command1 arg1   ')

    def test_interpreter_too_many_args(self):
        self.assertRaises(ComEngineException, self.interpreter.interpret, '/command1 arg1 arg2 arg3')


class TestInterpreterRepr(unittest.TestCase):
    def test_interpreter_repr_success(self):
        command = Command('command1', lambda arg_list: arg_list, [string_lexeme, string_lexeme])
        command2 = Command('command2', lambda arg_list: arg_list[::-1], [string_lexeme, number_lexeme])
        interpreter = Interpreter([command, command2])

        self.assertEqual(repr(interpreter), '<Interpreter commands=' + repr(interpreter.commands) +
                         ' command_char=' + repr(interpreter.command_char) + ' trim_strings=' +
                         repr(interpreter.trim_strings) + ' disallowed_chars=' +
                         repr(interpreter.disallowed_chars) + '>')
