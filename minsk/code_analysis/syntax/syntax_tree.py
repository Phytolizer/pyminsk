from typing import Iterable, TextIO, Union, Optional, cast

from rich.console import Console

from minsk.code_analysis.diagnostic_bag import DiagnosticBag
from minsk.code_analysis.syntax.expression_syntax import ExpressionSyntax
from minsk.code_analysis.syntax.lexer import Lexer
from minsk.code_analysis.syntax.parser import Parser
from minsk.code_analysis.syntax.syntax_kind import SyntaxKind
from minsk.code_analysis.syntax.syntax_node import SyntaxNode
from minsk.code_analysis.syntax.syntax_token import SyntaxToken
from minsk.code_analysis.text.source_text import SourceText


class SyntaxTree:
    text: SourceText
    diagnostics: DiagnosticBag
    root: ExpressionSyntax
    end_of_file_token: SyntaxToken

    def __init__(
            self,
            source_text: SourceText,
            diagnostics: DiagnosticBag,
            root: ExpressionSyntax,
            end_of_file_token: SyntaxToken,
    ):
        self.text = source_text
        self.diagnostics = diagnostics
        self.root = root
        self.end_of_file_token = end_of_file_token

    @staticmethod
    def parse(text: Union[str, SourceText]) -> "SyntaxTree":
        if isinstance(text, str):
            text = SourceText.create_from(text)
        return SyntaxTree(*Parser(text).parse())

    @staticmethod
    def parse_tokens(text: Union[str, SourceText]) -> Iterable[SyntaxToken]:
        if isinstance(text, str):
            text = SourceText.create_from(text)
        lexer = Lexer(text)
        while True:
            token = lexer.lex()
            if token.kind() == SyntaxKind.END_OF_FILE_TOKEN:
                break

            yield token

    def write_to(self, writer: Union[TextIO, Console], is_console: bool):
        _pretty_print(writer, is_console, self.root)


def _pretty_write(writer: Union[TextIO, Console], color: Optional[str], text: str, should_color: bool):
    if should_color:
        writer = cast(Console, writer)
        writer.print(text, end="", style=color, highlight=False)
    else:
        writer = cast(TextIO, writer)
        writer.write(text)


def _pretty_print(writer: Union[TextIO, Console], with_colors: bool, node: SyntaxNode, indent: str = "",
                  is_last: bool = True):
    _pretty_write(writer, "grey35", indent, with_colors)
    if is_last:
        _pretty_write(writer, "grey35", "\\..", with_colors)
    else:
        _pretty_write(writer, "grey35", "+..", with_colors)
    _pretty_write(writer, None, str(node.kind()), with_colors)
    if isinstance(node, SyntaxToken):
        if node.value is None:
            _pretty_write(writer, "green", f" '{node.text}'", with_colors)
        else:
            _pretty_write(writer, "magenta", f" {node.value}", with_colors)

    _pretty_write(writer, None, "\n", with_colors)

    if is_last:
        indent += "   "
    else:
        indent += "|  "

    try:
        last = node.children()[-1]
    except IndexError:
        return
    for child in node.children():
        _pretty_print(writer, with_colors, child, indent, child == last)
