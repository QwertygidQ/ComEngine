from comengine import string_lexeme, integer_lexeme, Lexeme, Command, Interpreter
from random import randint


def random_number(arg_list):
    return randint(0, 100)


capital_letters_lexeme = Lexeme('[A-Z]+')  # one or more capital letters

teleport = Command('tp',
                   lambda arg_list: print('Teleported', arg_list[0], 'to', arg_list[1]),
                   [string_lexeme, string_lexeme])

say = Command('say',
              lambda arg_list: print('User #', arg_list[0], 'said', arg_list[1]),
              [integer_lexeme, string_lexeme])

sum = Command('sum',
              lambda arg_list: int(arg_list[0]) + int(arg_list[1]),
              [integer_lexeme, integer_lexeme])

rand = Command('rand', random_number)

scream = Command('scream',
                 lambda arg_list: print('AARGH!', arg_list[0]),
                 [capital_letters_lexeme])

interpreter = Interpreter([teleport, say, sum, rand, scream])

result1 = interpreter.interpret('/tp player1 player2')
print(result1)

print('=====================')
result2 = interpreter.interpret('/say 123 Hello!')
print(result2)

print('=====================')
result3 = interpreter.interpret('/sum -23 53')
print(result3)

print('=====================')
result4 = interpreter.interpret('/rand')
print(result4)

print('=====================')
result5 = interpreter.interpret('/scream HELLO')
print(result5)

print('=====================')
result6 = interpreter.interpret('Not a command!')
print(result6)

'''
Output:
Teleported player1 to player2
('command', <Command command_word='tp' func=<function <lambda> at 0x7fdf49f398c8>
expects=[<Lexeme regex='[^\\s]+'>, <Lexeme regex='[^\\s]+'>]>, None)
=====================
User # 123 said Hello!
('command', <Command command_word='say' func=<function <lambda> at 0x7fdf49f39950>
expects=[<Lexeme regex='[+-]?\\d+'>, <Lexeme regex='[^\\s]+'>]>, None)
=====================
('command', <Command command_word='sum' func=<function <lambda> at 0x7fdf49f399d8>
expects=[<Lexeme regex='[+-]?\\d+'>, <Lexeme regex='[+-]?\\d+'>]>, 30)
=====================
('command', <Command command_word='rand' func=<function random_number at 0x7fdf4bd3ee18>
expects=[]>, 43)
=====================
AARGH! HELLO
('command', <Command command_word='scream' func=<function <lambda> at 0x7fdf49f39a60>
expects=[<Lexeme regex='[A-Z]+'>]>, None)
=====================
('string', 'Not a command!')
'''
