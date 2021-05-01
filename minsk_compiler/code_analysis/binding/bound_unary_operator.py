from typing import Type, Optional, Tuple

from minsk_compiler.code_analysis.binding.bound_unary_operator_kind import BoundUnaryOperatorKind
from minsk_compiler.code_analysis.syntax.syntax_kind import SyntaxKind


class BoundUnaryOperator:
    syntax_kind: SyntaxKind
    kind: BoundUnaryOperatorKind
    operand_type: Type
    type: Type

    def __init__(self, syntax_kind: SyntaxKind, kind: BoundUnaryOperatorKind, operand_type: Type,
                 result_type: Optional[Type] = None):
        self.syntax_kind = syntax_kind
        self.kind = kind
        self.operand_type = operand_type
        if result_type is None:
            result_type = operand_type
        self.type = result_type

    @staticmethod
    def _operators() -> Tuple["BoundUnaryOperator", ...]:
        return (
            BoundUnaryOperator(SyntaxKind.BANG_TOKEN, BoundUnaryOperatorKind.LOGICAL_NEGATION, bool),
            BoundUnaryOperator(SyntaxKind.PLUS_TOKEN, BoundUnaryOperatorKind.IDENTITY, int),
            BoundUnaryOperator(SyntaxKind.MINUS_TOKEN, BoundUnaryOperatorKind.NEGATION, int),
        )

    @staticmethod
    def bind(syntax_kind: SyntaxKind, operand_type: Type) -> Optional["BoundUnaryOperator"]:
        for op in BoundUnaryOperator._operators():
            if op.syntax_kind == syntax_kind and op.operand_type == operand_type:
                return op

        return None
