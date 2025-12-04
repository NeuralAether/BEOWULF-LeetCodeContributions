#!/bin/bash

echo "Adapted on MacOS default bash shell"

# Colors for better UI
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Global variables
selected_language=""
selected_problem_id=""
selected_problem_name=""
selected_method_idx=""
selected_method_name=""

# Function to convert string to uppercase
to_upper() {
    echo "$1" | tr '[:lower:]' '[:upper:]'
}

# Function to load problems from JSON
load_problems() {
    if [ ! -f "Mainfiles/solved_problems.json" ]; then
        echo -e "${RED}Error: Mainfiles/solved_problems.json not found${NC}" >&2
        exit 1
    fi
    
    # Check if jq is available for JSON parsing
    if ! command -v jq &> /dev/null; then
        echo -e "${RED}Error: jq is required but not installed. Please install jq.${NC}" >&2
        exit 1
    fi
}

# Function to select programming language
select_language() {
    echo ""
    echo "=== Select Programming Language ==="
    echo "1. PYTHON"
    echo "2. CPP"
    
    while true; do
        read -p $'\nEnter your choice (1-2): ' choice
        
        case "$choice" in
            1)
                selected_language="python"
                echo -e "${GREEN}Selected: PYTHON${NC}"
                return 0
                ;;
            2)
                selected_language="cpp"
                echo -e "${GREEN}Selected: CPP${NC}"
                return 0
                ;;
            *)
                echo -e "${RED}Invalid choice. Please try again.${NC}"
                ;;
        esac
    done
}

# Function to select problem
select_problem() {
    # Get problems that support the selected language
    local available_problems=$(jq -c ".problems[] | select(.languages[] | contains(\"$selected_language\"))" Mainfiles/solved_problems.json)
    
    if [ -z "$available_problems" ]; then
        local lang_upper=$(to_upper "$selected_language")
        echo -e "${RED}No problems available for ${lang_upper}${NC}"
        exit 1
    fi
    
    echo ""
    local lang_upper=$(to_upper "$selected_language")
    echo "=== Select Problem (${lang_upper}) ==="
    
    # Display available problems
    while IFS= read -r problem; do
        local id=$(echo "$problem" | jq -r '.id')
        local name=$(echo "$problem" | jq -r '.name')
        printf "%d. [%04d] %s\n" "$id" "$id" "$name"
    done <<< "$available_problems"
    
    while true; do
        read -p $'\nEnter problem number: ' choice
        
        # Validate input is a number
        if ! [[ "$choice" =~ ^[0-9]+$ ]]; then
            echo -e "${RED}Invalid input. Please enter a number.${NC}"
            continue
        fi
        
        # Check if problem with this ID exists and supports the language
        local selected=$(jq -c ".problems[] | select(.id == $choice and (.languages[] | contains(\"$selected_language\")))" Mainfiles/solved_problems.json)
        
        if [ -n "$selected" ]; then
            selected_problem_id="$choice"
            selected_problem_name=$(echo "$selected" | jq -r '.name')
            printf "${GREEN}Selected: [%04d] %s${NC}\n" "$selected_problem_id" "$selected_problem_name"
            return 0
        else
            echo -e "${RED}Invalid choice. Please enter a number from the list.${NC}"
        fi
    done
}

