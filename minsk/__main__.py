import sys
from typing import Any

from rich.console import Console

from minsk.code_analysis.compilation import Compilation
from minsk.code_analysis.syntax.syntax_tree import SyntaxTree
from minsk.code_analysis.variable_symbol import VariableSymbol

show_tree = False
console = Console()
variables: dict[VariableSymbol, Any] = dict()

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
    result = compilation.evaluate(variables)
    diagnostics = result.diagnostics

    if show_tree:
        syntax_tree.write_to(console, True)
    if len(diagnostics) > 0:
        text = syntax_tree.text
        for diagnostic in diagnostics:
            line_index = text.get_line_index(diagnostic.span.start)
            line_number = line_index + 1
            character = diagnostic.span.start - text.lines[line_index].start + 1
            prefix = line[0:diagnostic.span.start]
            error = line[diagnostic.span.start:diagnostic.span.end()]
            suffix = line[diagnostic.span.end():]

            console.print()
            console.print(f"({line_number}, {character}):", highlight=False)
            console.print(f"    {prefix}", end="", highlight=False)
            console.print(error, style="red", end="", highlight=False)
            console.print(suffix, highlight=False)

            console.print(str(diagnostic), style="red", highlight=False)
            console.print()
    else:
        console.print(result.value, style="magenta", highlight=False)
