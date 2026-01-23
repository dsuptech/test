def calculate(left, operator, right):
    if operator == "+":
        return left + right
    if operator == "-":
        return left - right
    if operator == "*":
        return left * right
    if operator == "/":
        if right == 0:
            raise ZeroDivisionError("division by zero")
        return left / right
    raise ValueError("unsupported operator")


def main():
    print("Simple Calculator")
    try:
        left = float(input("Enter first number: ").strip())
        operator = input("Enter operator (+, -, *, /): ").strip()
        right = float(input("Enter second number: ").strip())
        result = calculate(left, operator, right)
        print(f"Result: {result}")
    except ZeroDivisionError:
        print("Error: division by zero.")
    except ValueError as exc:
        print(f"Error: {exc}")
    except Exception:
        print("Error: invalid input.")


if __name__ == "__main__":
    main()
