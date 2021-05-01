from abc import ABC


class Addable(ABC):
    @classmethod
    def __subclasshook__(cls, c):
        if cls is Addable:
            if any("__add__" in b.__dict__ for b in c.__mro__) and any("__iadd__" in b.__dict__ for b in c.__mro__):
                return True
        return NotImplemented
