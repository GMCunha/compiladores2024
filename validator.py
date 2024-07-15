import lexer

class TreeNode: # estrutura de árvore para mensagem do analisador
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.left = None
        self.right = None

class Validator:       # classe do validador da gramática
    def __init__(self, terminals: list[str], non_terminals: list[str], permutations: dict[str, list[list[str]]], starting_symbol: str):
        self.terminals = terminals
        self.non_terminals = non_terminals
        self.permutations = permutations            #permutations: mapeia cada símbolo não-terminal para suas produções.
        self.starting_symbol = starting_symbol
        self.word = ''
        self.position = 0

    def assert_word(self, word: str) -> tuple[bool, int]:    # verifica se a palavra contém apenas caracteres válidos e, se não, retorna a posição do erro
        for i, char in enumerate(word):
            if char not in self.terminals:
                return False, i
        return True, -1
    
    def first(self, symbol: str) -> set[str]:       # retorna o conjunto first de um símbolo não-terminal
        first_set = set()
        for production in self.permutations.get(symbol, []):
            if production and production[0] in self.terminals:
                first_set.add(production[0])
            elif production and production[0] in self.non_terminals:
                first_set |= self.first(production[0])
        return first_set
    
    def first_direct_path(self, symbol: str, target: str) -> list[str]:       # retorna o caminho direto do conjunto first de um símbolo não-terminal para um símbolo terminal
        if target not in self.first(symbol):
            return []
        for production in self.permutations.get(symbol, []):
            if production and production[0] == target:
                return [production[0]]
            elif production and production[0] in self.non_terminals:
                path = self.first_direct_path(production[0], target)
                if path:
                    return [production[0]] + path
    
    def remove_empty(self):     # remove vazio da palavra
        self.word = self.word.replace('&', '')

    def assert_char(self, expected_char: str) -> bool:       # verifica se o caracter atual é igual ao esperado
        if self.position < len(self.word) and self.word[self.position] == expected_char:
            self.position += 1
            return True
        return False

    def validate(self, word: str) -> tuple[bool, str | None, TreeNode | None]: # verifica se a palavra é valida para a gramática
        #retorna bool de validação, mensagem de erro (ou None se não houver erro), e a raiz da árvore (se palavra aceita)
        self.word = word
        self.remove_empty()
        self.position = 0
        root = TreeNode(self.starting_symbol)
        result, error, tree, pos = self._validate_symbol(self.starting_symbol, root)
        valid_word, error_position = self.assert_word(self.word)
        if not valid_word:
            return False, f"Caractere {self.word[error_position]} na posição {error_position} não foi encontrado na lista de terminais", None
        if result:
            return True, None, tree
        return False, error or f"Erro inesperado após posição {pos}", None

    def _validate_symbol(self, symbol: str, node: TreeNode) -> tuple[bool, str | None, TreeNode, int]:       # valida simbolo da gramática com recurssão, produz a árvore da análise
        # retorna bool de palavra válida ou não, mensagem de erro (ou None se não tiver erro), 
        # nó atual na árvore e a posição do erro (ou atual se não houver erro)
        if self.position == len(self.word):
            if '&' in [p[0] for p in self.first(symbol)]:
                path = self.first_direct_path(symbol, '&')
                current_node = node
                for char in path:
                    print(char)
                    new_node = TreeNode(char)
                    if current_node.left is None:
                        current_node.left = new_node
                    else:
                        current_node.right = new_node
                    current_node = new_node
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
                        if self.position >= error_position:
                            error_position = self.position
                            error_symbol = char
                        break
            if matched and self.position == len(self.word):
                return True, None, node, self.position
            self.position = initial_position

        return False, best_error_message or f"Erro ao validar símbolo esperado {error_symbol} na posição {error_position}", node, error_position
    
def print_tree(node: TreeNode, level: int=0):
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
