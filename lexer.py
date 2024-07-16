# Trabalho para a disciplina de Compiladores
# Arquivo de implementação do Lexer
# Formato da entrada:
# G = (NT, T, P, S), onde:
# G é a gramática (trecho opcional),
# NT é o conjunto de símbolos não-terminais, separados por vírgula e entre chaves,
# T é o conjunto de símbolos terminais, separados por vírgula e entre chaves,
# P é o conjunto de permutações, separados por quebra de linha e entre chaves (podendo possuir quebra de linha antes do início e após o final),
# S é o símbolo inicial, único e não-terminal
# Alunos: Guilherme Medeiros da Cunha e Josiane Cristine Aggens

class Lexer:
    def __init__(self, input_path: str): # Inicializa o Lexer com o arquivo de entrada
        self.__input_file = open(input_path, 'r')                           # Abre o arquivo de entrada.
        self.__input = self.remove_whitespace(self.__input_file.read())     # Lê o conteúdo do arquivo de entrada e remove espaços e tabulações.
        self.__input_file.close()                                           # Fecha o arquivo de entrada.
        self.__pos = 0                                                      # Posição atual no conteúdo do arquivo de entrada.
        self.__char = self.__input[self.__pos]                              # Caractere atual no conteúdo do arquivo de entrada.
        self.terminals = ['&']                                              # Símbolos terminais da gramática (inicializado com o símbolo vazio).
        self.non_terminals = []                                             # Símbolos não-terminais da gramática.
        self.permutations = {}                                              # Permutações da gramática.
        self.starting_symbol = None                                         # Símbolo inicial da gramática.
        self.process_grammar()                                              # Processa a gramática do arquivo de entrada.

    def next_char(self):  # Avança para o próximo caractere no conteúdo do arquivo de entrada.
        self.__pos += 1                                 # Avança para o próximo caractere.
        if self.__pos < len(self.__input):              # Se a posição atual for menor que o tamanho do conteúdo do arquivo de entrada, atualiza o caractere atual.
            self.__char = self.__input[self.__pos]
        else:                                           # Caso contrário, o caractere atual é nulo.
            self.__char = None

    def assert_char(self, expected_char: str): # Garante que o caractere atual é o esperado.
        if self.__char == expected_char:    # Se o caractere atual for o caractere esperado, avança para o próximo caractere.
            self.next_char()
        else:                               # Caso contrário, lança uma exceção
            raise Exception(f'Expected {expected_char}, got {self.__char}')

    def process_grammar(self):  # Processa a gramática do arquivo de entrada.
        if self.__char == 'G':          # Inicio 'G = ' da gramática., opcional
            self.next_char()
            self.assert_char('=')
        self.assert_char('(')           # Inicio '(' da gramática definição própria da gramática.
        self.process_non_terminals()    # Processa os símbolos não-terminais da gramática.
        self.assert_char(',')           # Separador entre primeiro e segundo elementos da quadrupla.
        self.process_terminals()        # Processa os símbolos terminais da gramática.
        self.assert_char(',')           # Separador entre segundo e terceiro elementos da quadrupla.
        self.process_permutations()     # Processa as permutações da gramática.
        self.assert_char(',')           # Separador entre terceiro e quarto elementos da quadrupla.
        self.process_starting_symbol()  # Processa o símbolo inicial da gramática.
        self.assert_char(')')           # Fim ')' da gramática.

    def process_non_terminals(self):        # Processa e armazena os símbolos não-terminais da gramática.
        self.assert_char('{')                                                       # Inicio '{' dos símbolos não-terminais.
        while True:                                                                 # Loop para processar todos os símbolos não-terminais.
            if self.__char in self.terminals:                                       # Se o caractere atual for um símbolo terminal, lança uma exceção.
                raise Exception('Non-terminal symbol is also a terminal symbol')
            if self.__char in self.non_terminals:                                   # Se o caractere atual for um símbolo não-terminal repetido, lança uma exceção.
                raise Exception('Non-terminal symbol is repeated')
            
            self.non_terminals.append(self.__char)                                  # Adiciona o símbolo não-terminal à lista de símbolos não-terminais.
            self.next_char()
            if self.__char == '}':                                                  # Se o caractere atual for '}', avança para o próximo caractere e encerra o loop.
                self.next_char()
                break
            self.assert_char(',')                                                   # Se o caractere atual não for '}', garante que o caractere atual é ',' para separação.

    def process_terminals(self):       # Processa e armazena os símbolos terminais da gramática.
        self.assert_char('{')                                                       # Inicio '{' dos símbolos terminais.
        while True:                                                                 # Loop para processar todos os símbolos terminais.
            if self.__char in self.non_terminals:                                   # Se o caractere atual for um símbolo não-terminal, lança uma exceção.
                raise Exception('Terminal symbol is also a non-terminal symbol')
            if self.__char in self.terminals and self.__char != '&':                # Se o caractere atual for um símbolo terminal repetido, lança uma exceção.
                raise Exception('Terminal symbol is repeated')
            if self.__char == '&':                                                  # Como adição de símbolo vazio é opcional, verifica se o caractere atual é '&'
                self.terminals.remove('&')                                          # e caso seja, impede que o símbolo vazio seja repetido.
            
            self.terminals.append(self.__char)                                      # Adiciona o símbolo terminal à lista de símbolos terminais.
            self.next_char()
            if self.__char == '}':                                                  # Se o caractere atual for '}', avança para o próximo caractere e encerra o loop.
                self.next_char()
                break
            self.assert_char(',')                                                   # Se o caractere atual não for '}', garante que o caractere atual é ',' para separação.

    def process_permutations(self):     # Processa e armazena as permutações da gramática.
        self.assert_char('{')                           # Inicio '{' das permutações.
        if self.__char == '\n':                         # Pode haver uma quebra de linha após o início das permutações.
            self.assert_char('\n')
        while True:                                     # Loop para processar todas as permutações.
            self.process_permutation()                  # Processa uma permutação individual.
            if self.__char == '}':                      # Se o caractere atual for '}', avança para o próximo caractere e encerra o loop.
                self.next_char()
                break
            self.assert_char('\n')                      # Se o caractere atual não for '}', garante que o caractere atual é '\n' para separação.
            if self.__char == '}':                      # Repete o processo de verificação caso haja uma quebra de linha antes do final das permutações.
                self.next_char()
                break

    def process_permutation(self):          # Processa uma permutação individual da gramática.
        non_terminal = self.__char                              # Símbolo não-terminal da permutação.
        if non_terminal not in self.non_terminals:              # Se o símbolo não-terminal não for encontrado, lança uma exceção.
            raise Exception('Non-terminal symbol not found')
        self.next_char()                                        # Avança para o próximo caractere.
        self.assert_char('-')                                   # Garante que início da permutação é '->'.
        self.assert_char('>')
        self.process_permutation_body(non_terminal)             # Processa o corpo da permutação.

    def process_permutation_body(self, non_terminal: str):       # Processa corpo da permutação e armazena as produções num dicionário.
        if non_terminal not in self.permutations:                                           # Adiciona o símbolo não-terminal à lista de permutações da gramática caso ausente.
            self.permutations[non_terminal] = []                                            # Inicializa a lista de permutações do símbolo não-terminal.
        while self.__char != '\n' and self.__char != '}':                                   # Loop para processar todas as produções da permutação.
            if self.__char not in self.terminals and self.__char not in self.non_terminals: # Lança uma exceção caso o símbolo não seja terminal nem não-terminal.
                raise Exception('Symbol not found')
            if self.__char in self.terminals:                       # Se o caractere atual for um símbolo terminal, adiciona às permutações do símbolo não-terminal.
                perm = []                                           # Inicializa a produção.
                while True:                                         # Loop para processar todos os símbolos terminais da produção.
                    perm.append(self.__char)                        # Adiciona o símbolo terminal à produção e avança para o próximo caractere.
                    self.next_char()
                    if self.__char == '|':                          # Se for o caractere de separação '|', avança para o próximo caractere e encerra a produção.
                        self.next_char()
                        break
                    if self.__char == '\n':                         # Se for uma quebra de linha, encerra a produção (nova linha será processada na próxima iteração).
                        break
                    if self.__char in self.non_terminals:           # Se o caractere atual for um símbolo não-terminal, adiciona à permutação e encerra.
                        perm.append(self.__char)
                        self.next_char()
                        if self.__char != '\n':                     # Se não for uma quebra de linha, garante que o caractere atual é '|'.
                            self.assert_char('|')                   # Isso garante que a gramática possua no máximo 1 símbolo não-terminal por produção.
                        break                                       # Além disso, garante que o símbolo não-terminal seja o último da produção.
                self.permutations[non_terminal].append(perm)        # Adiciona a produção à lista de permutações do símbolo não-terminal.
            if self.__char in self.non_terminals:                   # Se o caractere atual for um símbolo não-terminal, adiciona às permutações do símbolo não-terminal.
                perm = [self.__char]                                # Inicializa a produção com o símbolo não-terminal e avança para o próximo caractere.
                self.next_char()
                if self.__char != '\n':                             # Se não for uma quebra de linha, garante que o caractere atual é '|'.
                    self.assert_char('|')                           # Isso garante que garante que o símbolo não-terminal seja o último (único) da produção.
                self.permutations[non_terminal].append(perm)        # Adiciona a produção à lista de permutações do símbolo não-terminal.

    def process_starting_symbol(self): # Processa e armazena símbolo inicial da gramática, exception: símbolo não-terminal.
        self.starting_symbol = self.__char                      # Símbolo inicial da gramática.
        if self.starting_symbol not in self.non_terminals:      # Se o símbolo inicial não for um símbolo não-terminal, lança uma exceção.
            raise Exception('Starting symbol is not a non-terminal symbol')
        self.next_char()
        
    def print_grammar(self):    # Exibe a gramática em ordem de declaração da quadrupla.
        print("Non-terminals: ", self.non_terminals)            # Exibe os símbolos não-terminais da gramática.
        print("Terminals: ", self.terminals)                    # Exibe os símbolos terminais da gramática.
        print("Permutations: {")                                # Exibe as permutações da gramática.
        for key, value in self.permutations.items():
            print(key, " -> ", end='')
            print(" | ".join(["".join(x) for x in value]))
        print("}")
        print("Starting symbol: ", self.starting_symbol)        # Exibe o símbolo inicial da gramática.

    @staticmethod
    def remove_whitespace(input: str) -> str: # Remove espaços e tabulações do conteúdo do arquivo de entrada.
        return input.replace(' ', '').replace('\t', '')
