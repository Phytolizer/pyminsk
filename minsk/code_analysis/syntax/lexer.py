from minsk.code_analysis.diagnostic_bag import DiagnosticBag
from minsk.code_analysis.syntax import syntax_facts
from minsk.code_analysis.syntax.syntax_kind import SyntaxKind
from minsk.code_analysis.syntax.syntax_token import SyntaxToken
from minsk.code_analysis.text_span import TextSpan


class Lexer:
    _text: str
    diagnostics: DiagnosticBag

    def __init__(self, text: str):
        self._text = text
        self._position = 0
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
        elif self._current().isalpha():
            start = self._position
            while self._current().isalpha():
                self._next()

            text = self._text[start:self._position]
            kind = syntax_facts.keyword_kind(text)
            return SyntaxToken(kind, start, text)
        elif self._current() == "&" and self._lookahead() == "&":
            tok = SyntaxToken(SyntaxKind.AMPERSAND_AMPERSAND_TOKEN, self._position, "&&")
            self._position += 2
            return tok
        elif self._current() == "|" and self._lookahead() == "|":
            tok = SyntaxToken(SyntaxKind.PIPE_PIPE_TOKEN, self._position, "||")
            self._position += 2
            return tok
        elif self._current() == "=" and self._lookahead() == "=":
            tok = SyntaxToken(SyntaxKind.EQUALS_EQUALS_TOKEN, self._position, "==")
            self._position += 2
            return tok
        elif self._current() == "!" and self._lookahead() == "=":
            tok = SyntaxToken(SyntaxKind.BANG_EQUALS_TOKEN, self._position, "!=")
            self._position += 2
            return tok
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
            tok = SyntaxToken(SyntaxKind.OPEN_PARENTHESIS_TOKEN, self._position, "(")
            self._position += 1
            return tok
        elif self._current() == ")":
            tok = SyntaxToken(SyntaxKind.CLOSE_PARENTHESIS_TOKEN, self._position, ")")
            self._position += 1
            return tok
        elif self._current() == "!":
            tok = SyntaxToken(SyntaxKind.BANG_TOKEN, self._position, "!")
            self._position += 1
            return tok
        elif self._current() == "=":
            tok = SyntaxToken(SyntaxKind.EQUALS_TOKEN, self._position, "=")
            self._position += 1
            return tok
        else:
            self.diagnostics.report_bad_character(
                TextSpan(self._position, 1), self._current()
            )
            tok = SyntaxToken(
                SyntaxKind.BAD_TOKEN, self._position, self._text[self._position]
            )
            self._position += 1
            return tok
