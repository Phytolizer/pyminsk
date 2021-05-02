from typing import List, Sequence, Union

from minsk.code_analysis.text.text_span import TextSpan


class TextLine:
    source_text: "SourceText"
    start: int
    length: int
    length_including_line_break: int

    def __init__(self, source_text: "SourceText", start: int, length: int, length_including_line_break: int):
        self.source_text = source_text
        self.start = start
        self.length = length
        self.length_including_line_break = length_including_line_break

    @property
    def span(self) -> TextSpan:
        return TextSpan(self.start, self.length)

    @property
    def span_including_line_break(self) -> TextSpan:
        return TextSpan(self.start, self.length_including_line_break)


class SourceText:
    _CREATE_KEY = object()
    text: str
    lines: Sequence[TextLine]

    def __init__(self, create_key: object, text: str):
        if create_key != SourceText._CREATE_KEY:
            raise RuntimeError("please use SourceText.create_from instead of initializing directly")
        self.text = text
        self.lines = self._parse_lines(self, text)

    @classmethod
    def create_from(cls, text: str) -> "SourceText":
        return SourceText(SourceText._CREATE_KEY, text)

    def get_line_index(self, position) -> int:
        lower = 0
        upper = len(self.lines) - 1

        while lower <= upper:
            index = lower + (upper - lower) // 2
            start = self.lines[index].start

            if start == position:
                return index
            elif start < position:
                upper = index - 1
            elif start > position:
                lower = index + 1

        return lower

    @staticmethod
    def _parse_lines(source_text: "SourceText", text: str) -> Sequence[TextLine]:
        result: List[TextLine] = []

        position = 0
        line_start = 0
        while position < len(text):
            line_break_width = SourceText._get_line_break_width(text, position)

            if line_break_width == 0:
                position += 1
            else:
                line = SourceText._add_line(source_text, position, line_start, line_break_width)
                result.append(line)
                position += line_break_width
                line_start = position

        if position > line_start:
            result.append(SourceText._add_line(source_text, position, line_start, 0))

        return result

    @staticmethod
    def _add_line(source_text: "SourceText", position: int, line_start: int, line_break_width: int):
        line_length = position - line_start
        line_length_including_line_break = line_length + line_break_width
        line = TextLine(source_text, line_start, line_length, line_length_including_line_break)
        return line

    @staticmethod
    def _get_line_break_width(text: str, position: int) -> int:
        current = text[position]
        if position + 1 >= len(text):
            lookahead = "\0"
        else:
            lookahead = text[position + 1]
        if current == "\r" and lookahead == "\n":
            return 2
        if current == "\r" or current == "\n":
            return 1
        return 0

    def __str__(self) -> str:
        return self.text

    def __getitem__(self, item):
        return self.text[item]

    def __len__(self):
        return len(self.text)

    def to_string(self, span_or_start: Union[int, TextSpan], length: int) -> str:
        if isinstance(span_or_start, int):
            start = span_or_start
            end = length + start
            return self.text[start:end]
        else:
            span = span_or_start
            return self.to_string(span.start, span.length)
