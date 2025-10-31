# Jim Bolding
# CIS 261 - Object-Oriented Computer Programming I
# Week 2 Lab: Guessing Game
# Submission Date: October 27, 2025

import random

def guessing_game():
    secret_number = random.randint(1, 100)
    guess = None
    attempts = 0

    print("Welcome to the Guessing Game!")
    print("I'm thinking of a number between 1 and 100.")

    while guess != secret_number:
        try:
            guess = int(input("Enter your guess: "))
            attempts += 1

            if guess < secret_number:
                print("Too low. Try again.")
            elif guess > secret_number:
                print("Too high. Try again.")
            else:
                print(f"Congratulations! You guessed it in {attempts} attempts.")
        except ValueError:
            print("Invalid input. Please enter an integer.")

guessing_game()