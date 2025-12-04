#include "common.hpp"

using ProblemResult = variant<
    vector<int>,
    int
>;

class ProblemSolver {
public:
    virtual ~ProblemSolver() = default; 
    virtual ProblemResult solve(const json& input, const string& method ) = 0; 
    virtual const vector<string>& get_declinations() const = 0;
    virtual const vector<string>& get_name_description_version() const = 0;
}; 