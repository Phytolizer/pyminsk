from dataclasses import dataclass
from typing import Type


@dataclass
class VariableSymbol:
    name: str
    type: Type

    def __eq__(self, other: object) -> bool:
        return isinstance(other, VariableSymbol) and self.name == other.name and self.type == other.type

    def __hash__(self):
        return hash(self.name) * hash(self.type)
