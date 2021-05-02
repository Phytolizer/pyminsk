import pytest

from minsk.code_analysis.syntax.syntax_kind import SyntaxKind


class TestParser:
    @pytest.mark.parametrize("op1,op2", [])
    def test_binary_expression_honors_precedence(self, op1: SyntaxKind, op2: SyntaxKind):
        pass
