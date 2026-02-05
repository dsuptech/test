# Python Calculator

A simple, well-structured calculator written in Python.

## Features

- Basic arithmetic operations: addition, subtraction, multiplication, division
- Advanced operations: power/exponent, modulo, square root
- Memory functions: store, recall, clear
- Interactive command-line interface
- Comprehensive test suite

## Files

- `calculator.py` - Main calculator module with `Calculator` class
- `cli_calculator.py` - Interactive command-line interface
- `test_calculator.py` - Unit tests

## Usage

### As a Module

```python
from calculator import Calculator

calc = Calculator()

# Basic operations
print(calc.add(5, 3))        # 8
print(calc.subtract(10, 4))  # 6
print(calc.multiply(6, 7))   # 42
print(calc.divide(20, 4))    # 5.0

# Advanced operations
print(calc.power(2, 8))      # 256
print(calc.modulo(17, 5))    # 2
print(calc.square_root(16))  # 4.0

# Memory operations
calc.store(42)
print(calc.recall())         # 42
calc.clear_memory()
```

### Using the Expression Parser

```python
from calculator import calculate

print(calculate("5 + 3"))    # 8
print(calculate("10 * 2"))   # 20
print(calculate("2 ^ 8"))    # 256
```

### Interactive CLI

Run the interactive calculator:

```bash
python cli_calculator.py
```

Available commands:
- Basic math: `5 + 3`, `10 - 4`, `6 * 7`, `20 / 4`
- Power: `2 ^ 8`
- Modulo: `17 % 5`
- Square root: `sqrt 16`
- Memory: `store 42`, `recall`, `clear`
- Help: `help`
- Exit: `quit` or `exit`

## Running Tests

```bash
python -m unittest test_calculator -v
```

Or simply:

```bash
python test_calculator.py
```

## Quick Demo

```bash
python calculator.py
```
