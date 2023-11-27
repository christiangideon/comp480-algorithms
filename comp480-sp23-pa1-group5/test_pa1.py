# File: test_pa1.py
# Author: John Glick    
# Date: February 7, 2023
# Description: Program that tests the correctness
#              of pa1, comp 480, spring 2023.

import sys
import time
import numpy as np

# import the module containing pa1 solution
from pa1 import gale_shapley

def test_problems(message, start_index, end_index, num_tests, num_correct, incorrect_tests):
    """
    Test problem indices start_index up to and including end_index.
    """
    print(message)
    for i in range(start_index, end_index + 1):
        num_tests += 1
        filename = f"input{i}.txt"
        print(f"Testing input file {filename}")
        solution_filename = f"solution{i}.txt"
        solution_f = open(solution_filename, "r")
        correct_answer = [None if i == "None" else int(i) for i in solution_f.readline().split()]
        your_answer = gale_shapley(filename)
        if your_answer == correct_answer:
            print("Correct\n")
            num_correct += 1
        else:
            print("Incorrect")
            print(f"Your answer = {your_answer}")
            print(f"Correct answer = {correct_answer}")
            incorrect_tests.append(i)
    
    return (num_tests, num_correct, incorrect_tests)


if __name__ == "__main__":

    # Print message
    print("Checking your program.")

    # Test for correctness
    num_tests = 0
    num_correct = 0
    incorrect_tests = []
    message = """ Testing 'basic' problems where each hospital
          has one position and there are the same number of
          hospitals as student.\n"""
    (num_tests, num_correct, incorrect_tests) = test_problems(message, 1, 5, num_tests, num_correct, incorrect_tests)

    message = """ Testing problems where each hospital
          has more than one position, all hospitals have the same
          number of positions, and there are the same number of
          positions as student.\n"""
    (num_tests, num_correct, incorrect_tests) = test_problems(message, 6, 9, num_tests, num_correct, incorrect_tests)
    
    message = """Testing problems where each hospital
          has more than one position, all hospitals have the same
          number of positions, but there are more students than positions.\n"""
    (num_tests, num_correct, incorrect_tests) = test_problems(message, 10, 13, num_tests, num_correct, incorrect_tests)

    message = """Testing problems where each hospital
          has more than one position, hospitals have varying numbers of positions
          number of positions, and there are more students than positions.\n"""
    (num_tests, num_correct, incorrect_tests) = test_problems(message, 14, 17, num_tests, num_correct, incorrect_tests)

    message = """Testing problems where each hospital
          has more than one position, hospitals have varying numbers of positions
          number of positions, and there are more positions than students.\n"""
    (num_tests, num_correct, incorrect_tests) = test_problems(message, 18, 21, num_tests, num_correct, incorrect_tests)


    if num_correct == num_tests:
        print("All correct.  Nice job!  Make sure your code meets other requirements before submitting")
    else:
        print(f"One or more tests incorrect.  Keep working on it.")
        print(f"Indices of incorrect tests = {incorrect_tests}")
        print(f"Keep working on it.")