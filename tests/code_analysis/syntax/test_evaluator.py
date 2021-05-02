from typing import Any

import pytest

from minsk.code_analysis.compilation import Compilation
from minsk.code_analysis.syntax.syntax_tree import SyntaxTree


@pytest.mark.parametrize("text,expected_result", (
        ("1", 1),
        ("-1", -1),
        ("+1", 1),
        ("1 + 2", 3),
        ("1 - 2", -1),
        ("1 * 2", 2),
        ("1 / 2", 0),
        ("(1 + 2) * 3", 9),
        ("9 / 3", 3),
        ("(10)", 10),
        ("true", True),
        ("false", False),
        ("!true", False),
        ("!false", True),
        ("12 == 3", False),
        ("3 == 3", True),
        ("12 != 3", True),
        ("3 != 3", False),
        ("false == false", True),
        ("true == false", False),
        ("true != false", True),
        ("false != false", False),
        ("(a = 10) * a", 100),
))
def test_basic_evaluation(text: str, expected_result: Any):
    expression = SyntaxTree.parse(text)
    compilation = Compilation(expression)
    actual_result = compilation.evaluate(dict())
    assert len(actual_result.diagnostics) == 0
    assert actual_result.value == expected_result
