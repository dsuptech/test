#!/usr/bin/env python3
"""간단한 사칙연산 계산기 (모듈 + 명령줄)."""


def add(a: float, b: float) -> float:
    return a + b


def subtract(a: float, b: float) -> float:
    return a - b


def multiply(a: float, b: float) -> float:
    return a * b


def divide(a: float, b: float) -> float:
    if b == 0:
        raise ZeroDivisionError("0으로 나눌 수 없습니다.")
    return a / b


def calculate(a: float, op: str, b: float) -> float:
    """연산자 문자열: +, -, *, /"""
    ops = {
        "+": add,
        "-": subtract,
        "*": multiply,
        "/": divide,
    }
    if op not in ops:
        raise ValueError(f"지원하지 않는 연산자: {op!r} (+, -, *, / 만 가능)")
    return ops[op](a, b)


def main() -> None:
    import sys

    if len(sys.argv) == 4:
        try:
            x = float(sys.argv[1])
            op = sys.argv[2]
            y = float(sys.argv[3])
            result = calculate(x, op, y)
            print(result)
        except (ValueError, ZeroDivisionError) as e:
            print(e, file=sys.stderr)
            sys.exit(1)
        return

    print("사용법: python calculator.py <숫자> <연산자> <숫자>", file=sys.stderr)
    print("예: python calculator.py 10 + 3", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
