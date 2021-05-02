from dataclasses import dataclass


@dataclass
class TextSpan:
    start: int
    length: int

    def end(self):
        return self.start + self.length

    @staticmethod
    def from_bounds(start, end) -> "TextSpan":
        return TextSpan(start, end - start)
