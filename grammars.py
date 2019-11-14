"""
Using generative grammars to produce random Python programs
"""

import random
from enum import Enum, auto
from typing import List, Tuple


INDENT, DEDENT = object(), object()
class NT(Enum):
    """Enumeration of non-terminal symbols"""
    PROGRAM = auto()
    IMPORT = auto()
    STMTS = auto()
    STMT = auto()
    PREFIX = auto()
    ASSIGN = auto()
    BLOCK = auto()
    BLOCK_NAME = auto()
    DEF = auto()
    CLASS = auto()
    PARAMS = auto()
    LONG_NAME = auto()
    NAME = auto()

grammar = {
    NT.PROGRAM: [[NT.IMPORT, NT.PROGRAM], [NT.STMTS]],
    NT.IMPORT: [['import ', NT.NAME, '\n']],
    NT.STMTS: [[NT.STMT], [NT.BLOCK], [NT.STMT, NT.STMTS], [NT.BLOCK, NT.STMTS]],
    NT.STMT: [[NT.LONG_NAME, NT.ASSIGN, NT.LONG_NAME, '\n'], [NT.PREFIX, NT.LONG_NAME, '\n'], ['pass', '\n']],
    NT.PREFIX: [['del '], ['return '], ['raise '], ['assert '], ['global ']],
    NT.ASSIGN: [[' = '], [' += '], [' -= '], [' *= '], [' |= '], [' &= ']],

    NT.BLOCK: [[NT.BLOCK_NAME, NT.NAME, '(', NT.PARAMS, '):', INDENT, '\n', NT.STMTS, DEDENT]],
    NT.BLOCK_NAME: [['def '], ['class ']],
    NT.PARAMS: [[NT.NAME, ', ', NT.PARAMS], [NT.NAME]],

    NT.LONG_NAME: [[NT.LONG_NAME, '.', NT.NAME], [NT.NAME]],
    NT.NAME: [['foo'], ['bar'], ['baz'], ['spam'], ['eggs']]
}

def gen_strings(start_string):
    stack: List[Tuple[int, List]] = [(0, start_string)]

    while stack:
        depth, string = stack.pop()

        next_nonterminal = next((x for x in string if isinstance(x, NT)), None)
        if next_nonterminal is None:
            # Yield a string of terminals
            yield string
        elif depth < 500:  # Limit depth to avoid infinite recursion
            # Apply one of the grammar rules to the next nonterminal
            idx = string.index(next_nonterminal)

            # Apply the production rules and stack the results
            for rhs in sorted(grammar[next_nonterminal], key=lambda x: random.random()):
                new_string = list(string)
                new_string[idx: idx+1] = rhs
                stack.append((depth + 1, new_string))

def format_program(program):
    indents = []
    for string in program:
        if string is INDENT:
            indents.append('    ')
        elif string is DEDENT:
            indents.pop()
        elif string == '\n':
            print('\n' + ''.join(indents), end='')
        else:
            print(string, end='')

gen = gen_strings([NT.PROGRAM])
programs = list(sorted([next(gen) for _ in range(20)], key=len))
format_program(programs[-1])