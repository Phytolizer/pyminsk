from minsk_compiler.syntax_kind import SyntaxKind
from minsk_compiler.lexer import Lexer

while True:
    try:
        line = input("> ")
    except EOFError:
        break

    lexer = Lexer(line)
    while True:
        tok = lexer.next_token()
        if tok.kind == SyntaxKind.END_OF_FILE_TOKEN:
            break
        print(str(tok))
