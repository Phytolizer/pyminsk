from typing import cast

from minsk_compiler.code_analysis.syntax.binary_expression_syntax import BinaryExpressionSyntax
from minsk_compiler.code_analysis.syntax.expression_syntax import ExpressionSyntax
from minsk_compiler.code_analysis.syntax.literal_expression_syntax import LiteralExpressionSyntax
from minsk_compiler.code_analysis.syntax.parenthesized_expression_syntax import ParenthesizedExpressionSyntax
from minsk_compiler.code_analysis.syntax.syntax_kind import SyntaxKind
from minsk_compiler.code_analysis.syntax.unary_expression_syntax import UnaryExpressionSyntax


class Evaluator:
    _root: ExpressionSyntax

    def __init__(self, root: ExpressionSyntax):
        self._root = root

    def evaluate(self) -> int:
        return self._evaluate_expression(self._root)

    def _evaluate_expression(self, root: ExpressionSyntax) -> int:
        if root.kind() == SyntaxKind.LITERAL_EXPRESSION:
            root = cast(LiteralExpressionSyntax, root)
            return root.literal_token.value
        elif root.kind() == SyntaxKind.UNARY_EXPRESSION:
            root = cast(UnaryExpressionSyntax, root)
            operand = self._evaluate_expression(root.operand)

            if root.operator_token.kind() == SyntaxKind.PLUS_TOKEN:
                return operand
            elif root.operator_token.kind() == SyntaxKind.MINUS_TOKEN:
                return -operand
            else:
                raise Exception(f"unexpected unary operator {root.operator_token.kind()}")

        elif root.kind() == SyntaxKind.BINARY_EXPRESSION:
            root = cast(BinaryExpressionSyntax, root)
            left = self._evaluate_expression(root.left)
            right = self._evaluate_expression(root.right)

            if root.operator_token.kind() == SyntaxKind.PLUS_TOKEN:
                return left + right
            elif root.operator_token.kind() == SyntaxKind.MINUS_TOKEN:
                return left - right
            elif root.operator_token.kind() == SyntaxKind.STAR_TOKEN:
                return left * right
            elif root.operator_token.kind() == SyntaxKind.SLASH_TOKEN:
                return left // right
            else:
                raise Exception(f"unexpected binary operator {root.operator_token.kind()}")

        elif root.kind() == SyntaxKind.PARENTHESIZED_EXPRESSION:
            root = cast(ParenthesizedExpressionSyntax, root)
            return self._evaluate_expression(root.expression)
        else:
            raise Exception(f"unexpected node {root.kind()}")
