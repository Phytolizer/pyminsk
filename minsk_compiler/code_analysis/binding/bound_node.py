from abc import ABC, abstractmethod

from minsk_compiler.code_analysis.binding.bound_node_kind import BoundNodeKind


class BoundNode(ABC):
    @abstractmethod
    def kind(self) -> BoundNodeKind:
        pass
