import lexer

class TreeNode: # estrutura de árvore para mensagem do analisador
    def __init__(self, symbol):
        self.symbol = symbol
        self.left = None
        self.right = None

class Validator:       # classe do validador da gramática
    def __init__(self, terminals, non_terminals, permutations, starting_symbol):
        self.terminals = terminals
        self.non_terminals = non_terminals
        self.permutations = permutations            #permutations: mapeia cada símbolo não-terminal para suas produções.
        self.starting_symbol = starting_symbol
        self.word = ''
        self.position = 0

    def assert_word(self, word) -> tuple[bool, int]:
        for i, char in enumerate(word):
            if char not in self.terminals:
                return False, i
        return True, -1

    def assert_char(self, expected_char) -> bool:       # verifica se o caracter atual é igual ao esperado
        if self.position < len(self.word) and self.word[self.position] == expected_char:
            self.position += 1
            return True
        return False

    def validate(self, word): # verifica se a palavra é valida para a gramática
        #retorna bool de validação, mensagem de erro (ou None se não houver erro), e a raiz da árvore (se palavra aceita)
        self.word = word
        self.position = 0
        root = TreeNode(self.starting_symbol)
        result, error, tree, pos = self._validate_symbol(self.starting_symbol, root)
        valid_word, error_position = self.assert_word(word)
        if not valid_word:
            return False, f"Caractere {word[error_position]} na posição {error_position} não foi encontrado na lista de terminais", None
        if result and self.position == len(word):
            return True, None, tree
        return False, error or f"Erro inesperado após posição {pos}", None

    def _validate_symbol(self, symbol, node):       # valida simbolo da gramática com recurssão, produz a árvore da análise
        # retorna bool de palavra válida ou não, mensagem de erro (ou None se não tiver erro), 
        # nó atual na árvore e a posição do erro (ou atual se não houver erro)
        if self.position == len(self.word):
            if '&' in [p[0] for p in self.permutations.get(symbol, [])]:
                new_node = TreeNode('&')
                if node.left is None:
                    node.left = new_node
                else:
                    node.right = new_node
                node = new_node
                return True, None, node, self.position
            return False, "Palavra incompleta", node, self.position
        error_position = self.position
        error_symbol = symbol
        best_error_message = None

        for production in self.permutations.get(symbol, []):
            initial_position = self.position
            matched = True
            current_node = node
            for char in production:
                if char in self.non_terminals:
                    new_node = TreeNode(char)
                    if current_node.left is None:
                        current_node.left = new_node
                    else:
                        current_node.right = new_node
                    result, error_message, _, pos = self._validate_symbol(char, new_node)
                    if not result:
                        matched = False
                        if pos >= error_position:
                            error_position = pos
                            error_symbol = char
                            best_error_message = error_message
                        break
                    current_node = new_node
                else:
                    if self.assert_char(char):
                        new_node = TreeNode(char)
                        if current_node.left is None:
                            current_node.left = new_node
                        else:
                            current_node.right = new_node
                        current_node = new_node
                    else:
                        matched = False
                        if self.position > error_position:
                            error_position = self.position
                            error_symbol = char
                        break
            if matched:
                return True, None, node, self.position
            self.position = initial_position

        return False, best_error_message or f"Erro ao validar símbolo {error_symbol} na posição {error_position}", node, error_position
    
def print_tree(node, level=0):
    if node is not None:
        print(' ' * 4 * level + '->', node.symbol)
        print_tree(node.left, level + 1)
        print_tree(node.right, level + 1)

def main():

    lxr = lexer.Lexer("input.txt")          # inicializa o analisador léxico
    palavra_teste = input("Digite a palavra para validação: ")
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
