#!/bin/bash

runonly=0
keep_executable=0
problem_id=""
method_index=0

# Function to display help message
show_help() {
  echo "Usage: $0 [OPTIONS] <problem_id> [method_index]"
  echo "  OPTIONS:"
  echo "    --run-only or -re:   Skip the build step and only run the executable (if it exists)."
  echo "    --keep or -k:        Keep the executable after running (don't delete it)."
  echo "  <problem_id>:          The problem ID as an integer (e.g., 1 for problem 0001)."
  echo "  [method_index]:        The method index (default: 0)."
  echo ""
  echo "Examples:"
  echo "  $0 1              # Build and run problem 0001 with method 0, then delete executable"
  echo "  $0 1 1            # Build and run problem 0001 with method 1, then delete executable"
  echo "  $0 --keep 1       # Build and run problem 0001, keep the executable"
  echo "  $0 -re 1          # Run existing executable for problem 0001"
  exit 1
}

# Parse options and arguments
while [ $# -gt 0 ]; do
  case "$1" in
    "--run-only"|-re)
      runonly=1
      shift
      ;;
    "--keep"|-k)
      keep_executable=1
      shift
      ;;
    *)
      if [ -z "$problem_id" ]; then
        problem_id="$1"
        shift
      elif [ "$method_index" -eq 0 ] && [ -n "$1" ]; then
        method_index="$1"
        shift
      else
        echo "Error: Too many arguments."
        show_help
      fi
      ;;
  esac
done

# Check if problem_id was provided
if [ -z "$problem_id" ]; then
  echo "Error: Please provide a problem ID."
  show_help
fi

# Validate that problem_id is a positive integer
if ! [[ "$problem_id" =~ ^[0-9]+$ ]]; then
  echo "Error: problem_id must be a positive integer."
  exit 1
fi

# Validate that method_index is a positive integer
if ! [[ "$method_index" =~ ^[0-9]+$ ]]; then
  echo "Error: method_index must be a positive integer."
  exit 1
fi

# Format problem_id with leading zeros (4 digits)
formatted_id=$(printf "%04d" "$problem_id")

# Get the directory where this script is located
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Create __tmp directory in parent directory if it doesn't exist
tmp_dir="$script_dir/../__tmp"
mkdir -p "$tmp_dir"

cpp_file="$script_dir/main.cpp"
executable_name="__${formatted_id}"
executable_path="${tmp_dir}/${executable_name}"

if [ $runonly -eq 0 ]; then
  echo "Building '$cpp_file' and creating executable '$executable_path'"
  g++ -std=c++17 -Wall "$cpp_file" -o "$executable_path"
  if [ $? -ne 0 ]; then
    echo "Error: Compilation failed."
    exit 1
  fi
else
  echo "Running existing executable '$executable_path'"
fi

# Run the executable
if [ -f "$executable_path" ]; then
  "$executable_path" "$problem_id" "$method_index"
  exit_code=$?
  
  # Clean up executable unless --keep flag is set
  if [ $keep_executable -eq 0 ]; then
    echo "Removing executable '$executable_path'"
    rm "$executable_path"
  else
    echo "Executable kept at '$executable_path'"
  fi
  
  exit $exit_code
else
  if [ $runonly -eq 1 ]; then
    echo "Error: Executable '$executable_path' not found. Cannot run in --run-only mode."
  else
    echo "Error: Executable '$executable_path' not found. Compilation might have failed."
  fi
  exit 1
fi 