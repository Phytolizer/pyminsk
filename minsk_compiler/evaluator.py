from minsk_compiler.syntax_kind import SyntaxKind
from minsk_compiler.expression_syntax import ExpressionSyntax


class Evaluator:
    _root: ExpressionSyntax

    def __init__(self, root: ExpressionSyntax):
        self._root = root

    def evaluate(self) -> int:
        return self._evaluate_expression(self._root)

    def _evaluate_expression(self, root: ExpressionSyntax) -> int:
        if root.kind() == SyntaxKind.LITERAL_EXPRESSION:
            return root.literal_token.value
        elif root.kind() == SyntaxKind.BINARY_EXPRESSION:
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
                raise Exception(
                    f"unexpected binary operator {root.operator_token.kind()}"
                )
        elif root.kind() == SyntaxKind.PARENTHESIZED_EXPRESSION:
            return self._evaluate_expression(root.expression)
        else:
            raise Exception(f"unexpected node {root.kind()}")
