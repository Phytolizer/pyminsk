from typing import Any

from rich.console import Console

from minsk.code_analysis.compilation import Compilation
from minsk.code_analysis.syntax.syntax_tree import SyntaxTree
from minsk.code_analysis.text.text_span import TextSpan
from minsk.code_analysis.variable_symbol import VariableSymbol

show_tree = False
console = Console()
variables: dict[VariableSymbol, Any] = dict()
text_builder = ""

while True:
    if len(text_builder) == 0:
        console.print("> ", style="yellow", end="")
    else:
        console.print("| ", style="yellow", end="")
    try:
        line = input()
    except EOFError:
        break

    is_blank = len(line.strip()) == 0

    if len(text_builder) == 0:
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

    text_builder += line + "\n"

    syntax_tree = SyntaxTree.parse(text_builder)

    if not is_blank and len(syntax_tree.diagnostics) > 0:
        continue

    compilation = Compilation(syntax_tree)
    result = compilation.evaluate(variables)
    diagnostics = result.diagnostics

    if show_tree:
        syntax_tree.write_to(console, True)
    text_builder = ""
    if len(diagnostics) > 0:
        text = syntax_tree.text
        for diagnostic in diagnostics:
            line_index = text.get_line_index(diagnostic.span.start)
            line_number = line_index + 1
            source_line = text.lines[line_index]
            character = diagnostic.span.start - source_line.start + 1

            prefix_span = TextSpan.from_bounds(source_line.start, diagnostic.span.start)
            suffix_span = TextSpan.from_bounds(diagnostic.span.end(), source_line.end)

            print(repr(source_line))
            print(repr(prefix_span))

            prefix = text[prefix_span]
            error = text[diagnostic.span.start:diagnostic.span.end()]
            suffix = text[suffix_span]

            console.print()
            console.print(f"({line_number}, {character}):", highlight=False)
            console.print(f"    {prefix}", end="", highlight=False)
            console.print(error, style="red", end="", highlight=False)
            console.print(suffix, highlight=False)

            console.print(str(diagnostic), style="red", highlight=False)
            console.print()
    else:
        console.print(result.value, style="magenta", highlight=False)
