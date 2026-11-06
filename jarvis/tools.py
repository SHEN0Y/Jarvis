"""Tool registry. Decorate a function with @tool to expose it to Jarvis."""
import ast
import operator
from datetime import datetime

TOOLS = {}


def tool(description, properties=None):
    properties = properties or {}

    def wrap(fn):
        TOOLS[fn.__name__] = {
            "fn": fn,
            "schema": {
                "name": fn.__name__,
                "description": description,
                "input_schema": {
                    "type": "object",
                    "properties": properties,
                    "required": list(properties),
                },
            },
        }
        return fn

    return wrap


def run_tool(name, args):
    if name not in TOOLS:
        return f"Unknown tool: {name}"
    try:
        return str(TOOLS[name]["fn"](**args))
    except Exception as e:
        return f"Tool error: {e}"


@tool("Get the current local date and time")
def get_time() -> str:
    return datetime.now().strftime("%A, %B %d %Y, %I:%M %p")


_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}


def _eval(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval(node.left), _eval(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval(node.operand))
    raise ValueError("Unsupported expression")


@tool("Evaluate a math expression, e.g. '2 * (3 + 4)'", {"expression": {"type": "string"}})
def calculate(expression: str) -> str:
    return _eval(ast.parse(expression, mode="eval").body)


@tool("Save a note to notes.txt", {"text": {"type": "string"}})
def save_note(text: str) -> str:
    with open("notes.txt", "a") as f:
        f.write(f"{datetime.now().isoformat()} {text}\n")
    return "Note saved."
