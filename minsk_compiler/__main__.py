from minsk_compiler.syntax_token import SyntaxToken
from minsk_compiler.syntax_node import SyntaxNode
from minsk_compiler.parser import Parser


def pretty_print(node: SyntaxNode, indent: str = "", is_last: bool = True):
    print(indent, end="")
    if is_last:
        print("\\..", end="")
    else:
        print("+..", end="")
    print(node.kind(), end="")
    if isinstance(node, SyntaxToken) and node.value is not None:
        print(f" {node.value}", end="")

    print()
    if is_last:
        indent += "   "
    else:
        indent += "|  "

    try:
        last = node.children()[-1]
    except IndexError:
        return
    for child in node.children():
        pretty_print(child, indent, child == last)


while True:
    try:
        line = input("> ")
    except EOFError:
        break

    parser = Parser(line)
    expression = parser.parse()
    pretty_print(expression)
