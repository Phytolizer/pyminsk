from typing import Any, Sequence

from minsk.code_analysis.syntax.syntax_kind import SyntaxKind
from minsk.code_analysis.syntax.syntax_node import SyntaxNode
from minsk.code_analysis.text_span import TextSpan


class SyntaxToken(SyntaxNode):
    _span: TextSpan
    _kind: SyntaxKind
    position: int
    text: str

    def __init__(self, kind: SyntaxKind, position: int, text: str,
                 value: Any = None):
        self._span = TextSpan(position, len(text))
        self._kind = kind
        self.position = position
        self.text = text
        self.value = value

    def __str__(self) -> str:
        out = f"{self.kind} {self.text}"
        if self.value is not None:
            out += f" {self.value}"
        return out

    def kind(self) -> SyntaxKind:
        return self._kind

    def children(self) -> Sequence["SyntaxNode"]:
        return ()

    def span(self) -> TextSpan:
        return self._span
