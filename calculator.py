"""
Calculator Module

A simple calculator that supports basic arithmetic operations.
"""

from typing import Union

Number = Union[int, float]


class Calculator:
    """A calculator class that performs basic arithmetic operations."""

    def __init__(self):
        """Initialize the calculator with a memory value of 0."""
        self.memory = 0

    def add(self, a: Number, b: Number) -> Number:
        """Add two numbers together.
        
        Args:
            a: First number
            b: Second number
            
        Returns:
            The sum of a and b
        """
        return a + b

    def subtract(self, a: Number, b: Number) -> Number:
        """Subtract b from a.
        
        Args:
            a: First number
            b: Second number
            
        Returns:
            The difference of a and b
        """
        return a - b

    def multiply(self, a: Number, b: Number) -> Number:
        """Multiply two numbers together.
        
        Args:
            a: First number
            b: Second number
            
        Returns:
            The product of a and b
        """
        return a * b

    def divide(self, a: Number, b: Number) -> float:
        """Divide a by b.
        
        Args:
            a: Dividend
            b: Divisor
            
        Returns:
            The quotient of a divided by b
            
        Raises:
            ValueError: If b is zero
        """
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

    def power(self, base: Number, exponent: Number) -> Number:
        """Raise base to the power of exponent.
        
        Args:
            base: The base number
            exponent: The exponent
            
        Returns:
            base raised to the power of exponent
        """
        return base ** exponent

    def modulo(self, a: Number, b: Number) -> Number:
        """Calculate the remainder of a divided by b.
        
        Args:
            a: Dividend
            b: Divisor
            
        Returns:
            The remainder of a divided by b
            
        Raises:
            ValueError: If b is zero
        """
        if b == 0:
            raise ValueError("Cannot calculate modulo with zero divisor")
        return a % b

    def square_root(self, a: Number) -> float:
        """Calculate the square root of a number.
        
        Args:
            a: The number to find the square root of
            
        Returns:
            The square root of a
            
        Raises:
            ValueError: If a is negative
        """
        if a < 0:
            raise ValueError("Cannot calculate square root of a negative number")
        return a ** 0.5

    def store(self, value: Number) -> None:
        """Store a value in memory.
        
        Args:
            value: The value to store
        """
        self.memory = value

    def recall(self) -> Number:
        """Recall the value stored in memory.
        
        Returns:
            The value stored in memory
        """
        return self.memory

    def clear_memory(self) -> None:
        """Clear the memory (set to 0)."""
        self.memory = 0


def calculate(expression: str) -> Number:
    """Evaluate a simple arithmetic expression.
    
    Supports: +, -, *, /, ^, %
    
    Args:
        expression: A string containing a simple arithmetic expression
                   (e.g., "5 + 3", "10 * 2")
    
    Returns:
        The result of the calculation
        
    Raises:
        ValueError: If the expression is invalid
    """
    calc = Calculator()
    
    # Parse the expression
    expression = expression.strip()
    
    operators = {
        '+': calc.add,
        '-': calc.subtract,
        '*': calc.multiply,
        '/': calc.divide,
        '^': calc.power,
        '%': calc.modulo,
    }
    
    # Find the operator
    operator = None
    operator_pos = -1
    
    for op in operators:
        # Find operator, but skip if it's at the start (negative number)
        pos = expression.rfind(op)
        if pos > 0:
            operator = op
            operator_pos = pos
            break
    
    if operator is None:
        # Try to parse as a single number
        try:
            return float(expression) if '.' in expression else int(expression)
        except ValueError:
            raise ValueError(f"Invalid expression: {expression}")
    
    # Split the expression
    left = expression[:operator_pos].strip()
    right = expression[operator_pos + 1:].strip()
    
    try:
        a = float(left) if '.' in left else int(left)
        b = float(right) if '.' in right else int(right)
    except ValueError:
        raise ValueError(f"Invalid numbers in expression: {expression}")
    
    return operators[operator](a, b)


if __name__ == "__main__":
    # Quick demo
    calc = Calculator()
    
    print("Calculator Demo")
    print("-" * 30)
    print(f"5 + 3 = {calc.add(5, 3)}")
    print(f"10 - 4 = {calc.subtract(10, 4)}")
    print(f"6 * 7 = {calc.multiply(6, 7)}")
    print(f"20 / 4 = {calc.divide(20, 4)}")
    print(f"2 ^ 8 = {calc.power(2, 8)}")
    print(f"17 % 5 = {calc.modulo(17, 5)}")
    print(f"sqrt(16) = {calc.square_root(16)}")
