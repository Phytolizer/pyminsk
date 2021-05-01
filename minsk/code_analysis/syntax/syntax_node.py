from abc import ABC, abstractmethod
from typing import Sequence

from minsk.code_analysis.syntax.syntax_kind import SyntaxKind


class SyntaxNode(ABC):
    @abstractmethod
    def kind(self) -> SyntaxKind:
        pass

    @abstractmethod
    def children(self) -> Sequence["SyntaxNode"]:
        pass
