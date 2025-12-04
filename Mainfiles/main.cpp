#include "../Runners/run.cpp"

int main(int argc, char* argv[]) {
    if (argc < 3) {
        cerr << "Usage: " << argv[0] << " <problem_id> <method_index>" << endl;
        cerr << "Example: " << argv[0] << " 1 0" << endl;
        return 1;
    }
    
    // Parse and validate problem_id
    int problem_id_int;
    try {
        problem_id_int = stoi(argv[1]);
        if (problem_id_int < 0) {
            cerr << "Error: problem_id must be a positive integer" << endl;
            return 1;
        }
    } catch (const exception& e) {
        cerr << "Error: Invalid problem_id. Must be a positive integer" << endl;
        return 1;
    }
    
    // Parse and validate method_index
    int method_index;
    try {
        method_index = stoi(argv[2]);
        if (method_index < 0) {
            cerr << "Error: method_index must be a positive integer" << endl;
            return 1;
        }
    } catch (const exception& e) {
        cerr << "Error: Invalid method_index. Must be a positive integer" << endl;
        return 1;
    }
    
    // Format problem_id with leading zeros (4 digits)
    string problem_id = to_string(problem_id_int);
    while (problem_id.length() < 4) {
        problem_id = "0" + problem_id;
    }
    
    Runner<string> runner;
    runner.run_eager(problem_id, method_index);
    return 0;
}