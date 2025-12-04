#!/usr/bin/env python3

import sys
import os

# Add parent directory to path to import from Runners
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from Runners.run import PythonRunner

def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <problem_id> <method_index>", file=sys.stderr)
        print(f"Example: {sys.argv[0]} 1 0", file=sys.stderr)
        return 1
    
    # Parse and validate problem_id
    try:
        problem_id_int = int(sys.argv[1])
        if problem_id_int < 0:
            print("Error: problem_id must be a positive integer", file=sys.stderr)
            return 1
    except ValueError:
        print("Error: Invalid problem_id. Must be a positive integer", file=sys.stderr)
        return 1
    
    # Parse and validate method_index
    try:
        method_index = int(sys.argv[2])
        if method_index < 0:
            print("Error: method_index must be a positive integer", file=sys.stderr)
            return 1
    except ValueError:
        print("Error: Invalid method_index. Must be a positive integer", file=sys.stderr)
        return 1
    
    # Format problem_id with leading zeros (4 digits)
    problem_id = f"{problem_id_int:04d}"
    
    runner = PythonRunner()
    runner.run_eager(problem_id, method_index)
    return 0

if __name__ == "__main__":
    sys.exit(main())
