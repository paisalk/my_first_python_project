#!/usr/bin/env python3
"""
A simple Python script to demonstrate Git workflow
"""

def greet(name):
    """Return a greeting message"""
    return f"Hello, {name}! Welcome to Git!"

def multiply(a, b):
    """Multiply two numbers and return the result"""
    return a * b

def main():
    """Main function"""
    name = input("What's your name? ")
    message = greet(name)
    print(message)
    print("This is your first Git commit!")

if __name__ == "__main__":
    main()
