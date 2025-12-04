# Solutions 
from Solutions.Python.Two_Sum import TwoSum

class Solution:
    def __init__(self):
        self.solution_name = "Base Solution Class"
        self.description = "This is a base class for solutions."
        self.version = "1.0"
        self.solutions = {
            "0001": TwoSum(),
        }  # Dictionary to hold different solution methods
    
    def get_solution(self, problem_id):
        if isinstance(problem_id, int):
            problem_id = f"{problem_id:04d}"  # Convert to zero-padded string
        problem_id = f"{problem_id:0>4}"  # Ensure it's a 4-digit string
        if problem_id not in self.solutions:
            print(f"Solution for problem ID {problem_id} not found.")
            return None
        return self.solutions.get(problem_id, None)
    
    def get_solution_declinations(self, problem_id):
        solution_instance = self.get_solution(problem_id)
        if solution_instance is None:
            return None
        return solution_instance.declinations