from .ComEngineException import ComEngineException
from .Command import Command
import re


'''
Class used for creating Interpreter objects for interpreting commands
'''


class Interpreter:
    '''
    Interpreter constructor

    :param commands: list of Command objects to interpret
    :param command_char: str key in kwargs, default value is '/', character to denote a command
    :param trim_strings: bool key in kwargs, default value is True, whether to trim non-command strings or not
    :param disallowed_chars: str key in kwargs, default value is None, regular expression for illegal characters
    :raises TypeError: if commands is not a list of Command objects, command_char is not a single-character string,
                       trim_strings is not a bool, or disallowed_chars is not a str
    :raises sre_constants.error: if fails to compile a regular expression in disallowed_chars
    '''
    def __init__(self, commands, **kwargs):
        if type(commands) != list or not all([type(command) == Command for command in commands]):
            raise TypeError('commands should be a list of Command objects')

        self.commands = commands

        self.command_char = '/'
        self.trim_strings = True
        self.disallowed_chars = None

        self._disallowed_chars_re_obj = None

        if kwargs:
            if 'command_char' in kwargs:
                command_char = kwargs['command_char']

                if type(command_char) != str:
                    raise TypeError('command_char should be a str')
                elif len(command_char) != 1:
                    raise TypeError('command_char length should be exactly 1')

                self.command_char = command_char

            if 'trim_strings' in kwargs:
                trim_strings = kwargs['trim_strings']

                if type(trim_strings) != bool:
                    raise TypeError('trim_strings should be a bool')

                self.trim_strings = trim_strings

            if 'disallowed_chars' in kwargs:
                disallowed_chars = kwargs['disallowed_chars']

                if type(disallowed_chars) != str:
                    raise TypeError('disallowed_chars should be a str')

                self.disallowed_chars = disallowed_chars
                self._disallowed_chars_re_obj = re.compile(disallowed_chars)  # might fail, user should catch

    '''
    Method used to interpret a string potentially containing a command

    :param string: string to interpret
    :returns: ('command', *Command object*, *Command's func result*) if string is a command,
              ('string', string) otherwise
    :raises TypeError: if string is not of type str
    :raises ComEngineException: if an illegal character or an unknown command is found,
                                fails to interpret a command, or
                                there are too many/too few arguments to the command
    '''
    def interpret(self, string):
        if type(string) != str:
            raise TypeError('string should be a str')

        if self.trim_strings:
            return_string = string.strip()
        else:
            return_string = string

        string = string.lstrip()

        if self._disallowed_chars_re_obj and self._disallowed_chars_re_obj.search(string):
            raise ComEngineException('Found a disallowed character in string "' + string + '"')

        if string == '' or string[0] != self.command_char:
            return 'string', return_string

        string = string[1:]

        for command in self.commands:
            rest = command.try_remove_command_word(string)
            if rest:
                break

        if not rest:
            raise ComEngineException('Unknown command in "' + return_string + '"')

        _, string = rest

        args = []
        for lexeme in command.expects:
            res = lexeme.eat(string)
            if not res:
                raise ComEngineException('Failed to interpret command "' +
                                         command.command_word + '" from "' + return_string + '"')
            _, arg, rest = res
            args.append(arg)
            string = rest.lstrip()

        if string.strip() != '':
            raise ComEngineException('Too many arguments to command "' +
                                     command.command_word + '" in "' + return_string + '"')

        res = command.func(args)

        return 'command', command, res

    def __repr__(self):
        return ('<Interpreter commands=' + repr(self.commands) + ' command_char=' +
                repr(self.command_char) + ' trim_strings=' + repr(self.trim_strings) +
                ' disallowed_chars=' + repr(self.disallowed_chars) + '>')
