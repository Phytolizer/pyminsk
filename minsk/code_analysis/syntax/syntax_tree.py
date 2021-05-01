from typing import Iterable

from minsk.code_analysis.diagnostic_bag import DiagnosticBag
from minsk.code_analysis.syntax.expression_syntax import ExpressionSyntax
from minsk.code_analysis.syntax.lexer import Lexer
from minsk.code_analysis.syntax.parser import Parser
from minsk.code_analysis.syntax.syntax_kind import SyntaxKind
from minsk.code_analysis.syntax.syntax_token import SyntaxToken


class SyntaxTree:
    diagnostics: DiagnosticBag
    root: ExpressionSyntax
    end_of_file_token: SyntaxToken

    def __init__(
            self,
            diagnostics: DiagnosticBag,
            root: ExpressionSyntax,
            end_of_file_token: SyntaxToken,
    ):
        self.diagnostics = diagnostics
        self.root = root
        self.end_of_file_token = end_of_file_token

    @staticmethod
    def parse(text: str) -> "SyntaxTree":
        return SyntaxTree(*Parser(text).parse())

    @staticmethod
    def parse_tokens(text: str) -> Iterable[SyntaxToken]:
        lexer = Lexer(text)
        while True:
            token = lexer.lex()
            if token.kind() == SyntaxKind.END_OF_FILE_TOKEN:
                break

            yield token
