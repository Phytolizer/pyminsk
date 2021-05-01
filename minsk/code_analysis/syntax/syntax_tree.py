from minsk.code_analysis.diagnostic_bag import DiagnosticBag
from minsk.code_analysis.syntax.expression_syntax import ExpressionSyntax
from minsk.code_analysis.syntax.parser import Parser
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
