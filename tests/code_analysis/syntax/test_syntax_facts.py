from typing import Iterable

import pytest

from minsk.code_analysis.syntax import syntax_facts
from minsk.code_analysis.syntax.syntax_kind import SyntaxKind
from minsk.code_analysis.syntax.syntax_tree import SyntaxTree


def get_syntax_kind_data() -> Iterable[tuple[SyntaxKind]]:
    for kind in SyntaxKind:
        yield kind,


@pytest.mark.parametrize("kind", get_syntax_kind_data())
def test_get_text_round_trips(kind: SyntaxKind):
    text = syntax_facts.text_for(kind)
    if text is None:
        return

    tokens = tuple(SyntaxTree.parse_tokens(text))
    assert len(tokens) == 1
    token = tokens[0]
    assert token.kind() == kind
    assert token.text == text
