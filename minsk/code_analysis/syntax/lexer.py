from typing import Any

from minsk.code_analysis.diagnostic_bag import DiagnosticBag
from minsk.code_analysis.syntax import syntax_facts
from minsk.code_analysis.syntax.syntax_kind import SyntaxKind
from minsk.code_analysis.syntax.syntax_token import SyntaxToken
from minsk.code_analysis.text.text_span import TextSpan


class Lexer:
    _text: str
    _start: int
    _position: int
    _kind: SyntaxKind
    _value: Any
    diagnostics: DiagnosticBag

    def __init__(self, text: str):
        self._text = text
        self._start = 0
        self._position = 0
        self._kind = SyntaxKind.BAD_TOKEN
        self._value = None
        self.diagnostics = DiagnosticBag()

    def _peek(self, offset: int) -> str:
        index = self._position + offset
        if index >= len(self._text):
            return "\0"
        else:
            return self._text[index]

    def _current(self) -> str:
        return self._peek(0)

    def _lookahead(self) -> str:
        return self._peek(1)

    def _next(self):
        self._position += 1

    def lex(self):
        self._start = self._position
        self._kind = SyntaxKind.BAD_TOKEN
        self._value = None
        if self._current().isdigit():
            self._read_number()
        elif self._current().isspace():
            self._read_whitespace()
        elif self._current().isalpha():
            self._read_identifier_or_keyword()
        elif self._current() == "&" and self._lookahead() == "&":
            self._kind = SyntaxKind.AMPERSAND_AMPERSAND_TOKEN
            self._position += 2
        elif self._current() == "|" and self._lookahead() == "|":
            self._kind = SyntaxKind.PIPE_PIPE_TOKEN
            self._position += 2
        elif self._current() == "=" and self._lookahead() == "=":
            self._kind = SyntaxKind.EQUALS_EQUALS_TOKEN
            self._position += 2
        elif self._current() == "!" and self._lookahead() == "=":
            self._kind = SyntaxKind.BANG_EQUALS_TOKEN
            self._position += 2
        elif self._current() == "\0":
            self._kind = SyntaxKind.END_OF_FILE_TOKEN
            self._position += 1
        elif self._current() == "+":
            self._kind = SyntaxKind.PLUS_TOKEN
            self._position += 1
        elif self._current() == "-":
            self._kind = SyntaxKind.MINUS_TOKEN
            self._position += 1
        elif self._current() == "/":
            self._kind = SyntaxKind.SLASH_TOKEN
            self._position += 1
        elif self._current() == "*":
            self._kind = SyntaxKind.STAR_TOKEN
            self._position += 1
        elif self._current() == "(":
            self._kind = SyntaxKind.OPEN_PARENTHESIS_TOKEN
            self._position += 1
        elif self._current() == ")":
            self._kind = SyntaxKind.CLOSE_PARENTHESIS_TOKEN
            self._position += 1
        elif self._current() == "!":
            self._kind = SyntaxKind.BANG_TOKEN
            self._position += 1
        elif self._current() == "=":
            self._kind = SyntaxKind.EQUALS_TOKEN
            self._position += 1
        else:
            self.diagnostics.report_bad_character(
                TextSpan(self._position, 1), self._current()
            )
            self._position += 1
        text = syntax_facts.text_for(self._kind)
        if text is None:
            text = self._text[self._start:self._position]
        return SyntaxToken(self._kind, self._start, text, self._value)

    def _read_identifier_or_keyword(self):
        while self._current().isalpha():
            self._next()
        text = self._text[self._start:self._position]
        self._kind = syntax_facts.keyword_kind(text)

    def _read_whitespace(self):
        while self._current().isspace():
            self._next()
        self._kind = SyntaxKind.WHITESPACE_TOKEN

    def _read_number(self):
        while self._current().isdigit():
            self._next()

        self._kind = SyntaxKind.NUMBER_TOKEN
        text = self._text[self._start:self._position]
        self._value = int(text)
