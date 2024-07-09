import lexer

def main():
    lxr = lexer.Lexer("input.txt")
    palavra_teste = input("Digite a palavra para validação: ")
    interpreter = Interpreter(lxr)
    resultado, erro = interpreter.word_validate(palavra_teste)
    if resultado:
        print("Palavra aceita pela gramática.")
    else:
        print(f"Palavra rejeitada pela gramática. Erro: {erro}")


class Interpreter:
    def __init__(self, lexer):
        self.lexer = lexer
        self.grammar = lexer.permutations
        self.starting_symbol = lexer.starting_symbol

    def word_validate(self, palavra_teste):
        resultado, pos, erro = self._validate(self.starting_symbol, palavra_teste, 0)
        if resultado and pos == len(palavra_teste):
            return True, None
        else:
            return False, erro or f"Erro inesperado na posição {pos}"

    def _validate(self, symbol, word, pos):
        
        if pos >= len(word):
            if '&' in [p[0] for p in self.grammar.get(symbol, [])]:
                return True, pos, None
            else:
                return False, pos, "Palavra incompleta"

        for production in self.grammar.get(symbol, []):
            new_pos = pos
            matched = True
            error_message = None

            for char in production:
                if char in self.lexer.non_terminals:
                    resultado, new_pos, error_message = self._validate(char, word, new_pos)
                    if not resultado:
                        matched = False
                        break
                else:
                    if new_pos < len(word) and word[new_pos] == char:
                        new_pos += 1
                    else:
                        matched = False
                        break

            if matched:
                return True, new_pos, None

        return False, pos, f"Erro ao validar símbolo {symbol} na posição {pos}"

if __name__ == '__main__':
    main()
