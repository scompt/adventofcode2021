import sys
from typing import TextIO
from sly import Lexer, Parser
from collections import defaultdict
import functools
import itertools
import copy

class CalcLexer(Lexer):
    tokens = { NAME, NUMBER, INPUT, ADD, MULTIPLY, DIVIDE, MODULO, EQUAL }
    ignore = ' \t;'
    # literals = { ';' }

    # Tokens
    NAME = r'[wxyz]'
    NUMBER = r'-?\d+'
    INPUT = r'inp'
    ADD = r'add'
    MULTIPLY = r'mul'
    DIVIDE = r'div'
    MODULO = r'mod'
    EQUAL = r'eql'

    # Ignored pattern
    ignore_newline = r'\n+'

    # Extra action for newlines
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1

class InputUnavailable(Exception):
    pass

class CalcParser(Parser):
    tokens = CalcLexer.tokens

    def __init__(self):
        self.names = defaultdict(lambda: 0)
        self.input = []
        self.read_values = []

    def add_input(self, value):
        self.input.append(value)

    @_('INPUT NAME')
    def statement(self, p):
        try:
            read_value = int(self.input.pop(0))
        except IndexError as e:
            raise InputUnavailable from e

        self.read_values.append(read_value)
        self.names[p.NAME] = read_value

    @_('MULTIPLY NAME expr')
    def statement(self, p):
        self.names[p.NAME] *= p.expr

    @_('DIVIDE NAME expr')
    def statement(self, p):
        self.names[p.NAME] //= p.expr

    @_('MODULO NAME expr')
    def statement(self, p):
        self.names[p.NAME] %= p.expr

    @_('EQUAL NAME expr')
    def statement(self, p):
        if self.names[p.NAME] == p.expr:
            self.names[p.NAME] = 1
        else:
            self.names[p.NAME] = 0

    @_('expr')
    def statement(self, p):
        pass

    @_('ADD NAME expr')
    def statement(self, p):
        self.names[p.NAME] += p.expr

    @_('NUMBER')
    def expr(self, p):
        return int(p.NUMBER)

    @_('NAME')
    def expr(self, p):
        return self.names[p.NAME]

def lex(textio: TextIO):
    lexed_lines = []
    lexer = CalcLexer()

    for line in textio.readlines():
        # line = line.strip()
        if line.strip():
            lexed_lines.append(list(lexer.tokenize(line)))
            # parser.parse(lexer.tokenize(line))
    
    return lexed_lines

def parse(lexed, inp):
    parser = CalcParser(iter(inp))
    for line in lexed:
        parser.parse(iter(line))
    return parser.names

monad = lex(open(sys.argv[1]))
# parser = CalcParser()
# parser.input = list('41299994879959')
# for line in monad:
#     parser.parse(iter(line))
# print(parser.names['z'])

for i in range(1,2):
    for j in range(1,2):
        for k in range(1,2):
            for l in range(7,9):
                for m in range(8,10):
                    for n in range(4,7):
                        for o in range(5,8):
                            for p in range(1,3):
                                for q in range(1,3):
                                    for r in range(1,3):
                                        for s in range(2,5):
                                            for t in range(1,4):
                                                for u in range(1, 3):
                                                    for v in range(5,8):
                                                        parser = CalcParser()
                                                        parser.add_input(str(i))
                                                        parser.add_input(str(j))
                                                        parser.add_input(str(k))
                                                        parser.add_input(str(l))
                                                        parser.add_input(str(m))
                                                        parser.add_input(str(n))
                                                        parser.add_input(str(o))
                                                        parser.add_input(str(p))
                                                        parser.add_input(str(q))
                                                        parser.add_input(str(r))
                                                        parser.add_input(str(s))
                                                        parser.add_input(str(t))
                                                        parser.add_input(str(u))
                                                        parser.add_input(str(v))

                                                        try:
                                                            for line in monad:
                                                                parser.parse(iter(line))
                                                        except InputUnavailable:
                                                            pass
                                                            # if parser.names['z'] ==0:
                                                            #     print(i, j, k, l, m, n, o, p, q, r, s, t, u, v, parser.names['z'])
                                                        if parser.names['z'] ==0:
                                                            print(f'{i}{j}{k}{l}{m}{n}{o}{p}{q}{r}{s}{t}{u}{v} {parser.names["z"]}')
                                                            raise Exception()


# # for model_number in itertools.product([str(i) for i in range(9,0,-1)], repeat=14):
# #     model_number = list(reversed(model_number))
# #     if all(model_number[i]=='9' for i in range(-4,0)):
# #         model_number = ''.join(model_number)
# #         # print(model_number)
# #     else:
# #         model_number = ''.join(model_number)
# #     try:
# #         parser, _ = woot(model_number)
# #     except:
# #         print(model_number)
# #     if parser.names['z'] == 0:
# #         print(model_number)
# #         break

# if __name__ == '__main__':
#     digits = range(9, 0, -1)

#     parsers = defaultdict(lambda: CalcParser())

#     model_numbers = [[1]*14]
#     # for model_number in model_numbers:


#     # for line in monad:
#     #     parser.parse(iter(line))

#     # valid = test_model_number([1]*14)
#     # print(valid)
#     # # with Pool(processes=4) as pool:
#     #     model_numbers = itertools.combinations_with_replacement(range(9, 0, -1), 14)
#     #     oot = pool.map(test_model_number, model_numbers)

#     #         # print(''.join(str(digit) for digit in model_number))
#     #         # variables = parse(monad, model_number)
#     #         # if variables['z'] == 0:
#     #         #     print(''.join(str(digit) for digit in model_number))
#     #         #     break