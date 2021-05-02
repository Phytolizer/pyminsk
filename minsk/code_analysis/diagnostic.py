from dataclasses import dataclass

from minsk.code_analysis.text.text_span import TextSpan


@dataclass
class Diagnostic:
    span: TextSpan
    message: str

    def __str__(self):
        return self.message
