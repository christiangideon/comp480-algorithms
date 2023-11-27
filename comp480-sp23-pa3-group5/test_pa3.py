# File: test_pa3.py
# Author: John Glick    
# Date: March 23, 2023
# Description: Program that tests the correctness
#              of pa3, comp 480, spring 2023.

import sys
from time import process_time

# import the module containing pa1 solution
import pa3

def run_test(test_input_filename, correct_output_filename):
    """
    Runs the test inputs specified in test_input_filename,
    whose correct output is in correct_output_filename.
    Returns (num_cases, num_queries, correct_queries, correct_headers)
    associated with the test.
    """  

    # Run the program 
    results_filename = "temp.out"
    orig_std_output = sys.stdout
    sys.stdout = open(results_filename, "w")
    pa3.solve(test_input_filename)
    sys.stdout.close()
    sys.stdout = orig_std_output
    print(f"Finished running tests from {test_input_filename}")
    
    # Open files
    test_input_file = open(test_input_filename)
    correct_output_file = open(correct_output_filename)
    results_file = open(results_filename)

    # Get number of cases and queries 
    num_cases = 0
    num_queries = 0
    queries_per_case = []
    while True:
        n_c, n_r, n_s, n_q = (int(x) for x in test_input_file.readline().split())
        if n_c == 0 and n_r == 0 and n_s == 0 and n_q == 0:
            break
        num_cases += 1
        queries_per_case.append(n_q)
        num_queries += n_q
        for _ in range(n_s):
            test_input_file.readline()
        for _ in range(n_q):
            test_input_file.readline()

    # Check answers
    correct_queries = 0
    correct_headers = 0
    for i in range(1, num_cases + 1):
        print(f"Case {i}")
        result = results_file.readline()
        correct = correct_output_file.readline()
        if result.strip() == correct.strip():
            correct_headers += 1
        else:
            print(f"Output header for case {i} incorrect")
            print(f"Correct: '{correct}'")
            print(f"Yours: '{result}'")
        for q in range(queries_per_case[i-1]):
            result = results_file.readline()
            correct = correct_output_file.readline()
            if result.strip() == correct.strip():
                correct_queries += 1
            else:
                print(f"For case {i}, query {q} incorrect")
                print(f"Correct: '{correct}'")
                print(f"Yours: '{result}'")

    return (num_cases, num_queries, correct_queries, correct_headers)

if __name__ == "__main__":

    # Print message
    print("Testing your program.")

    TARGET_RUN_TIME = 150

    total_cases = 0
    total_queries = 0
    total_correct_queries = 0
    total_correct_headers = 0

    start_time = process_time()

    print("Testing sample inputs")
    (num_cases, num_queries, correct_queries, correct_headers) = run_test(
        "test1.in", "test1.out")
    total_cases += num_cases
    total_queries += num_queries
    total_correct_queries += correct_queries
    total_correct_headers += correct_headers

    print("Testing more inputs")
    (num_cases, num_queries, correct_queries, correct_headers) = run_test(
        "test2.in", "test2.out")
    total_cases += num_cases
    total_queries += num_queries
    total_correct_queries += correct_queries
    total_correct_headers += correct_headers

    print("Testing big inputs")
    (num_cases, num_queries, correct_queries, correct_headers) = run_test(
        "test3.in", "test3.out")
    total_cases += num_cases
    total_queries += num_queries
    total_correct_queries += correct_queries
    total_correct_headers += correct_headers

    processor_time = process_time() - start_time
    print(f"Processor time = {processor_time} seconds")
    if processor_time > TARGET_RUN_TIME:
        print("Your run time higher than the target.  Look to make your program more efficient.")

    if total_correct_headers == total_cases and total_correct_queries == total_queries:
        print("All tests correct.")    
    else:
        print("Some incorrect output on these tests")
