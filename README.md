# Trabalho da disciplina de Compiladores
readme.txt contendo todas as instruções para a compilação e
execução do código, indicando dependências, plataforma escolhida e passos detalhados.

Este trabalho consiste na criação de uma Gramática Regular e um Interpretador para ela.
No input.txt temos a Gramática utilizada, deve ser uma GLD (linear a direita), a ser lida pelo lexer implementado em lexer.py.
O validator.py recebe a palavra pelo terminal e usa o lexer.py para validar a palavra conforme a gramática de input.txt.
Está sendo implementadoo método do analisador recursivo com retrocesso.

# Compilando e executando
**Linha de comando:** python validator.py

Irá pedir uma palavra para ser testada, essa palavra deve ser digitada no terminal (e pressionar a tecla enter em seguida).
Se for aceita a árvore de derivação será mostrada, se não aceita mostrará mensagem de erro.