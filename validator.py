import lexer

class TreeNode:
    def __init__(self, symbol):
        self.symbol = symbol
        self.left = None
        self.right = None

class Validator:
    def __init__(self, terminals, non_terminals, permutations, starting_symbol):
        self.terminals = terminals
        self.non_terminals = non_terminals
        self.permutations = permutations
        self.starting_symbol = starting_symbol
        self.word = ''
        self.position = 0

    def assert_char(self, expected_char) -> bool:
        if self.position < len(self.word) and self.word[self.position] == expected_char:
            self.position += 1
            return True
        return False

    def validate(self, word):
        self.word = word
        self.position = 0
        root = TreeNode(self.starting_symbol)
        result, error, tree, pos = self._validate_symbol(self.starting_symbol, root)
        if result and self.position == len(word):
            return True, None, tree
        else:
            return False, error or f"Erro inesperado na posição {pos}", None

    def _validate_symbol(self, symbol, node):
        if self.position >= len(self.word):
            if '&' in [p[0] for p in self.permutations.get(symbol, [])]:
                return True, None, node, self.position
            else:
                return False, "Palavra incompleta", node, self.position
        for production in self.permutations.get(symbol, []):
            initial_position = self.position
            matched = True
            error_message = None
            error_position = self.position
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
                        error_position = pos
                        break
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
                        error_message = f"Erro ao validar símbolo {symbol} na posição {self.position}"
                        error_position = self.position
                        break

            if matched:
                return True, None, node, self.position
            else:
                self.position = initial_position

        return False, error_message or f"Erro ao validar símbolo {symbol} na posição {self.position}", node, error_position

def print_tree(node, level=0):
    if node is not None:
        print(' ' * 4 * level + '->', node.symbol)
        print_tree(node.left, level + 1)
        print_tree(node.right, level + 1)

def main():
    lxr = lexer.Lexer("input.txt")
    palavra_teste = input("Digite a palavra para validação: ")
    validator = Validator(lxr.terminals, lxr.non_terminals, lxr.permutations, lxr.starting_symbol)
    resultado, erro, tree = validator.validate(palavra_teste)
    if resultado:
        print("Palavra aceita pela gramática.")
        print("Árvore de análise:")
        print_tree(tree)
    else:
        print(f"Palavra rejeitada pela gramática. Erro: {erro}")

if __name__ == '__main__':
    main()