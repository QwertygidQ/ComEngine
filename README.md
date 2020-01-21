# ComEngine
[![Build Status](https://travis-ci.org/QwertygidQ/ComEngine.svg?branch=master)](https://travis-ci.org/QwertygidQ/ComEngine)
[![Coverage Status](https://coveralls.io/repos/github/QwertygidQ/ComEngine/badge.svg?branch=master)](https://coveralls.io/github/QwertygidQ/ComEngine?branch=master)
[![GitHub](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/QwertygidQ/ComEngine/blob/master/LICENSE)
[![GitHub release](https://img.shields.io/github/release/QwertygidQ/ComEngine.svg)](https://github.com/QwertygidQ/ComEngine/releases/latest)

A Python library for interpreting Minecraft-like commands

PyPI URL: https://pypi.org/project/ComEngine/

## Installation
```
pip install comengine
```

## Usage
### Basic example
```
from comengine import Command, Interpreter

command = Command('hello', lambda arg_list: 'Hello!')  # create a command with no arguments
interpreter = Interpreter([command])  # create an interpreter that can interpret this command
output_type, used_command, returned_val = interpreter.interpret('/hello')  # interpret the command
print(returned_val)  # outputs "Hello!"
```
Output:
```
Hello!
```

### Commands with arguments
```
from comengine import integer_lexeme, number_lexeme, Command, Interpreter

command = Command('sum', lambda arg_list: int(arg_list[0]) + float(arg_list[1]), [integer_lexeme, number_lexeme])  # create a command with two arguments: an integer, and a number
interpreter = Interpreter([command])  # create an interpreter that can interpret this command
output_type, used_command, returned_val = interpreter.interpret('/sum -22 -.3')  # interpret the command
print(returned_val)  # outputs "-22.3"
```
Output:
```
-22.3
```

### Commands with custom lexeme arguments
```
from comengine import Lexeme, Command, Interpreter

custom_lexeme = Lexeme(r'[A-Z]+')  # lexeme that describes a string of one or more capital letters
command = Command('say', lambda arg_list: arg_list[0], [custom_lexeme])  # create a command with an argument that should be a custom lexeme
interpreter = Interpreter([command])  # create an interpreter that can interpret this command
output_type, used_command, returned_val = interpreter.interpret('/say HELLO')  # interpret the command
print(returned_val)  # outputs "HELLO"
```
Output:
```
HELLO
```

### Interpreting a non-command string
```
from comengine import Command, Interpreter

command = Command('hello', lambda arg_list: 'Hello!')  # create a command with no arguments
interpreter = Interpreter([command])  # create an interpreter that can interpret this command
output_type, returned_val = interpreter.interpret('I\'m not a command!')  # interpret the string
print(returned_val)  # outputs "I'm not a command!"
```
Output:
```
I'm not a command!
```
