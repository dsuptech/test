#!/usr/bin/env python3
"""
A simple yet powerful calculator application.
Supports basic arithmetic operations and more advanced functions.
"""

import math
from typing import Union

Number = Union[int, float]


class Calculator:
    """A calculator class that performs various mathematical operations."""
    
    def __init__(self):
        self.history: list[str] = []
        self.last_result: Number = 0
    
    def _record(self, operation: str, result: Number) -> Number:
        """Record an operation in history and return the result."""
        self.history.append(f"{operation} = {result}")
        self.last_result = result
        return result
    
    # Basic Operations
    def add(self, a: Number, b: Number) -> Number:
        """Add two numbers."""
        result = a + b
        return self._record(f"{a} + {b}", result)
    
    def subtract(self, a: Number, b: Number) -> Number:
        """Subtract b from a."""
        result = a - b
        return self._record(f"{a} - {b}", result)
    
    def multiply(self, a: Number, b: Number) -> Number:
        """Multiply two numbers."""
        result = a * b
        return self._record(f"{a} * {b}", result)
    
    def divide(self, a: Number, b: Number) -> Number:
        """Divide a by b."""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        result = a / b
        return self._record(f"{a} / {b}", result)
    
    # Advanced Operations
    def power(self, base: Number, exponent: Number) -> Number:
        """Raise base to the power of exponent."""
        result = base ** exponent
        return self._record(f"{base} ^ {exponent}", result)
    
    def square_root(self, n: Number) -> Number:
        """Calculate the square root of n."""
        if n < 0:
            raise ValueError("Cannot calculate square root of negative number")
        result = math.sqrt(n)
        return self._record(f"sqrt({n})", result)
    
    def modulo(self, a: Number, b: Number) -> Number:
        """Calculate a modulo b."""
        if b == 0:
            raise ValueError("Cannot perform modulo by zero")
        result = a % b
        return self._record(f"{a} % {b}", result)
    
    def absolute(self, n: Number) -> Number:
        """Calculate the absolute value of n."""
        result = abs(n)
        return self._record(f"|{n}|", result)
    
    def factorial(self, n: int) -> int:
        """Calculate the factorial of n."""
        if not isinstance(n, int) or n < 0:
            raise ValueError("Factorial requires a non-negative integer")
        result = math.factorial(n)
        return self._record(f"{n}!", result)
    
    def logarithm(self, n: Number, base: Number = math.e) -> Number:
        """Calculate the logarithm of n with given base (default: natural log)."""
        if n <= 0:
            raise ValueError("Logarithm requires a positive number")
        if base <= 0 or base == 1:
            raise ValueError("Logarithm base must be positive and not equal to 1")
        result = math.log(n, base)
        if base == math.e:
            return self._record(f"ln({n})", result)
        return self._record(f"log_{base}({n})", result)
    
    # Trigonometric Functions
    def sin(self, angle: Number, degrees: bool = False) -> Number:
        """Calculate the sine of an angle."""
        if degrees:
            angle = math.radians(angle)
        result = math.sin(angle)
        return self._record(f"sin({angle})", result)
    
    def cos(self, angle: Number, degrees: bool = False) -> Number:
        """Calculate the cosine of an angle."""
        if degrees:
            angle = math.radians(angle)
        result = math.cos(angle)
        return self._record(f"cos({angle})", result)
    
    def tan(self, angle: Number, degrees: bool = False) -> Number:
        """Calculate the tangent of an angle."""
        if degrees:
            angle = math.radians(angle)
        result = math.tan(angle)
        return self._record(f"tan({angle})", result)
    
    # Utility Methods
    def clear_history(self) -> None:
        """Clear the calculation history."""
        self.history.clear()
        self.last_result = 0
    
    def get_history(self) -> list[str]:
        """Return the calculation history."""
        return self.history.copy()
    
    def get_last_result(self) -> Number:
        """Return the last calculated result."""
        return self.last_result


