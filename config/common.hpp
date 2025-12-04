#ifndef COMMON_HPP
#define COMMON_HPP

#include <memory>
#include <iostream>
#include <sstream>
#include <fstream>
#include <tuple>
#include <vector>
#include <unordered_map>
#include <string>
#include <stdexcept>
#include <variant>
#include <chrono>
#include "json.hpp" // nlohmann json

using namespace std;
using json = nlohmann::json;
//using namespace json;

struct ListNode {
    int val;
    ListNode *next;
    ListNode() : val(0), next(nullptr) {}
    ListNode(int x) : val(x), next(nullptr) {}
    ListNode(int x, ListNode *next) : val(x), next(next) {}
    public:
    void print() {
        ListNode* current = this;
        while (current != nullptr) {
            cout << current->val;
            if (current->next != nullptr) {
                cout << " -> ";
            }
            current = current->next;
        }
        cout << endl;
    }   
};

#endif // COMMON_HPP