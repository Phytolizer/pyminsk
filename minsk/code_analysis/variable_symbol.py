from dataclasses import dataclass
from typing import Type


@dataclass
class VariableSymbol:
    name: str
    type: Type

    def __eq__(self, other: "VariableSymbol") -> bool:
        return self.name == other.name and self.type == other.type

    def __hash__(self):
        return hash(self.name) * hash(self.type)
