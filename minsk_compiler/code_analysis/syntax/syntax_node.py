from abc import ABC, abstractmethod
from typing import Iterable

from minsk_compiler.code_analysis.syntax.syntax_kind import SyntaxKind


class SyntaxNode(ABC):
    @abstractmethod
    def kind(self) -> SyntaxKind:
        pass

    @abstractmethod
    def children(self) -> Iterable["SyntaxNode"]:
        pass
