from minsk_compiler.syntax_kind import SyntaxKind
from minsk_compiler.syntax_token import SyntaxToken


class Lexer:
    _text: str

    def __init__(self, text: str):
        self._text = text
        self._position = 0

    def _current(self) -> str:
        if self._position >= len(self._text):
            return '\0'
        else:
            return self._text[self._position]

    def _next(self):
        self._position += 1

    def next_token(self):
        if self._position >= len(self._text):
            return SyntaxToken(SyntaxKind.END_OF_FILE_TOKEN, self._position, "")
        if self._current().isdigit():
            start = self._position
            while self._current().isdigit():
                self._next()

            text = self._text[start:self._position]
            value = int(text)
            return SyntaxToken(SyntaxKind.NUMBER_TOKEN, start, text, value)
        elif self._current().isspace():
            start = self._position
            while self._current().isspace():
                self._next()

            text = self._text[start:self._position]
            return SyntaxToken(SyntaxKind.WHITESPACE_TOKEN, start, text)
        elif self._current() == "+":
            tok = SyntaxToken(SyntaxKind.PLUS_TOKEN, self._position, "+")
            self._position += 1
            return tok
        elif self._current() == "-":
            tok = SyntaxToken(SyntaxKind.MINUS_TOKEN, self._position, "-")
            self._position += 1
            return tok
        elif self._current() == "/":
            tok = SyntaxToken(SyntaxKind.SLASH_TOKEN, self._position, "/")
            self._position += 1
            return tok
        elif self._current() == "*":
            tok = SyntaxToken(SyntaxKind.STAR_TOKEN, self._position, "*")
            self._position += 1
            return tok
        elif self._current() == "(":
            tok = SyntaxToken(
                SyntaxKind.OPEN_PARENTHESIS_TOKEN, self._position, "(")
            self._position += 1
            return tok
        elif self._current() == ")":
            tok = SyntaxToken(
                SyntaxKind.CLOSE_PARENTHESIS_TOKEN, self._position, ")")
            self._position += 1
            return tok
        else:
            tok = SyntaxToken(SyntaxKind.BAD_TOKEN,
                              self._position, self._text[self._position])
            self._position += 1
            return tok
