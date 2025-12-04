from config import *

class AddTwoNumber:
    """
    We will see if we can inherit from another class (like a big classification whether a problem is part of a specific group)
    """
    def __init__(self, *args, **kwds):
        self.name = "Add Two Numbers"
        self.description = "You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse order, and each of their nodes contains a single digit. Add the two numbers and return the sum as a linked list."
        self.version = "1.0"
        self.declinations = ['iterative', 'recursive']  # Different methods to solve the problem

    def __iterative_add_two_numbers(self, l1: ListNode, l2: ListNode) -> ListNode:
        """
        Params : 
            l1 : ListNode : First linked list representing a non-negative integer
            l2 : ListNode : Second linked list representing a non-negative integer
        Returns :
            ListNode : Linked list representing the sum of the two integers

        Complexity Analysis :
            Time complexity : O(max(m, n))
            Space complexity : O(max(m, n))

        Complexity Analysis Explanation :
            We traverse both linked lists once, where m and n are the lengths of the two linked lists.
            At each iteration, we perform constant time operations and advance both pointers. 
            When one list is longer, we continue processing the remaining nodes of the longer list. 
            If the carry is non-zero after processing both lists, we add an additional node to the result.
            So basically the amount of operations (if considering the sum to be C) is (max(m, n) + 1)*C which is O(max(m, n))
        """
        result = ListNode(0) # Dummy head
        current = result
        carry = 0
        curr_sum = 0 
        while l1 or l2 or carry:
            val1 = l1.val if l1 else 0
            val2 = l2.val if l2 else 0
            curr_sum = val1 + val2 + carry
            carry = curr_sum // 10
            current.next = ListNode(curr_sum % 10)
            current = current.next
            if l1:
                l1 = l1.next
            if l2:
                l2 = l2.next
        return result.next

    def __recursive_add_two_numbers(self, l1: ListNode, l2: ListNode) -> ListNode:
        """
        Params : 
            l1 : ListNode : First linked list representing a non-negative integer
            l2 : ListNode : Second linked list representing a non-negative integer
        Returns :
            ListNode : Linked list representing the sum of the two integers
        Complexity Analysis :
            Time complexity : O(max(m, n))
            Space complexity : O(max(m, n))
        Complexity Analysis Explanation :
           Look at the sub function below
        """

        def recursive_add_two_numbers_helper(l1, l2, carry):
            """
            Params :
                l1 : ListNode : First linked list node
                l2 : ListNode : Second linked list node
                carry : int : Carry from previous addition
            Returns :
                ListNode : Resultant linked list node
            Complexity Analysis :
                Time complexity : O(max(m, n))
                Space complexity : O(max(m, n))
            Complexity Analysis Explanation :
                The base case occurs when both l1 and l2 are None and carry is 0, leading to O(1) time and space.
                In each recursive call, we process one node from either l1 or l2 (or both) and make a recursive call for the next nodes.
                Process(n,m) = Process(n-1,m-1) + O(1) 
                Let us say that m = n +k where k >= 0 as we can always assume that l2 is the longer list (if not we can swap them)
                Process(n,n+k) = Process(n-1,n-1+k) + O(1) .. = Process(n-2,n-2+k) + 2*O(1) ... = Process(0,k) + n*O(1). 
                Now Process(0,k) = Process(0,k-1) + O(1) ... = Process(0,0) + k*O(1) = O(1) + k*O(1) = k*O(1)
                Therefore total time complexity = (n+k)*O(1) = O(n+k) = O(max(m,n))
                Each recursive call adds a new frame to the call stack, leading to O(max(m, n)) space complexity in the worst case. 
            """
            if not l1 and not l2 and carry == 0:
                return None
            val1 = l1.val if l1 else 0
            val2 = l2.val if l2 else 0
            curr_sum = val1 + val2 + carry
            new_carry = curr_sum // 10
            node = ListNode(curr_sum % 10)
            node.next = recursive_add_two_numbers_helper(l1.next if l1 else None,
                                                        l2.next if l2 else None,
                                                        new_carry)
            return node
        return recursive_add_two_numbers_helper(l1, l2, 0)

    def __list_to_linked_list(self, lst: List[int]) -> ListNode:
        """Helper function to convert a list to a linked list"""
        dummy = ListNode(0)
        current = dummy
        for value in lst:
            current.next = ListNode(value)
            current = current.next
        return dummy.next
    
    def __linked_list_to_list(self, node: ListNode) -> List[int]:
        """Helper function to convert a linked list to a list"""
        result = []
        while node:
            result.append(node.val)
            node = node.next
        return result
    
    def __call__(self, l1: List[int], l2: List[int], **kwargs) -> List[int]:
        l1 = self.__list_to_linked_list(l1)
        l2 = self.__list_to_linked_list(l2)
        method = kwargs.get('method', 'recursive')
        if method not in self.declinations:
            raise ValueError(f"Method '{method}' not recognized. Available methods: {self.declinations}")
        if method == 'iterative':
            return self.__linked_list_to_list(self.__iterative_add_two_numbers(l1, l2))
        else:  # method == 'recursive'
            return self.__linked_list_to_list(self.__recursive_add_two_numbers(l1, l2))