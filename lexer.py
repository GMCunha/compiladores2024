# Trabalho da Disciplina de compiladores

class Lexer:
    def __init__(self, input_path):
        self.__input_path = input_path
        self.__input_file = open(input_path, 'r')
        self.__input = self.remove_whitespace(self.__input_file.read())
        self.__input_file.close()
        self.__pos = 0
        self.__char = self.__input[self.__pos]
        self.terminals = ['&']
        self.non_terminals = []
        self.permutations = {}
        self.starting_symbol = None
        self.process_grammar()


    def next_char(self):
        self.__pos += 1
        if self.__pos < len(self.__input):
            self.__char = self.__input[self.__pos]
        else:
            self.__char = None


    def assert_char(self, expected_char):
        if self.__char == expected_char:
            self.next_char()
        else:
            raise Exception(f'Expected {expected_char}, got {self.__char}')


    def process_grammar(self):
        if self.__char == 'G':
            self.next_char()
            self.assert_char('=')
        self.assert_char('(')
        self.process_non_terminals()
        self.assert_char(',')
        self.process_terminals()
        self.assert_char(',')
        self.process_permutations()
        self.assert_char(',')
        self.process_starting_symbol()
        self.assert_char(')')

    
    def process_non_terminals(self):
        self.assert_char('{')
        while True:
            if self.__char in self.terminals:
                raise Exception('Non-terminal symbol is also a terminal symbol')
            if self.__char in self.non_terminals:
                raise Exception('Non-terminal symbol is repeated')
            
            self.non_terminals.append(self.__char)
            self.next_char()
            if self.__char == '}':
                self.next_char()
                break
            self.assert_char(',')
        print(self.non_terminals)


    def process_terminals(self):
        self.assert_char('{')
        while True:
            if self.__char in self.non_terminals:
                raise Exception('Terminal symbol is also a non-terminal symbol')
            if self.__char in self.terminals and self.__char != '&':
                raise Exception('Terminal symbol is repeated')
            if self.__char == '&':
                self.terminals.remove('&')
            
            self.terminals.append(self.__char)
            self.next_char()
            if self.__char == '}':
                self.next_char()
                break
            self.assert_char(',')
        print(self.terminals)
        

    def process_permutations(self):
        self.assert_char('{')
        if self.__char == '\n':
            self.assert_char('\n')
        while True:
            self.process_permutation()
            if self.__char == '}':
                self.next_char()
                break
            self.assert_char('\n')
            if self.__char == '}':
                self.next_char()
                break
        for key, value in self.permutations.items():
            print(key, " -> ", end='')
            print(" | ".join(["".join(x) for x in value]))


    def process_permutation(self):
        non_terminal = self.__char
        if non_terminal not in self.non_terminals:
            raise Exception('Non-terminal symbol not found')
        self.next_char()
        self.assert_char('-')
        self.assert_char('>')
        self.process_permutation_body(non_terminal)


    def process_permutation_body(self, non_terminal):
        if non_terminal not in self.permutations:
            self.permutations[non_terminal] = []
        while self.__char != '\n' and self.__char != '}':
            if self.__char not in self.terminals and self.__char not in self.non_terminals:
                raise Exception('Symbol not found')
            if self.__char in self.terminals:
                perm = []
                while True:
                    perm.append(self.__char)
                    self.next_char()
                    if self.__char == '|':
                        self.next_char()
                        break
                    if self.__char == '\n':
                        break
                    if self.__char in self.non_terminals:
                        perm.append(self.__char)
                        self.next_char()
                        if self.__char != '\n':
                            self.assert_char('|')
                        break
                self.permutations[non_terminal].append(perm)
            if self.__char in self.non_terminals:
                perm = [self.__char]
                self.next_char()
                if self.__char != '\n':
                    self.assert_char('|')
                self.permutations[non_terminal].append(perm)


    def process_starting_symbol(self):
        self.starting_symbol = self.__char
        if self.starting_symbol not in self.non_terminals:
            raise Exception('Starting symbol is not a non-terminal symbol')
        self.next_char()
        print(self.starting_symbol)


    @staticmethod
    def remove_whitespace(input):
        return input.replace(' ', '').replace('\t', '')
    

if __name__ == '__main__':
    lexer = Lexer('input.txt')

