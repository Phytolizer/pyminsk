from typing import Iterable, Iterator

import pytest

from minsk.code_analysis.syntax import syntax_facts
from minsk.code_analysis.syntax.syntax_kind import SyntaxKind
from minsk.code_analysis.syntax.syntax_node import SyntaxNode
from minsk.code_analysis.syntax.syntax_token import SyntaxToken
from minsk.code_analysis.syntax.syntax_tree import SyntaxTree


class AssertingEnumerator:
    _enumerator: Iterator[SyntaxNode]
    _has_errors: bool

    def __init__(self, node: SyntaxNode):
        self._enumerator = iter(self._flatten(node))
        self._has_errors = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self._has_errors:
            assert next(self._enumerator, None) is None

    @staticmethod
    def _flatten(node: SyntaxNode) -> Iterable[SyntaxNode]:
        stack: list[SyntaxNode] = [node]
        while len(stack) > 0:
            n = stack.pop()
            yield n
            for child in reversed(n.children()):
                stack.append(child)

    def assert_token(self, kind: SyntaxKind, text: str):
        tok = next(self._enumerator, None)
        try:
            assert tok is not None
            assert kind == tok.kind()
            assert isinstance(tok, SyntaxToken)
            assert text == tok.text
        except AssertionError:
            self._has_errors = True
            raise

    def assert_node(self, kind: SyntaxKind):
        node = next(self._enumerator, None)
        try:
            assert node is not None
            assert node.kind() == kind
            assert not isinstance(node, SyntaxToken)
        except AssertionError:
            self._has_errors = True
            raise


def get_binary_operator_pairs_data() -> Iterable[tuple[SyntaxKind, SyntaxKind]]:
    for op1 in syntax_facts.binary_operators():
        for op2 in syntax_facts.binary_operators():
            yield op1, op2


@pytest.mark.parametrize("op1,op2", get_binary_operator_pairs_data())
def test_binary_expression_honors_precedence(op1: SyntaxKind, op2: SyntaxKind):
    op1_precedence = syntax_facts.get_binary_operator_precedence(op1)
    op2_precedence = syntax_facts.get_binary_operator_precedence(op2)
    op1_text = syntax_facts.text_for(op1)
    op2_text = syntax_facts.text_for(op2)
    text = f"a {op1_text} b {op2_text} c"
    expression = SyntaxTree.parse(text).root
    if op1_precedence >= op2_precedence:
        with AssertingEnumerator(expression) as e:
            e.assert_node(SyntaxKind.BINARY_EXPRESSION)
            e.assert_node(SyntaxKind.BINARY_EXPRESSION)
            e.assert_node(SyntaxKind.NAME_EXPRESSION)
            e.assert_token(SyntaxKind.IDENTIFIER_TOKEN, "a")
            e.assert_token(op1, op1_text)
            e.assert_node(SyntaxKind.NAME_EXPRESSION)
            e.assert_token(SyntaxKind.IDENTIFIER_TOKEN, "b")
            e.assert_token(op2, op2_text)
            e.assert_node(SyntaxKind.NAME_EXPRESSION)
            e.assert_token(SyntaxKind.IDENTIFIER_TOKEN, "c")
    else:
        with AssertingEnumerator(expression) as e:
            e.assert_node(SyntaxKind.BINARY_EXPRESSION)
            e.assert_node(SyntaxKind.NAME_EXPRESSION)
            e.assert_token(SyntaxKind.IDENTIFIER_TOKEN, "a")
            e.assert_token(op1, op1_text)
            e.assert_node(SyntaxKind.BINARY_EXPRESSION)
            e.assert_node(SyntaxKind.NAME_EXPRESSION)
            e.assert_token(SyntaxKind.IDENTIFIER_TOKEN, "b")
            e.assert_token(op2, op2_text)
            e.assert_node(SyntaxKind.NAME_EXPRESSION)
            e.assert_token(SyntaxKind.IDENTIFIER_TOKEN, "c")
