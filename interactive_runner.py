#!/usr/bin/env python3

import json
import subprocess
import sys
import os

class InteractiveRunner:
    def __init__(self):
        self.problems = self.load_problems()
        self.selected_language = None
        self.selected_problem = None
        self.selected_method = None
    
    def load_problems(self):
        """Load the solved problems from JSON file"""
        try:
            with open('Mainfiles/solved_problems.json', 'r') as f:
                data = json.load(f)
                return data.get('problems', [])
        except FileNotFoundError:
            print("Error: Mainfiles/solved_problems.json not found", file=sys.stderr)
            sys.exit(1)
        except json.JSONDecodeError:
            print("Error: Invalid JSON in Mainfiles/solved_problems.json", file=sys.stderr)
            sys.exit(1)
    
    def select_language(self):
        """Interactive language selection"""
        print("\n=== Select Programming Language ===")
        languages = ["python", "cpp"]
        
        for idx, lang in enumerate(languages, 1):
            print(f"{idx}. {lang.upper()}")
        
        while True:
            try:
                choice = input("\nEnter your choice (1-2): ").strip()
                choice_idx = int(choice) - 1
                
                if 0 <= choice_idx < len(languages):
                    self.selected_language = languages[choice_idx]
                    print(f"Selected: {self.selected_language.upper()}")
                    return
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")
            except KeyboardInterrupt:
                print("\n\nExiting...")
                sys.exit(0)
    
    def select_problem(self):
        """Interactive problem selection"""
        # Filter problems that support the selected language
        available_problems = [
            p for p in self.problems 
            if self.selected_language in p.get('languages', [])
        ]
        
        if not available_problems:
            print(f"No problems available for {self.selected_language.upper()}")
            sys.exit(1)
        
        print(f"\n=== Select Problem ({self.selected_language.upper()}) ===")
        for problem in available_problems:
            problem_id = f"{problem['id']:04d}"
            print(f"{problem['id']}. [{problem_id}] {problem['name']}")
        
        while True:
            try:
                choice = input(f"\nEnter problem number (1-{len(available_problems)}): ").strip()
                choice_num = int(choice)
                
                # Find the problem with this ID
                selected = next((p for p in available_problems if p['id'] == choice_num), None)
                
                if selected:
                    self.selected_problem = selected
                    print(f"Selected: [{selected['id']:04d}] {selected['name']}")
                    return
                else:
                    print(f"Invalid choice. Please enter a number from the list.")
            except ValueError:
                print("Invalid input. Please enter a number.")
            except KeyboardInterrupt:
                print("\n\nExiting...")
                sys.exit(0)
    
    def select_method(self):
        """Interactive method selection"""
        methods = self.selected_problem.get('methods', [])
        
        if not methods:
            print("No methods available for this problem")
            sys.exit(1)
        
        print(f"\n=== Select Method for {self.selected_problem['name']} ===")
        for method in methods:
            print(f"{method['index']}. {method['name']}")
        
        while True:
            try:
                choice = input(f"\nEnter method index (0-{len(methods)-1}): ").strip()
                choice_idx = int(choice)
                
                # Validate the method index exists
                selected_method = next((m for m in methods if m['index'] == choice_idx), None)
                
                if selected_method:
                    self.selected_method = selected_method
                    print(f"Selected: {selected_method['name']}")
                    return
                else:
                    print(f"Invalid choice. Please enter a valid method index.")
            except ValueError:
                print("Invalid input. Please enter a number.")
            except KeyboardInterrupt:
                print("\n\nExiting...")
                sys.exit(0)
    
    def run_solution(self):
        """Execute the selected solution"""
        problem_id = self.selected_problem['id']
        method_idx = self.selected_method['index']
        
        print(f"\n{'='*60}")
        print(f"Running: {self.selected_problem['name']}")
        print(f"Language: {self.selected_language.upper()}")
        print(f"Method: {self.selected_method['name']}")
        print(f"{'='*60}\n")
        
        if self.selected_language == "cpp":
            # Run bash script for C++
            cmd = ["bash", "Mainfiles/run.sh", str(problem_id), str(method_idx)]
        else:  # python
            # Run Python directly
            cmd = ["python3", "Mainfiles/main.py", str(problem_id), str(method_idx)]
        
        try:
            result = subprocess.run(cmd, check=True)
            return result.returncode
        except subprocess.CalledProcessError as e:
            print(f"\nError: Execution failed with exit code {e.returncode}", file=sys.stderr)
            return e.returncode
        except FileNotFoundError:
            print(f"\nError: Could not find the runner script", file=sys.stderr)
            return 1
    
    def run(self):
        """Main interactive flow"""
        print("=" * 60)
        print("LeetCode Solutions Interactive Runner")
        print("=" * 60)
        
        # Step 1: Select language
        self.select_language()
        
        # Step 2: Select problem
        self.select_problem()
        
        # Step 3: Select method
        self.select_method()
        
        # Step 4: Run the solution
        return self.run_solution()

def main():
    runner = InteractiveRunner()
    return runner.run()

if __name__ == "__main__":
    sys.exit(main())
