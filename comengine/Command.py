import types
import functools


'''
Class that represents a command that could be interpreted by an Interpreter
'''


class Command:
    '''
    Command constructor

    :param command_word: string that describes the Command's name
    :param func: function (can be built-in) that is called with a list of arguments whenever this Command is interpreted
    :param expects: list of Lexems that describe this Command's arguments (default value is [] - no arguments)
    :raises TypeError: if command_word is not a str or is empty, func is not a function, expects is not a list
    '''
    def __init__(self, command_word, func, expects=[]):
        if type(command_word) != str or command_word == '':
            raise TypeError('command_word should be a non-empty str')
        if not (isinstance(func, (types.FunctionType, types.BuiltinFunctionType, functools.partial)) or
                func == type):
            raise TypeError('func should be a function')
        if type(expects) != list:
            raise TypeError('expects should be a list')

        self.command_word = command_word
        self.expects = expects
        self.func = func

    '''
    Method that tries to remove this Command's command word from the beginning of a given string

    :param string: string from which to remove the command word
    :returns: (True, *rest of string*) if successfully removed, otherwise False
    :raises TypeError: if string is not of type str
    '''
    def try_remove_command_word(self, string):
        if type(string) != str:
            raise TypeError('string should be a str')

        string = string.lstrip()
        if (len(string) >= len(self.command_word) and
                string[:len(self.command_word)] == self.command_word):
            return True, string[len(self.command_word):].lstrip()

        return False

    def __repr__(self):
        return ('<Command command_word=' + repr(self.command_word) + ' func=' +
                repr(self.func) + ' expects=' + repr(self.expects) + '>')
