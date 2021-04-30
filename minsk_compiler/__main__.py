from minsk_compiler.syntax_token import SyntaxToken
from minsk_compiler.syntax_node import SyntaxNode
from minsk_compiler.parser import Parser


def pretty_print(node: SyntaxNode, indent: str = ""):
    print(indent, end="")
    print(node.kind(), end="")
    if isinstance(node, SyntaxToken) and node.value is not None:
        print(f" {node.value}", end="")

    print()
    indent += "    "
    for child in node.children():
        pretty_print(child, indent)


while True:
    try:
        line = input("> ")
    except EOFError:
        break

    parser = Parser(line)
    expression = parser.parse()
    pretty_print(expression)
