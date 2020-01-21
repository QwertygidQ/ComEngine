import re


'''
Class that represents a lexeme for interpreting - used for command arguments
'''


class Lexeme:
    '''
    Lexeme constructor

    :param regex: regular expression string that defines this lexem
    :raises TypeError: if the regular expression is not of type str
    :raises sre_constants.error: if fails to compile a regular expression in regex
    '''
    def __init__(self, regex):
        if type(regex) != str:
            raise TypeError('regex should be a str')

        self.regex = regex
        self.regex_obj = re.compile(regex)  # might fail, user should catch

    '''
    Method used to search for this lexeme in the beginning of the string

    :param string: string to search in
    :returns: (True, *matched string*, *rest of string*) if succeeded, False otherwise
    :raises TypeError: if the string is not of type str
    '''
    def eat(self, string):
        if type(string) != str:
            raise TypeError('string should be a str')

        string = string.lstrip()
        match = self.regex_obj.match(string)
        if match:
            return True, match.group(), string[match.end():].lstrip()
        else:
            return False

    def __repr__(self):
        return '<Lexeme regex=' + repr(self.regex) + '>'


'''
Default lexeme that matches all strings without whitespace characters
'''
string_lexeme = Lexeme(r'[^\s]+')

'''
Default lexeme that matches integer strings that Python can convert to int
'''
integer_lexeme = Lexeme(r'[+-]?\d+')

'''
Default lexeme that matches number strings that Python can convert to float
'''
number_lexeme = Lexeme(r'[+-]?(\d+(\.\d*)?|\.\d+)')
