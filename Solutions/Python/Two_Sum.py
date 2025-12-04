from config import *

class TwoSum:
    """
    We will see if we can inherit from another class (like a big classification whether a problem is part of a specific group)
    """
    def __init__(self, *args, **kwds):
        self.name = "Two Sum"
        self.description = "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target."
        self.version = "1.0"
        self.order = 1  # Problem number
        self.declinations = ['bruteforce', 'hashmap']  # Different methods to solve the problem
    # First solution O(n^2)
    def __twoSum_bruteforce(self, nums, target):
        """
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
        """
        n = len(nums)
        for i in range(n): # Loops from 0 to n-1
            for j in range(i + 1, n): # Loops from i+1 to n-1
                if nums[i] + nums[j] == target:
                    return [i, j] # The solution requires indices
        return [] # In case there is no solution
    
    def __twoSum_hashmap(self, nums, target):
        """
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
        """
        num_to_index = {} # Hashmap to store number and its index 
        for i, num in enumerate(nums): # Nice pythonic way to get index and value
            remaining = target - num
            if remaining in num_to_index:
                return [num_to_index[remaining], i]
            num_to_index[num] = i
        return [] # In case there is no solution
    
    def __call__(self, nums: List[int], target: int, **kwargs) -> List[int]:
        method = kwargs.get('method', 'hashmap')
        if method not in self.declinations:
            raise ValueError(f"Method '{method}' not recognized. Available methods: {self.declinations}")
        if method == 'bruteforce':
            return self.__twoSum_bruteforce(nums, target)
        else:  # method == 'hashmap'
            return self.__twoSum_hashmap(nums, target)