# Function to select method
select_method() {
    # Get methods for the selected problem
    local methods=$(jq -c ".problems[] | select(.id == $selected_problem_id) | .methods[]" Mainfiles/solved_problems.json)
    
    if [ -z "$methods" ]; then
        echo -e "${RED}No methods available for this problem${NC}"
        exit 1
    fi
    
    echo ""
    echo "=== Select Method for $selected_problem_name ==="
    
    # Display available methods
    while IFS= read -r method; do
        local idx=$(echo "$method" | jq -r '.index')
        local name=$(echo "$method" | jq -r '.name')
        echo "$idx. $name"
    done <<< "$methods"
    
    # Get max method index
    local max_idx=$(jq ".problems[] | select(.id == $selected_problem_id) | .methods | length - 1" Mainfiles/solved_problems.json)
    
    while true; do
        read -p $'\nEnter method index (0-'"$max_idx"'): ' choice
        
        # Validate input is a number
        if ! [[ "$choice" =~ ^[0-9]+$ ]]; then
            echo -e "${RED}Invalid input. Please enter a number.${NC}"
            continue
        fi
        
        # Check if method with this index exists
        local selected=$(jq -c ".problems[] | select(.id == $selected_problem_id) | .methods[] | select(.index == $choice)" Mainfiles/solved_problems.json)
        
        if [ -n "$selected" ]; then
            selected_method_idx="$choice"
            selected_method_name=$(echo "$selected" | jq -r '.name')
            echo -e "${GREEN}Selected: $selected_method_name${NC}"
            return 0
        else
            echo -e "${RED}Invalid choice. Please enter a valid method index.${NC}"
        fi
    done
}

# Function to run the solution
run_solution() {
    echo ""
    echo "============================================================"
    echo "Running: $selected_problem_name"
    local lang_upper=$(to_upper "$selected_language")
    echo "Language: ${lang_upper}"
    echo "Method: $selected_method_name"
    echo "============================================================"
    echo ""
    
    if [ "$selected_language" == "cpp" ]; then
        # Format problem_id with leading zeros for executable name
        local formatted_id=$(printf "%04d" "$selected_problem_id")
        local executable_path="__tmp/__${formatted_id}"
        
        local run_only_flag=""
        local keep_flag=""
        
        # Check if executable already exists
        if [ -f "$executable_path" ]; then
            echo -e "${YELLOW}Found existing executable: $executable_path${NC}"
            while true; do
                read -p "Do you want to use the existing executable? (y/n): " use_existing
                case "$use_existing" in
                    [Yy]*)
                        run_only_flag="--run-only"
                        echo -e "${GREEN}Using existing executable${NC}"
                        break
                        ;;
                    [Nn]*)
                        echo -e "${GREEN}Will rebuild the executable${NC}"
                        break
                        ;;
                    *)
                        echo -e "${RED}Please answer y or n${NC}"
                        ;;
                esac
            done
        fi
        
        # Ask if user wants to keep the executable (only if not using existing one)
        if [ -z "$run_only_flag" ]; then
            while true; do
                read -p "Do you want to keep the executable after running? (y/n): " keep_exec
                case "$keep_exec" in
                    [Yy]*)
                        keep_flag="--keep"
                        echo -e "${GREEN}Executable will be kept${NC}"
                        break
                        ;;
                    [Nn]*)
                        echo -e "${GREEN}Executable will be deleted after running${NC}"
                        break
                        ;;
                    *)
                        echo -e "${RED}Please answer y or n${NC}"
                        ;;
                esac
            done
        fi
        
        # Run bash script for C++ with appropriate flags
        bash Mainfiles/run.sh $run_only_flag $keep_flag "$selected_problem_id" "$selected_method_idx"
    else
        # Run Python directly
        python3 Mainfiles/main.py "$selected_problem_id" "$selected_method_idx"
    fi
    
    local exit_code=$?
    
    if [ $exit_code -ne 0 ]; then
        echo -e "\n${RED}Error: Execution failed with exit code $exit_code${NC}" >&2
    fi
    
    return $exit_code
}

# Main function
main() {
    # Trap Ctrl+C to exit gracefully
    trap 'echo -e "\n${YELLOW}Exiting...${NC}"; exit 0' INT
    
    echo "============================================================"
    echo "LeetCode Solutions Interactive Runner"
    echo "============================================================"
    
    # Load and validate JSON file
    load_problems
    
    # Step 1: Select language
    select_language
    
    # Step 2: Select problem
    select_problem
    
    # Step 3: Select method
    select_method
    
    # Step 4: Run the solution
    run_solution
    
    return $?
}

# Run main function
main
exit $?
