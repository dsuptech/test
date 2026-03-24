def calculate(a: float, operator: str, b: float) -> float:
    if operator == "+":
        return a + b
    if operator == "-":
        return a - b
    if operator == "*":
        return a * b
    if operator == "/":
        if b == 0:
            raise ZeroDivisionError("0으로 나눌 수 없습니다.")
        return a / b
    raise ValueError("지원하지 않는 연산자입니다. (+, -, *, / 만 가능)")


def main() -> None:
    print("간단 계산기")
    print("형식: 숫자 연산자 숫자 (예: 3 + 4)")

    expr = input("계산식을 입력하세요: ").strip().split()
    if len(expr) != 3:
        print("입력 형식이 올바르지 않습니다.")
        return

    try:
        a = float(expr[0])
        operator = expr[1]
        b = float(expr[2])
        result = calculate(a, operator, b)
        print(f"결과: {result}")
    except Exception as e:
        print(f"오류: {e}")


if __name__ == "__main__":
    main()
