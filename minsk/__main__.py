from rich.console import Console
from rich.style import Style

from minsk.code_analysis.compilation import Compilation
from minsk.code_analysis.syntax.syntax_node import SyntaxNode
from minsk.code_analysis.syntax.syntax_token import SyntaxToken
from minsk.code_analysis.syntax.syntax_tree import SyntaxTree

show_tree = False
console = Console()
pretty_indent_style = Style(color="grey35")


def pretty_print(node: SyntaxNode, indent: str = "", is_last: bool = True):
    console.print(indent, end="", style=pretty_indent_style, highlight=False)
    if is_last:
        console.print("\\..", end="", style=pretty_indent_style, highlight=False)
    else:
        console.print("+..", end="", style=pretty_indent_style, highlight=False)
    console.print(node.kind(), end="", highlight=False)
    if isinstance(node, SyntaxToken):
        if node.value is None:
            console.print(f" '{node.text}'", end="", style="bright_green", highlight=False)
        else:
            console.print(f" {node.value}", end="", style="bright_magenta", highlight=False)

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
    compilation = Compilation(syntax_tree)
    result = compilation.evaluate()
    diagnostics = result.diagnostics

    if show_tree:
        pretty_print(syntax_tree.root)
    if len(diagnostics) > 0:
        for diagnostic in diagnostics:
            prefix = line[0:diagnostic.span.start]
            error = line[diagnostic.span.start:diagnostic.span.end()]
            suffix = line[diagnostic.span.end():]

            console.print()
            console.print(f"    {prefix}", end="", highlight=False)
            console.print(error, style="red", end="", highlight=False)
            console.print(suffix, highlight=False)

            console.print(str(diagnostic), style="red", highlight=False)
            console.print()
    else:
        console.print(result.value, style="magenta", highlight=False)
