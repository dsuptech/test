#!/usr/bin/env python3
"""
Command Line Interface Calculator

An interactive calculator that runs in the terminal.
"""

from calculator import Calculator, calculate


def print_help():
    """Print help information."""
    print("""
Calculator Commands:
--------------------
Basic Operations:
  <number> + <number>   - Addition
  <number> - <number>   - Subtraction  
  <number> * <number>   - Multiplication
  <number> / <number>   - Division
  <number> ^ <number>   - Power/Exponent
  <number> % <number>   - Modulo

Special Operations:
  sqrt <number>         - Square root

Memory Operations:
  store <number>        - Store value in memory
  recall               - Recall value from memory
  clear                - Clear memory

Other Commands:
  help                 - Show this help message
  quit / exit          - Exit the calculator
""")


def main():
    """Run the interactive calculator."""
    calc = Calculator()
    
    print("=" * 40)
    print("       Welcome to the Calculator!")
    print("=" * 40)
    print("Type 'help' for available commands")
    print("Type 'quit' or 'exit' to exit")
    print()

    while True:
        try:
            user_input = input(">>> ").strip()
            
            if not user_input:
                continue
            
            # Handle special commands
            lower_input = user_input.lower()
            
            if lower_input in ('quit', 'exit', 'q'):
                print("Goodbye!")
                break
            
            if lower_input == 'help':
                print_help()
                continue
            
            if lower_input == 'recall':
                print(f"Memory: {calc.recall()}")
                continue
            
            if lower_input == 'clear':
                calc.clear_memory()
                print("Memory cleared")
                continue
            
            if lower_input.startswith('store '):
                try:
                    value = float(user_input[6:].strip())
                    calc.store(value)
                    print(f"Stored: {value}")
                except ValueError:
                    print("Error: Invalid number to store")
                continue
            
            if lower_input.startswith('sqrt '):
                try:
                    value = float(user_input[5:].strip())
                    result = calc.square_root(value)
                    print(f"= {result}")
                except ValueError as e:
                    print(f"Error: {e}")
                continue
            
            # Try to evaluate as an expression
            try:
                result = calculate(user_input)
                print(f"= {result}")
            except ValueError as e:
                print(f"Error: {e}")
            except Exception as e:
                print(f"Error: {e}")
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except EOFError:
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()
