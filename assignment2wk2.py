# Jimmy Bolding
# CIS 261 - Object-Oriented Computer Programming I
# Week 2 Lab: Iterative and Recursive Functionality
# Submission Date: October 27, 2025

# Iterative factorial function
def factorial_iterative(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

# Recursive factorial function
def factorial_recursive(n):
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial_recursive(n - 1)

# Main program
def main():
    try:
        number = int(input("Enter a non-negative integer: "))
        if number < 0:
            print("Please enter a non-negative integer.")
        else:
            print(f"Iterative result: {factorial_iterative(number)}")
            print(f"Recursive result: {factorial_recursive(number)}")
    except ValueError:
        print("Invalid input. Please enter an integer.")

main()