#!/usr/bin/env python3
from __future__ import annotations

import ast
import operator as op
import sys
from typing import Callable, Dict


class CalculatorError(ValueError):
    """Raised when an expression cannot be evaluated safely."""


_ALLOWED_BINOPS: Dict[type, Callable[[float, float], float]] = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
}

_ALLOWED_UNARYOPS: Dict[type, Callable[[float], float]] = {
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}


def _require_number(value: object, label: str = "value") -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{label} must be int or float")
    return float(value) if isinstance(value, int) else value


def add(a: float, b: float) -> float:
    return _require_number(a, "a") + _require_number(b, "b")


def subtract(a: float, b: float) -> float:
    return _require_number(a, "a") - _require_number(b, "b")


def multiply(a: float, b: float) -> float:
    return _require_number(a, "a") * _require_number(b, "b")


def divide(a: float, b: float) -> float:
    return _require_number(a, "a") / _require_number(b, "b")


def floor_divide(a: float, b: float) -> float:
    return _require_number(a, "a") // _require_number(b, "b")


def modulo(a: float, b: float) -> float:
    return _require_number(a, "a") % _require_number(b, "b")


def power(a: float, b: float) -> float:
    return _require_number(a, "a") ** _require_number(b, "b")


def _eval_node(node: ast.AST) -> float:
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)
    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in _ALLOWED_BINOPS:
            raise CalculatorError(f"Operator {op_type.__name__} is not allowed")
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        return _ALLOWED_BINOPS[op_type](left, right)
    if isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in _ALLOWED_UNARYOPS:
            raise CalculatorError(f"Unary operator {op_type.__name__} is not allowed")
        operand = _eval_node(node.operand)
        return _ALLOWED_UNARYOPS[op_type](operand)
    if isinstance(node, ast.Constant):
        if isinstance(node.value, bool) or not isinstance(node.value, (int, float)):
            raise CalculatorError("Only numeric literals are allowed")
        return float(node.value) if isinstance(node.value, int) else node.value
    if isinstance(node, ast.Num):  # pragma: no cover - for older Python ASTs
        return float(node.n) if isinstance(node.n, int) else node.n
    raise CalculatorError(f"Unsupported expression: {type(node).__name__}")


def evaluate(expression: str) -> float:
    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError as exc:
        raise CalculatorError(f"Invalid expression: {expression}") from exc
    return _eval_node(tree)


def _parse_number(text: str) -> float:
    try:
        if text.lower().startswith(("0x", "0o", "0b")):
            return float(int(text, 0))
        if any(char in text for char in (".", "e", "E")):
            return float(text)
        return float(int(text))
    except ValueError as exc:
        raise CalculatorError(f"Invalid number: {text}") from exc


_OPERATIONS: Dict[str, Callable[[float, float], float]] = {
    "add": add,
    "sub": subtract,
    "mul": multiply,
    "div": divide,
    "floordiv": floor_divide,
    "mod": modulo,
    "pow": power,
}


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args or args[0] in {"-h", "--help"}:
        print(
            "Usage:\n"
            "  calculator.py \"2 + 3 * 4\"\n"
            "  calculator.py add 2 3\n\n"
            "Supported operators: +, -, *, /, //, %, **, parentheses"
        )
        return 0

    if args[0] in _OPERATIONS:
        if len(args) != 3:
            print("Error: operation requires exactly two numbers", file=sys.stderr)
            return 2
        left = _parse_number(args[1])
        right = _parse_number(args[2])
        result = _OPERATIONS[args[0]](left, right)
    else:
        expression = " ".join(args)
        result = evaluate(expression)

    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
