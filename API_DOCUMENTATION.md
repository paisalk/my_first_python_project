# API Documentation

## Overview

This document provides comprehensive documentation for all public APIs, functions, and components in the `hello.py` module. The module contains utility functions for greeting users and mathematical operations, along with a main entry point for interactive execution.

## Table of Contents

- [Functions](#functions)
  - [greet()](#greet)
  - [multiply()](#multiply)
  - [main()](#main)
- [Usage Examples](#usage-examples)
- [Module Import](#module-import)

## Functions

### greet()

**Description:** Returns a personalized greeting message for a given name.

**Signature:**
```python
def greet(name: str) -> str
```

**Parameters:**
- `name` (str): The name of the person to greet

**Returns:**
- `str`: A formatted greeting message

**Example:**
```python
from hello import greet

# Basic usage
message = greet("Alice")
print(message)  # Output: "Hello, Alice! Welcome to Git!"

# With different names
print(greet("Bob"))     # Output: "Hello, Bob! Welcome to Git!"
print(greet("Charlie")) # Output: "Hello, Charlie! Welcome to Git!"
```

**Error Handling:**
- Function expects a string input
- Will work with any string value, including empty strings

---

### multiply()

**Description:** Multiplies two values and returns the result. Works with numbers (multiplication) and strings with numbers (string repetition).

**Signature:**
```python
def multiply(a, b)
```

**Parameters:**
- `a`: The first value (number or string)
- `b`: The second value (number)

**Returns:**
- The product of the two input values (number result for numeric inputs, string result for string repetition)

**Example:**
```python
from hello import multiply

# Basic multiplication with numbers
result = multiply(5, 3)
print(result)  # Output: 15

# With floating point numbers
result = multiply(2.5, 4.0)
print(result)  # Output: 10.0

# With negative numbers
result = multiply(-3, 7)
print(result)  # Output: -21

# With zero
result = multiply(0, 100)
print(result)  # Output: 0

# String repetition
result = multiply("hello", 3)
print(result)  # Output: "hellohellohello"

# String with fractional repetition
result = multiply("x", 5)
print(result)  # Output: "xxxxx"
```

**Error Handling:**
- Function works with numeric types (int, float) and string repetition
- Will raise `TypeError` if operands cannot be multiplied (e.g., None types)

---

### main()

**Description:** The main entry point function that provides interactive user experience. Prompts for user input and displays a greeting message.

**Signature:**
```python
def main() -> None
```

**Parameters:**
- None

**Returns:**
- `None`: This function doesn't return a value, it performs I/O operations

**Behavior:**
1. Prompts the user to enter their name via `input()`
2. Calls `greet()` function with the provided name
3. Prints the greeting message
4. Prints an additional informational message

**Example:**
```python
from hello import main

# Interactive execution
main()
# Prompts: "What's your name? "
# User enters: "John"
# Output: 
# Hello, John! Welcome to Git!
# This is your first Git commit!
```

**Usage Notes:**
- This function is designed for interactive command-line usage
- Requires user input, so not suitable for automated scripts
- Called automatically when script is run directly

---

## Usage Examples

### Importing the Module

```python
# Import specific functions
from hello import greet, multiply

# Import the entire module
import hello

# Use with module prefix
message = hello.greet("World")
result = hello.multiply(10, 5)
```

### Complete Usage Example

```python
#!/usr/bin/env python3
from hello import greet, multiply

def example_usage():
    """Example demonstrating all public APIs"""
    
    # Using greet function
    names = ["Alice", "Bob", "Charlie"]
    for name in names:
        print(greet(name))
    
    # Using multiply function
    calculations = [
        (2, 3),
        (5.5, 2),
        (-4, 6),
        (0, 999)
    ]
    
    for a, b in calculations:
        result = multiply(a, b)
        print(f"{a} × {b} = {result}")

if __name__ == "__main__":
    example_usage()
```

### Command Line Usage

```bash
# Run the interactive main function
python3 hello.py

# Or make it executable and run directly
chmod +x hello.py
./hello.py
```

## Module Import

The module can be imported and used in other Python scripts:

```python
# Method 1: Import specific functions
from hello import greet, multiply

user_greeting = greet("Developer")
calculation_result = multiply(7, 8)

# Method 2: Import entire module
import hello

user_greeting = hello.greet("Developer")
calculation_result = hello.multiply(7, 8)
```

## API Compatibility

- **Python Version:** Compatible with Python 3.6+
- **Dependencies:** No external dependencies required
- **Thread Safety:** All functions are stateless and thread-safe
- **Type Hints:** Functions work with duck typing but expect numeric types for `multiply()` and string types for `greet()`

## Error Handling Examples

```python
from hello import greet, multiply

# greet() with edge cases
print(greet(""))           # Works: "Hello, ! Welcome to Git!"
print(greet("123"))        # Works: "Hello, 123! Welcome to Git!"

# multiply() with different types
print(multiply("hello", 5))    # Works: "hellohellohellohellohello" (string repetition)
print(multiply("x", 3))        # Works: "xxx" (string repetition)

# multiply() error cases  
try:
    multiply(None, 5)      # TypeError: unsupported operand type(s)
except TypeError as e:
    print(f"Error: {e}")

try:
    multiply(5, None)      # TypeError: unsupported operand type(s)  
except TypeError as e:
    print(f"Error: {e}")
```

---

**Last Updated:** $(date)
**Module Version:** 1.0.0