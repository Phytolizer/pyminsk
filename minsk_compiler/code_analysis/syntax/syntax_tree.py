from typing import List, Tuple

from minsk_compiler.code_analysis.syntax.parser import Parser
from minsk_compiler.code_analysis.syntax.expression_syntax import ExpressionSyntax
from minsk_compiler.code_analysis.syntax.syntax_token import SyntaxToken


class SyntaxTree:
    diagnostics: Tuple[str, ...]
    root: ExpressionSyntax
    end_of_file_token: SyntaxToken

    def __init__(
            self,
            diagnostics: List[str],
            root: ExpressionSyntax,
            end_of_file_token: SyntaxToken,
    ):
        self.diagnostics = tuple(diagnostics)
        self.root = root
        self.end_of_file_token = end_of_file_token

    @staticmethod
    def parse(text: str) -> "SyntaxTree":
        return SyntaxTree(*Parser(text).parse())
