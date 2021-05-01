from abc import ABC, abstractmethod
from typing import Type

from minsk.code_analysis.binding.bound_node import BoundNode


class BoundExpression(BoundNode, ABC):
    @abstractmethod
    def type(self) -> Type:
        pass
