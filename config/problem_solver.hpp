#ifndef PROBLEM_SOLVER_HPP
#define PROBLEM_SOLVER_HPP

#include "common.hpp"

using ProblemResult = variant<
    vector<int>,
    int,
    ListNode*
>;

class ProblemSolver {
public:
    virtual ~ProblemSolver() = default; 
    virtual ProblemResult solve(const json& input, const string& method ) = 0; 
    virtual const vector<string>& get_declinations() const = 0;
    virtual const vector<string>& get_name_description_version() const = 0;
}; 

#endif 