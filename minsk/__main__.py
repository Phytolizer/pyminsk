from rich.console import Console
from rich.style import Style

from minsk.code_analysis.binding.binder import Binder
from minsk.code_analysis.evaluator import Evaluator
from minsk.code_analysis.syntax.syntax_node import SyntaxNode
from minsk.code_analysis.syntax.syntax_token import SyntaxToken
from minsk.code_analysis.syntax.syntax_tree import SyntaxTree

show_tree = False
console = Console()
pretty_indent_style = Style(color="grey35")


def pretty_print(node: SyntaxNode, indent: str = "", is_last: bool = True):
    console.print(indent, end="", style=pretty_indent_style)
    if is_last:
        console.print("\\..", end="", style=pretty_indent_style)
    else:
        console.print("+..", end="", style=pretty_indent_style)
    console.print(node.kind(), end="")
    if isinstance(node, SyntaxToken) and node.value is not None:
        console.print(f" {node.value}", end="", style="bright_magenta")

    console.print()

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

    if line == "#showTree":
        show_tree = not show_tree
        if show_tree:
            console.print("Showing parse trees", style="blue")
        else:
            console.print("Hiding parse trees", style="blue")
        continue
    elif line == "#cls":
        console.clear()
        continue

    syntax_tree = SyntaxTree.parse(line)
    binder = Binder()
    bound_expression = binder.bind_expression(syntax_tree.root)
    diagnostics = syntax_tree.diagnostics + tuple(binder.diagnostics)

    if show_tree:
        pretty_print(syntax_tree.root)
    if len(diagnostics) > 0:
        for diagnostic in diagnostics:
            console.print(diagnostic, style="red")
    else:
        e = Evaluator(bound_expression)
        result = e.evaluate()
        print(result)
