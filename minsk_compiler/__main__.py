from minsk_compiler.evaluator import Evaluator
from minsk_compiler.syntax_token import SyntaxToken
from minsk_compiler.syntax_node import SyntaxNode
from minsk_compiler.parser import Parser
from colored import fg, attr


def pretty_print(node: SyntaxNode, indent: str = "", is_last: bool = True):
    print(fg(240), end="")
    print(indent, end="")
    if is_last:
        print("\\..", end="")
    else:
        print("+..", end="")
    print(attr(0), end="")
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
    syntax_tree = parser.parse()
    pretty_print(syntax_tree.root)
    if len(syntax_tree.diagnostics) > 0:
        print(fg(124), end="")
        for diagnostic in syntax_tree.diagnostics:
            print(diagnostic)
        print(attr(0), end="")
    else:
        e = Evaluator(syntax_tree.root)
        result = e.evaluate()
        print(result)
