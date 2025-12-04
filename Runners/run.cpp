/*
The main classes to run the problem solvers
*/

#include "../Structural/solution_class.hpp"
template <typename T>

class Runner {
    private: 
        Solution solution_instance ; 
        shared_ptr<ProblemSolver> solution_function;
        vector<string> solution_declinations;
        string method_name; 

        void getSolutionFunction(T problem_id) {
            solution_function = solution_instance.get_solution(problem_id);
            if (!solution_function) {
                throw runtime_error("Solution function not found for problem ID: " + problem_id);
            }
        }

        void getSolutionDeclinations(T problem_id) {
            const vector<string>* declinations_ptr = solution_instance.get_declinations(problem_id);
            if (!declinations_ptr || declinations_ptr->empty()) {
                throw runtime_error("Solution declinations not found for problem ID");
            }
            solution_declinations = *declinations_ptr;
        }

        void getMethodName(int method) {
            if (method < 0 || method >= solution_declinations.size()) {
                throw out_of_range("Method index out of range: " + to_string(method));
            }
            method_name = solution_declinations[method];
        }

        string formatProblemId(T problem_id) {
            if constexpr (is_same_v<T, string>) {
                return problem_id;
            } else {
                string problem_id_str = to_string(problem_id);
                while (problem_id_str.length() < 4) {
                    problem_id_str = "0" + problem_id_str;
                }
                return problem_id_str;
            }
        }

        json getTestData(T problem_id) {
            string problem_id_str = formatProblemId(problem_id);
            ifstream file("./TestCases/problem_" + problem_id_str + ".json");
            if (!file.is_open()) {
                throw runtime_error("Could not open test data file for problem ID: " + problem_id_str);
            }
            json data;
            file >> data;
            file.close();
            return data;
        }

        void runTestCase(json& case_data) {
            string description = case_data.value("description", "");
            cout << "Running test case: " << description << endl;
            json expected_output_json = case_data["expected_output"];
            json inputs_json = case_data["inputs"];
            
            ProblemResult actual_output = solution_function->solve(inputs_json, method_name);
            
            // Convert actual_output to json for comparison
            json actual_output_json;
            if (holds_alternative<vector<int>>(actual_output)) {
                actual_output_json = get<vector<int>>(actual_output);
            } else if (holds_alternative<int>(actual_output)) {
                actual_output_json = get<int>(actual_output);
            }
            
            if (actual_output_json != expected_output_json) {
                cout << "Test failed for case: " << description << ". Expected " << expected_output_json.dump() << ", got " << actual_output_json.dump() << endl;
            } else {
                cout << "Description : " << description << ", Input : " << inputs_json.dump() << ", Expected Output : " << expected_output_json.dump() << endl;
                cout << "Result: " << actual_output_json.dump() << " -> Test Passed!" << endl;
            }
        }

    public:
        Runner() {
            solution_instance = Solution();
            solution_function = nullptr;    
        }

        void run_eager(T problem_id, int method_index) {
            getSolutionFunction(problem_id);
            getSolutionDeclinations(problem_id);
            getMethodName(method_index);
            cout << "Running tests for problem ID: " << problem_id << " using method: " << method_name << endl;
            cout << "Problem Description: " << solution_function->get_name_description_version()[1] << endl;
            cout << "---------------------------------------------------" << endl;
            
            auto start_time = chrono::high_resolution_clock::now();
            json data = getTestData(problem_id);
            json base = data.value("Base", json::array());
            cout << "------ Testing the solution with Base data ------" << endl;
            for (auto& case_data : base) {
                runTestCase(case_data);
            }
            json edge = data.value("Edge", json::array());
            cout << "------ Testing the solution with Edge data ------" << endl;
            for (auto& case_data : edge) {
                runTestCase(case_data);
            }
            auto end_time = chrono::high_resolution_clock::now();
            auto duration = chrono::duration_cast<chrono::milliseconds>(end_time - start_time).count();
            cout << "All Test Cases Passed! Total execution time: " << duration << " ms" << endl;
        }  
};

