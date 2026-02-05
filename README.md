# Python Calculator

A simple yet powerful calculator application built in Python. Includes basic arithmetic operations, advanced mathematical functions, trigonometry, and a calculation history feature.

## Features

### Basic Operations
- **Addition** (`+`): Add two numbers
- **Subtraction** (`-`): Subtract numbers
- **Multiplication** (`*`): Multiply numbers
- **Division** (`/`): Divide numbers (with zero-division protection)

### Advanced Operations
- **Power** (`pow`): Raise a number to an exponent
- **Square Root** (`sqrt`): Calculate square root
- **Modulo** (`mod`): Calculate remainder
- **Absolute Value** (`abs`): Get absolute value
- **Factorial** (`fact`): Calculate factorial
- **Logarithm** (`log`): Natural log or custom base

### Trigonometric Functions
- **Sine** (`sin`): Calculate sine (input in degrees)
- **Cosine** (`cos`): Calculate cosine (input in degrees)
- **Tangent** (`tan`): Calculate tangent (input in degrees)

### Utility Features
- **History**: View all past calculations
- **Clear**: Clear calculation history
- **Ans**: Retrieve the last result

## Usage

### Interactive Mode

Run the calculator interactively:

```bash
python3 calculator.py
```

Example session:
```
> 5 + 3
= 8

> 10 / 2
= 5

> sqrt 16
= 4

> pow 2, 8
= 256

> sin 90
= 1

> history
Calculation History:
  1. 5 + 3 = 8
  2. 10 / 2 = 5
  3. sqrt(16) = 4
  4. 2 ^ 8 = 256
  5. sin(90) = 1

> quit
```

### As a Module

Import and use in your Python code:

```python
from calculator import Calculator

calc = Calculator()

# Basic operations
result = calc.add(10, 5)       # 15
result = calc.subtract(10, 5)  # 5
result = calc.multiply(10, 5)  # 50
result = calc.divide(10, 5)    # 2.0

# Advanced operations
result = calc.power(2, 10)     # 1024
result = calc.square_root(81)  # 9.0
result = calc.factorial(5)     # 120

# Access history
history = calc.get_history()
last = calc.get_last_result()
```

## Running Tests

Execute the test suite:

```bash
python3 -m unittest test_calculator -v
```

## Error Handling

The calculator handles common errors gracefully:
- Division by zero
- Square root of negative numbers
- Factorial of negative/non-integer values
- Invalid logarithm inputs

## Requirements

- Python 3.9+
- No external dependencies (uses only standard library)
