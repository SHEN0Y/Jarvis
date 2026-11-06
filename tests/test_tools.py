from jarvis.tools import run_tool


def test_calculate():
    assert run_tool("calculate", {"expression": "2 * (3 + 4)"}) == "14"


def test_unknown_tool():
    assert "Unknown" in run_tool("nope", {})
