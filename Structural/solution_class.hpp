#include "../Solutions/C++/Two_Sum.hpp"
#include "../Solutions/C++/Add_Two_Numbers.hpp"

class Solution {
    // Has to take input as a str from list of strs
private: 
    string name = "Base Solution Class";
    string description = "This is the base solution class.";
    string version = "1.0";
    unordered_map<string, shared_ptr<ProblemSolver>> solutions_map ;
    // Helper to format the ID (like your Python logic)
    string format_problem_id(int id) const {
        char buffer[5]; // 4 digits + null terminator
        snprintf(buffer, sizeof(buffer), "%04d", id);
        return string(buffer);
    }

public:
    Solution() {
        solutions_map["0001"] = make_shared<TwoSum>();
        solutions_map["0002"] = make_shared<AddTwoNumbers>();
        // Add more solutions here as needed
    }

    shared_ptr<ProblemSolver> get_solution(const string& problem_id) {
        auto it = solutions_map.find(problem_id);
        if (it == solutions_map.end()) {
            cout << "Solution for problem ID " + problem_id + " not found." << endl;
            return nullptr; // To avoid unnecessary errors
        }
        return it->second;
    }

    shared_ptr<ProblemSolver> get_solution(int problem_id) {
        return get_solution(format_problem_id(problem_id));
    }

    const vector<string>* get_declinations(const string& problem_id) {
        shared_ptr<ProblemSolver> solution_instance = get_solution(problem_id);
        // Downcast to access declinations
        if (!solution_instance) {
            return nullptr;
        }
        return &solution_instance->get_declinations(); // Or throw an exception if declinations are not found
    }
};