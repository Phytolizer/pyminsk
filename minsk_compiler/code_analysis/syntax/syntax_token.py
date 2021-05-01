from typing import Any, Iterable

from minsk_compiler.code_analysis.syntax.syntax_kind import SyntaxKind
from minsk_compiler.code_analysis.syntax.syntax_node import SyntaxNode


class SyntaxToken(SyntaxNode):
    _kind: SyntaxKind
    position: int
    text: str

    def __init__(self, kind: SyntaxKind, position: int, text: str,
                 value: Any = None):
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

    def children(self) -> Iterable["SyntaxNode"]:
        return ()
