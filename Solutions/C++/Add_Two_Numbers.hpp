#include "../../config/problem_solver.hpp"

class AddTwoNumbers : public ProblemSolver {
private:
    // Variables
    const string name = "Add Two Numbers";
    const string description = "You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse order, and each of their nodes contains a single digit. Add the two numbers and return the sum as a linked list.";
    const string version = "1.0"; 
    const vector<string> declinations = {"iterative", "recursive"};
    const vector<string> name_desc_ver = {name, description, version};
    const unordered_map<string, string> inputs = {{"l1", "ListNode*"}, {"l2", "ListNode*"}};

    // Methods 

    // The iterative approach to add two numbers represented by linked lists
    ListNode* AddTwoNumbersIterative(ListNode* l1, ListNode* l2) {
        // Implementation of iterative solution
        ListNode* result = new ListNode(0); // Dummy head to remove later and simpliy the code
        ListNode* current = result;
        int carry = 0;
        int curr_sum = 0;
        /**
        This implementation is interesting. This goes back to the idea of
        parsing both linked lists simultaneously, then 
        adding the rest of one of the linked lists if the other is exhausted. 
        Finally, if there's a carry left, we add a new node with that carry value.
        Normally 3 loops would be needed, but we can optimize it to one loop.
        */
        while (l1 != nullptr || l2 != nullptr || carry != 0) {
            int val1 = (l1 != nullptr) ? l1->val : 0; // if l1 is not nullptr we take its value else 0. 
            int val2 = (l2 != nullptr) ? l2->val : 0; // if l2 is not nullptr we take its value else 0.
            curr_sum = val1 + val2 + carry; // The sum of both values and the carry from previous addition
            carry = curr_sum / 10; // Update carry for next addition ( equivalent to python  carry = curr_sum // 10 )
            current->next = new ListNode(curr_sum % 10); // Create new node with the digit value ( equivalent to python curr_sum % 10 )
            current = current->next; // Move to next node always thanks to dummy head
            if (l1) l1 = l1->next;  // Move to next node in l1 if it exists
            if (l2) l2 = l2->next;  // Move to next node in l2 if it exists
        }
        return result->next; // Return the next node of dummy head which is the actual result
    }

    // The recursive approach to add two numbers represented by linked lists
    ListNode* AddTwoNumbersRecursiveHelper(ListNode* l1, ListNode* l2, int carry) {
        // Base case: if both lists are null and no carry, return null
        if (l1 == nullptr && l2 == nullptr && carry == 0) {
            // This is where the recursion ends 
            return nullptr;
        }
        int val1 = (l1 != nullptr) ? l1->val : 0; // Same logic as iterative
        int val2 = (l2 != nullptr) ? l2->val : 0; // Same logic as iterative
        int curr_sum = val1 + val2 + carry;
        carry = curr_sum / 10; // Update carry for next addition ( equivalent to python  carry = curr_sum // 10 )
        ListNode* current = new ListNode(curr_sum % 10);
        current->next = AddTwoNumbersRecursiveHelper(
            (l1 != nullptr) ? l1->next : nullptr,
            (l2 != nullptr) ? l2->next : nullptr,
            carry
        );
        return current;
    }
    ListNode* AddTwoNumbersRecursive(ListNode* l1, ListNode* l2) {
        return AddTwoNumbersRecursiveHelper(l1, l2, 0);
    }

    // Now the main function 
    ListNode* AddTwoNumbersManager(ListNode* l1, ListNode* l2, const string& method) {
        if (method == "iterative") {
            return AddTwoNumbersIterative(l1, l2);
        } else if (method == "recursive") {
            return AddTwoNumbersRecursive(l1, l2);
        } else {
            throw invalid_argument("Invalid method name: " + method);
        }
    }
public:
    // Override the pure virtual function from ProblemSolver
    ProblemResult solve(const json& input, const string& method ) override {
        // Parse input json to get l1 and l2 as ListNode*
        ListNode* l1 = nullptr;
        ListNode* l2 = nullptr;
        // Helper function to convert json array to linked list
        auto jsonToListNode = [](const json& arr) -> ListNode* {
            ListNode* head = nullptr;
            ListNode* current = nullptr;
            for (const auto& val : arr) {
                if (!head) {
                    head = new ListNode(val.get<int>());
                    current = head;
                } else {
                    current->next = new ListNode(val.get<int>());
                    current = current->next;
                }
            }
            return head;
        };
        l1 = jsonToListNode(input["l1"]);
        l2 = jsonToListNode(input["l2"]);
        // l1->print();
        // l2->print();
        ListNode* lres = AddTwoNumbersManager(l1, l2, method);
        // lres->print();
        // Return the ListNode* directly as it's part of ProblemResult variant
        return lres;
    }

    const vector<string>& get_declinations() const override {
        return declinations;
    }

    const vector<string>& get_name_description_version() const override {
        return name_desc_ver;
    }
};