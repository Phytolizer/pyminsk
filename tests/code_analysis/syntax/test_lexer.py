import itertools
from typing import Iterable

import pytest

from minsk.code_analysis.syntax import syntax_facts
from minsk.code_analysis.syntax.syntax_kind import SyntaxKind
from minsk.code_analysis.syntax.syntax_tree import SyntaxTree


def get_tokens() -> Iterable[tuple[SyntaxKind, str]]:
    fixed_tokens = filter(lambda t: t[1] is not None, map(lambda k: (k, syntax_facts.text_for(k)), SyntaxKind))
    dynamic_tokens = (
        (SyntaxKind.IDENTIFIER_TOKEN, "a"),
        (SyntaxKind.IDENTIFIER_TOKEN, "abc"),
        (SyntaxKind.NUMBER_TOKEN, "1"),
        (SyntaxKind.NUMBER_TOKEN, "123"),
    )
    return itertools.chain(fixed_tokens, dynamic_tokens)


def get_separators() -> Iterable[tuple[SyntaxKind, str]]:
    return (
        (SyntaxKind.WHITESPACE_TOKEN, " "),
        (SyntaxKind.WHITESPACE_TOKEN, "  "),
        (SyntaxKind.WHITESPACE_TOKEN, "\r"),
        (SyntaxKind.WHITESPACE_TOKEN, "\n"),
        (SyntaxKind.WHITESPACE_TOKEN, "\r\n"),
    )


def get_token_pairs() -> Iterable[tuple[SyntaxKind, str, SyntaxKind, str]]:
    for t1_kind, t1_text in get_tokens():
        for t2_kind, t2_text in get_tokens():
            if not requires_separator(t1_kind, t2_kind):
                yield t1_kind, t1_text, t2_kind, t2_text


def get_token_pairs_with_separators() -> Iterable[tuple[SyntaxKind, str, SyntaxKind, str, SyntaxKind, str]]:
    for t1_kind, t1_text in get_tokens():
        for t2_kind, t2_text in get_tokens():
            if requires_separator(t1_kind, t2_kind):
                for s_kind, s_text in get_separators():
                    yield t1_kind, t1_text, s_kind, s_text, t2_kind, t2_text


def requires_separator(t1_kind: SyntaxKind, t2_kind: SyntaxKind) -> bool:
    t1_is_keyword = "KEYWORD" in t1_kind.name
    t2_is_keyword = "KEYWORD" in t2_kind.name
    if (t1_is_keyword or t1_kind == SyntaxKind.IDENTIFIER_TOKEN) and (
            t2_is_keyword or t2_kind == SyntaxKind.IDENTIFIER_TOKEN):
        return True
    if t1_kind == SyntaxKind.NUMBER_TOKEN and t2_kind == SyntaxKind.NUMBER_TOKEN:
        return True
    if t1_kind in (SyntaxKind.BANG_TOKEN, SyntaxKind.EQUALS_TOKEN) and t2_kind in (
            SyntaxKind.EQUALS_TOKEN, SyntaxKind.EQUALS_EQUALS_TOKEN):
        return True
    return False


class TestLexer:
    def test_tests_all_tokens(self):
        token_kinds = set(filter(lambda k: k.name.endswith("TOKEN") or k.name.endswith("KEYWORD"), SyntaxKind)) - {
            SyntaxKind.BAD_TOKEN, SyntaxKind.END_OF_FILE_TOKEN}
        tested_token_kinds = set(map(lambda t: t[0], itertools.chain(get_tokens(), get_separators())))
        assert token_kinds - tested_token_kinds == set()

    @pytest.mark.parametrize("kind,text", itertools.chain(get_tokens(), get_separators()))
    def test_lexes_token(self, kind: SyntaxKind, text: str):
        tokens = tuple(SyntaxTree.parse_tokens(text))
        assert len(tokens) == 1
        token = tokens[0]
        assert token.kind() == kind
        assert token.text == text

    @pytest.mark.parametrize("t1_kind,t1_text,t2_kind,t2_text", get_token_pairs())
    def test_lexes_token_pairs(self, t1_kind: SyntaxKind, t1_text: str, t2_kind: SyntaxKind, t2_text: str):
        text = f"{t1_text}{t2_text}"
        tokens = tuple(SyntaxTree.parse_tokens(text))
        assert len(tokens) == 2
        t1 = tokens[0]
        assert t1.kind() == t1_kind
        assert t1.text == t1_text
        t2 = tokens[1]
        assert t2.kind() == t2_kind
        assert t2.text == t2_text

    @pytest.mark.parametrize("t1_kind,t1_text,s_kind,s_text,t2_kind,t2_text", get_token_pairs_with_separators())
    def test_lexes_token_pairs_with_separator(self, t1_kind: SyntaxKind, t1_text: str, s_kind: SyntaxKind, s_text: str,
                                              t2_kind: SyntaxKind, t2_text: str):
        text = f"{t1_text}{s_text}{t2_text}"
        tokens = tuple(SyntaxTree.parse_tokens(text))
        assert len(tokens) == 3
        t1 = tokens[0]
        assert t1.kind() == t1_kind
        assert t1.text == t1_text
        s = tokens[1]
        assert s.kind() == s_kind
        assert s.text == s_text
        t2 = tokens[2]
        assert t2.kind() == t2_kind
        assert t2.text == t2_text
