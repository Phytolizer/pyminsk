from dataclasses import dataclass


@dataclass
class TextSpan:
    start: int
    length: int

    def end(self):
        return self.start + self.length
