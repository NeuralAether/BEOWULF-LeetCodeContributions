#include "../../config/common.hpp"
#include "../../config/problem_solver.hpp"

class TwoSum : public ProblemSolver {
private:
    // Variables 
    const string name = "Two Sum";
    const string description = "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.";
    const string version = "1.0"; 
    int order = 1; 
    const vector<string> declinations = {"bruteforce", "hashmap"};
    const vector<string> name_desc_ver = {name, description, version};
    const unordered_map<string, string> inputs = {{"nums", "vector<int>"}, {"target", "int"}};
    // convert inputs to a unorderd map of strings and types 

    // Methods

    vector<int> twoSumBruteForce(const vector<int>& nums, int target) {
        /**
        Params : 
            nums : List[int] : List of integers
            target : int : Target integer
        Returns :
            List[int] : Indices of the two numbers such that they add up to target

        Complexity Analysis :
            Time complexity : O(n^2)
            Space complexity : O(1)

        Complexity Analysis Explanation :
            For each element i in n : We run through n-i. 
            This is equivalent to n + (n-1) + (n-2) + ... + 1 = n(n+1)/2 = O(n^2)
        */
        
        int n = nums.size();
        for (int i = 0; i < n; ++i) {
            for (int j = i + 1; j < n; ++j) {
                if (nums[i] + nums[j] == target) {
                    return {i, j};
                }
            }
        }
        return {};
    }

    vector<int> twoSumHashMap(const vector<int>& nums, int target) {
        /**
        Params : 
            nums : List[int] : List of integers
            target : int : Target integer
        Returns :
            List[int] : Indices of the two numbers such that they add up to target
        Complexity Analysis :
            Time complexity : O(n)
            Space complexity : O(n) # Example of using extra space to save time like in DP

        Complexity Analysis Explanation :
            We traverse the list only once, and each lookup in the hashmap is O(1) on average.
            The lookup for hashmap takes O(1) time on average because it uses a hash function to find the correct bucket (or index) where the value is stored.
            -> Like index lookup in an array.
            */
        unordered_map<int, int> num_to_index;
        for (int i = 0; i < nums.size(); ++i) {
            int remaining = target - nums[i];
            if (num_to_index.find(remaining) != num_to_index.end()) {
                return {num_to_index[remaining], i};
            }
            num_to_index[nums[i]] = i;
        }
        return {};
    }

    vector<int> twoSumManager(const vector<int>& nums, int target, const string& method = "hashmap") {
        if (method == "bruteforce") {
            return twoSumBruteForce(nums, target);
        } else if (method == "hashmap") {
            return twoSumHashMap(nums, target); 
        } else {
            throw invalid_argument("Unknown method: " + method);
        }
    }

public:

    ProblemResult solve(const json& input, const string& method = "hashmap") override {
        // Assuming input is a JSON object with "nums" and "target"
        vector<int> nums = input["nums"].get<vector<int>>();
        int target = input["target"].get<int>();
        return twoSumManager(nums, target, method);
    }
    
    const vector<string>& get_declinations() const override {
        return declinations;
    }

    const vector<string>& get_name_description_version() const override {
        return name_desc_ver;
    }
};