"""
Runs the solution code with specified parameters.
"""
import json 
import time as tm
from Structural.solution_class import Solution

class PythonRunner:
    def __init__(self ):
        self.solution_instance = Solution()
        self.solution_function = None
        self.solution_declinations = None
        self.method_name = None

    def __get_solution_function(self, problem_id):
        self.solution_function = self.solution_instance.get_solution(problem_id)
        if self.solution_function is None:
            raise ValueError(f"No solution found for problem ID {problem_id}")
    
    def __get_solution_declinations(self, problem_id):
        self.solution_declinations = self.solution_instance.get_solution_declinations(problem_id)
        if self.solution_declinations is None:
            raise ValueError(f"No declinations found for problem ID {problem_id}")
        
    def __get_method_name(self, method_index : int):
        if method_index < 0 or method_index >= len(self.solution_declinations):
            raise ValueError(f"Method index '{method_index}' is out of range. Available methods: 0 to {len(self.solution_declinations)-1}")
        else : 
            self.method_name = self.solution_declinations[method_index]

    def __get_test_data(self, problem_id):
        with open(f"TestCases/problem_{problem_id:0>4}.json", 'r') as f:
            data = json.load(f)
        return data
    
    def __run_test_case(self, case : dict):
        description = case.pop('description', 'No description')
        expected_output = case.pop('expected_output', None)
        result = self.solution_function(**case, method=self.method_name) 
        # Check if the result matches the expected output
        if expected_output is not None:
            assert result == expected_output, f"Test failed for case: {description}. Expected {expected_output}, got {result}"
        print(f"Description: {description}, Input: {case}, Expected Output: {expected_output}")
        print(f"Result: {result} -> Test Passed!")

    def run_eager(self, problem_id, method_index : int):
        # Getting the solution function and declinations
        self.__get_solution_function(problem_id)
        self.__get_solution_declinations(problem_id) 
        self.__get_method_name(method_index)
        print(f"Running Problem ID: {problem_id} with Method name: {self.method_name}")
        print("Problem Description:", self.solution_function.description)
        print("---------------------------------------------------")
        # Getting the data 
        data = self.__get_test_data(problem_id)
        # Running the solution with the specified method
        start_time = tm.time()
        base = data.get('Base',[])  
        print("------ Testing the solution with Base data ------")
        for case in base:
            self.__run_test_case(case)
        # Running the solution with the extra data
        extra = data.get('Edge',[])
        print("------ Testing the solution with Edge cases ------")
        for case in extra:
            self.__run_test_case(case)
        end_time = tm.time()
        print(f"All Test Cases Passed ! Total execution time: {end_time - start_time} seconds")

    def run_inline(self, problem_id, method_index : int, **kwargs):
        pass # Made for future use