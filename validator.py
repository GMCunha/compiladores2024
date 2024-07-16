import lexer

class TreeNode: # estrutura de árvore para mensagem do analisador
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.left = None
        self.right = None

class Validator:       # classe do validador da gramática
    def __init__(self, terminals: list[str], non_terminals: list[str], permutations: dict[str, list[list[str]]], starting_symbol: str):
        self.terminals = terminals                  # terminais: lista de símbolos terminais da gramática
        self.non_terminals = non_terminals          # não-terminais: lista de símbolos não-terminais da gramática
        self.permutations = permutations            # permutations: mapeia cada símbolo não-terminal para suas produções
        self.starting_symbol = starting_symbol      # starting_symbol: símbolo inicial da gramática
        self.word = ''                              # palavra para validação (inicia vazia)
        self.position = 0                           # posição atual da palavra (inicia em 0)

    def assert_word(self, word: str) -> tuple[bool, int]:    # verifica se a palavra contém apenas caracteres válidos e, se não, retorna a posição do erro
        for i, char in enumerate(word):         # para cada caractere da palavra, verifica se está na lista de terminais da gramática
            if char not in self.terminals:
                return False, i                 # se o caractere não for um terminal, retorna False e a posição do caractere inválido
        return True, -1
    
    def first(self, symbol: str) -> set[str]:       # retorna o conjunto first de um símbolo não-terminal
        first_set = set()                                               # conjunto first
        for production in self.permutations.get(symbol, []):            # para cada produção do símbolo
            if production and production[0] in self.terminals:          # se o primeiro símbolo da produção for terminal, adiciona ao conjunto first
                first_set.add(production[0])
            elif production and production[0] in self.non_terminals:    # se o primeiro símbolo da produção for não-terminal, adiciona ao conjunto first
                first_set |= self.first(production[0])
        return first_set                                                # retorna o conjunto first
    
    def first_direct_path(self, symbol: str, target: str) -> list[str]:       # retorna o caminho direto para um símbolo terminal (deve pertencer ao conjunto first(symbol))
        if target not in self.first(symbol):                            # se o símbolo não estiver no conjunto first, retorna uma lista
            return []
        for production in self.permutations.get(symbol, []):            # para cada produção do símbolo
            if production and production[0] == target:                  # se o primeiro símbolo da produção for o alvo, retorna a produção
                return [production[0]]
            elif production and production[0] in self.non_terminals:    # se o primeiro símbolo da produção for não-terminal, procura o caminho direto para o alvo
                path = self.first_direct_path(production[0], target)    # procura o caminho direto para o alvo
                if path:                                                # se o caminho direto for encontrado, retorna a produção
                    return [production[0]] + path
    
    def remove_empty(self) -> None:     # remove símbolo vazio da palavra
        self.word = self.word.replace('&', '')
        self.word = self.word.replace(' ', '')  # remove espaços da palavra, já que não são considerados no lexer

    def assert_char(self, expected_char: str) -> bool:       # verifica se o caractere atual é igual ao esperado
        if self.position < len(self.word) and self.word[self.position] == expected_char:    # caso positivo, avança a posição e retorna True
            self.position += 1
            return True
        return False                                                                        # caso contrário, retorna False sem avançar a posição

    def validate(self, word: str) -> tuple[bool, str | None, TreeNode | None]:  # verifica se a palavra é valida para a gramática
        #retorna bool de validação, mensagem de erro (ou None se não houver erro), e a raiz da árvore (se palavra aceita)
        self.word = word       # palavra para validação
        self.remove_empty()   # remove vazio da palavra
        self.position = 0     # posição inicial
        root = TreeNode(self.starting_symbol)    # raiz da árvore
        valid_word, error_position = self.assert_word(self.word)   # verifica se a palavra contém apenas caracteres válidos
        if not valid_word:     # se a palavra contém caracteres inválidos, retorna erro na posição do caractere inválido
            return False, f"Caractere {self.word[error_position]} na posição {error_position} não foi encontrado na lista de terminais", None
        result, error, tree, pos = self._validate_symbol(self.starting_symbol, root)   # valida a palavra
        if result:     # se a palavra for válida, retorna True, None e a árvore de análise
            return True, None, tree
        return False, error or f"Erro inesperado após posição {pos}", None   # caso contrário, retorna False, mensagem de erro e None

    def _validate_symbol(self, symbol: str, node: TreeNode) -> tuple[bool, str | None, TreeNode, int]:  # valida simbolo da gramática com recursão, produz a árvore da análise
        # retorna bool de palavra válida ou não, mensagem de erro (ou None se não tiver erro), 
        # nó atual na árvore e a posição do erro (ou atual se não houver erro)
        if self.position == len(self.word):                 # verifica se o último caractere da palavra foi alcançado (caso algum simbolo não-terminal ainda deva ser validado)
            if '&' in [p[0] for p in self.first(symbol)]:   # se o vazio estiver no conjunto first do não-terminal atual, retorna True
                path = self.first_direct_path(symbol, '&')  # procura o caminho direto para o vazio
                current_node = node                         # nó atual
                for char in path:                           # cria caminho do nó atual até o vazio
                    print(char)
                    new_node = TreeNode(char)
                    if current_node.left is None:
                        current_node.left = new_node
                    else:
                        current_node.right = new_node
                    current_node = new_node
                return True, None, node, self.position      # retorna True, None (sem erro), nó atual e posição atual
            return False, "Palavra incompleta", node, self.position  # caso contrário, retorna False, mensagem de erro, nó atual e posição de erro
        error_position = self.position      # marca posição do erro
        error_symbol = symbol               # marca símbolo não-terminal onde ocorreu o erro
        best_error_message = None           # melhor mensagem de erro (mais específica, onde a posição do erro é a maior)

        for production in self.permutations.get(symbol, []):  # processa todas as produções do símbolo
            initial_position = self.position    # posição inicial (para retroceder em caso de erro)
            matched = True                      # flag de correspondência
            current_node = node                 # nó atual
            for char in production:             # processa cada símbolo da produção
                if char in self.non_terminals:      # se o símbolo for não-terminal, valida o símbolo
                    new_node = TreeNode(char)       # cria nó para o símbolo
                    if current_node.left is None:
                        current_node.left = new_node
                    else:
                        current_node.right = new_node
                    result, error_message, _, pos = self._validate_symbol(char, new_node)
                    if not result:                  # se a validação falhar, marca erro e sai do loop da produção atual
                        matched = False
                        if pos >= error_position:   # se a posição do erro for maior que a posição atual, atualiza a posição, símbolo e mensagem de erro
                            error_position = pos
                            error_symbol = char
                            best_error_message = error_message
                        break                       # sai do loop da produção atual (para tentar a próxima produção)
                    current_node = new_node     # atualiza o nó atual
                else:                               # se o símbolo for terminal, verifica se o caractere atual é igual ao símbolo
                    if self.assert_char(char):      # se for o caractere esperado, cria nó para o símbolo e avança para o próximo caractere
                        new_node = TreeNode(char)
                        if current_node.left is None:
                            current_node.left = new_node
                        else:
                            current_node.right = new_node
                        current_node = new_node
                    else:                           # se o caractere não for o esperado, marca erro e sai do loop da produção atual
                        matched = False
                        if self.position >= error_position:  # se a posição do erro for maior que a posição atual, atualiza a posição e símbolo do erro
                            error_position = self.position
                            error_symbol = char
                        break                      # sai do loop da produção atual (para tentar a próxima produção)
            if matched and self.position == len(self.word): # se corresponde e o final da palavra for alcançado, retorna True, None (sem erro), nó atual e posição atual
                return True, None, node, self.position
            self.position = initial_position    # retrocede a posição para a posição inicial da produção

        return False, best_error_message or f"Erro ao validar símbolo esperado {error_symbol} na posição {error_position}", node, error_position # retorna False, melhor mensagem de erro, nó atual e posição do erro
    
def print_tree(node: TreeNode, level: int=0):   # imprime a árvore de análise
    if node is not None:   # se o nó não for nulo, imprime de forma recursiva
        print(' ' * 4 * level + '->', node.symbol)  # 4 espaços são usados no lugar de \t pois a impressão da árvore é feita no console
        print_tree(node.left, level + 1)
        print_tree(node.right, level + 1)

def main():
    lxr = lexer.Lexer("input.txt")          # inicializa o analisador léxico
    palavra_teste = input("Digite a palavra para validação: ") # palavra para teste
    validator = Validator(lxr.terminals, lxr.non_terminals, lxr.permutations, lxr.starting_symbol) # teste de palavra inserida para validação
    resultado, erro, tree = validator.validate(palavra_teste)  # imprime o resultado e a árvore de análise se a palavra for aceita.
    if resultado:
        print("Palavra aceita pela gramática.")
        print("Árvore de análise:")
        print_tree(tree)
    else:
        print(f"Palavra rejeitada pela gramática. {erro}")

if __name__ == '__main__':
    main()
