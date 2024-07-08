# Trabalho da Disciplina de compiladores

import lexer

class Validator:
    def __init__(self, terminals, non_terminals, permutations, starting_symbol):
        self.terminals = terminals
        self.non_terminals = non_terminals
        self.permutations = permutations
        self.starting_symbol = starting_symbol
        self.word = ''

    def assert_char(self, expected_char) -> bool:
        if self.word[self.position] == expected_char:
            self.position += 1
            return True
        return False

    def validate(self, word):
        self.word = word
        self.position = 0
        position_stack = []
        

