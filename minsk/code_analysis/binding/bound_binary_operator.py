from typing import Type, Optional, Tuple

from minsk.code_analysis.binding.bound_binary_operator_kind import BoundBinaryOperatorKind
from minsk.code_analysis.syntax.syntax_kind import SyntaxKind


class BoundBinaryOperator:
    syntax_kind: SyntaxKind
    kind: BoundBinaryOperatorKind
    left_type: Type
    right_type: Type
    type: Type

    def __init__(self, syntax_kind: SyntaxKind, kind: BoundBinaryOperatorKind, left_type: Type,
                 right_type: Optional[Type] = None, result_type: Optional[Type] = None):
        self.syntax_kind = syntax_kind
        self.kind = kind
        self.left_type = left_type
        if right_type is None:
            right_type = left_type
        self.right_type = right_type
        if result_type is None:
            result_type = left_type
        self.type = result_type

    @staticmethod
    def _operators() -> Tuple["BoundBinaryOperator", ...]:
        return (
            BoundBinaryOperator(SyntaxKind.PLUS_TOKEN, BoundBinaryOperatorKind.ADDITION, int),
            BoundBinaryOperator(SyntaxKind.MINUS_TOKEN, BoundBinaryOperatorKind.SUBTRACTION, int),
            BoundBinaryOperator(SyntaxKind.STAR_TOKEN, BoundBinaryOperatorKind.MULTIPLICATION, int),
            BoundBinaryOperator(SyntaxKind.SLASH_TOKEN, BoundBinaryOperatorKind.DIVISION, int),

            BoundBinaryOperator(SyntaxKind.EQUALS_EQUALS_TOKEN, BoundBinaryOperatorKind.EQUALITY, int, int, bool),
            BoundBinaryOperator(SyntaxKind.BANG_EQUALS_TOKEN, BoundBinaryOperatorKind.INEQUALITY, int, int, bool),

            BoundBinaryOperator(SyntaxKind.AMPERSAND_AMPERSAND_TOKEN, BoundBinaryOperatorKind.LOGICAL_AND, bool),
            BoundBinaryOperator(SyntaxKind.PIPE_PIPE_TOKEN, BoundBinaryOperatorKind.LOGICAL_OR, bool),
            BoundBinaryOperator(SyntaxKind.EQUALS_EQUALS_TOKEN, BoundBinaryOperatorKind.EQUALITY, bool, bool, bool),
            BoundBinaryOperator(SyntaxKind.BANG_EQUALS_TOKEN, BoundBinaryOperatorKind.INEQUALITY, bool, bool, bool),
        )

    @staticmethod
    def bind(syntax_kind: SyntaxKind, left_type: Type, right_type: Type) -> Optional["BoundBinaryOperator"]:
        for op in BoundBinaryOperator._operators():
            if op.syntax_kind == syntax_kind and op.left_type == left_type and op.right_type == right_type:
                return op

        return None