def interactive_calculator():
    """Run an interactive calculator session."""
    calc = Calculator()
    
    print("=" * 50)
    print("       Welcome to the Python Calculator!")
    print("=" * 50)
    print("\nAvailable operations:")
    print("  Basic:    +, -, *, /")
    print("  Advanced: pow, sqrt, mod, abs, fact, log")
    print("  Trig:     sin, cos, tan")
    print("  Utility:  history, clear, ans (last result)")
    print("  Exit:     quit or exit")
    print("-" * 50)
    
    while True:
        try:
            user_input = input("\n> ").strip().lower()
            
            if not user_input:
                continue
            
            if user_input in ('quit', 'exit', 'q'):
                print("Thank you for using the calculator. Goodbye!")
                break
            
            if user_input == 'history':
                history = calc.get_history()
                if history:
                    print("\nCalculation History:")
                    for i, entry in enumerate(history, 1):
                        print(f"  {i}. {entry}")
                else:
                    print("No calculations yet.")
                continue
            
            if user_input == 'clear':
                calc.clear_history()
                print("History cleared.")
                continue
            
            if user_input == 'ans':
                print(f"Last result: {calc.get_last_result()}")
                continue
            
            # Parse and execute operations
            result = None
            
            # Basic operations with two numbers
            if '+' in user_input:
                parts = user_input.split('+')
                a, b = float(parts[0].strip()), float(parts[1].strip())
                result = calc.add(a, b)
            elif '-' in user_input and not user_input.startswith('-'):
                parts = user_input.split('-')
                a, b = float(parts[0].strip()), float(parts[1].strip())
                result = calc.subtract(a, b)
            elif '*' in user_input:
                parts = user_input.split('*')
                a, b = float(parts[0].strip()), float(parts[1].strip())
                result = calc.multiply(a, b)
            elif '/' in user_input:
                parts = user_input.split('/')
                a, b = float(parts[0].strip()), float(parts[1].strip())
                result = calc.divide(a, b)
            elif user_input.startswith('pow'):
                parts = user_input[3:].strip().split(',')
                base, exp = float(parts[0].strip()), float(parts[1].strip())
                result = calc.power(base, exp)
            elif user_input.startswith('sqrt'):
                n = float(user_input[4:].strip())
                result = calc.square_root(n)
            elif user_input.startswith('mod'):
                parts = user_input[3:].strip().split(',')
                a, b = float(parts[0].strip()), float(parts[1].strip())
                result = calc.modulo(a, b)
            elif user_input.startswith('abs'):
                n = float(user_input[3:].strip())
                result = calc.absolute(n)
            elif user_input.startswith('fact'):
                n = int(user_input[4:].strip())
                result = calc.factorial(n)
            elif user_input.startswith('log'):
                parts = user_input[3:].strip().split(',')
                if len(parts) == 1:
                    result = calc.logarithm(float(parts[0].strip()))
                else:
                    result = calc.logarithm(float(parts[0].strip()), float(parts[1].strip()))
            elif user_input.startswith('sin'):
                n = float(user_input[3:].strip())
                result = calc.sin(n, degrees=True)
            elif user_input.startswith('cos'):
                n = float(user_input[3:].strip())
                result = calc.cos(n, degrees=True)
            elif user_input.startswith('tan'):
                n = float(user_input[3:].strip())
                result = calc.tan(n, degrees=True)
            else:
                # Try to evaluate as a simple number
                try:
                    result = float(user_input)
                    print(f"= {result}")
                    continue
                except ValueError:
                    print("Unknown operation. Type 'quit' to exit.")
                    continue
            
            if result is not None:
                # Format result nicely
                if isinstance(result, float) and result.is_integer():
                    print(f"= {int(result)}")
                else:
                    print(f"= {result}")
                    
        except ValueError as e:
            print(f"Error: {e}")
        except IndexError:
            print("Error: Invalid input format. Please check your syntax.")
        except KeyboardInterrupt:
            print("\n\nExiting calculator...")
            break


if __name__ == "__main__":
    interactive_calculator()
