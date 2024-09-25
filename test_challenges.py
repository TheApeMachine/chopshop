# ai_code_assistant/test_challenges.py

CODING_CHALLENGES = [
    {
        "name": "LRU Cache",
        "description": "Implement a Least Recently Used (LRU) cache. It should support the following operations: get and put.",
        "details": """
        get(key) - Get the value (will always be positive) of the key if the key exists in the cache, otherwise return -1.
        put(key, value) - Set or insert the value if the key is not already present. When the cache reached its capacity, it should invalidate the least recently used item before inserting a new item.

        The cache should be O(1) time complexity for both operations.

        You may assume that the input consists of only positive integers.

        Example:
        LRUCache cache = new LRUCache(2); // 2 is the capacity

        cache.put(1, 1);
        cache.put(2, 2);
        cache.get(1);       // returns 1
        cache.put(3, 3);    // evicts key 2
        cache.get(2);       // returns -1 (not found)
        cache.put(4, 4);    // evicts key 1
        cache.get(1);       // returns -1 (not found)
        cache.get(3);       // returns 3
        cache.get(4);       // returns 4
        """
    },
    {
        "name": "Merge K Sorted Lists",
        "description": "Merge k sorted linked lists and return it as one sorted list.",
        "details": """
        You are given an array of k linked-lists lists, each linked-list is sorted in ascending order.
        Merge all the linked-lists into one sorted linked-list and return it.

        Example:
        Input: lists = [[1,4,5],[1,3,4],[2,6]]
        Output: [1,1,2,3,4,4,5,6]
        Explanation: The linked-lists are:
        [
          1->4->5,
          1->3->4,
          2->6
        ]
        Merging them into one sorted list:
        1->1->2->3->4->4->5->6

        Constraints:
        - k == lists.length
        - 0 <= k <= 10^4
        - 0 <= lists[i].length <= 500
        - -10^4 <= lists[i][j] <= 10^4
        - lists[i] is sorted in ascending order.
        - The sum of lists[i].length won't exceed 10^4.
        """
    },
    {
        "name": "Command-line Argument Parser",
        "description": "Implement a command-line argument parser that supports various types of arguments.",
        "details": """
        Create a function or class that can parse command-line arguments with the following features:
        1. Support for boolean flags (e.g., --verbose)
        2. Support for key-value pairs (e.g., --input file.txt)
        3. Support for positional arguments
        4. Support for default values
        5. Basic type validation (int, float, string)
        6. Help message generation

        Example usage:
        parser = ArgumentParser()
        parser.add_argument("--verbose", type=bool, default=False, help="Increase output verbosity")
        parser.add_argument("--input", type=str, required=True, help="Input file name")
        parser.add_argument("--number", type=int, default=42, help="A number")
        parser.add_argument("output", type=str, help="Output file name")

        args = parser.parse_args(["--input", "in.txt", "--verbose", "out.txt"])
        print(args.verbose)  # True
        print(args.input)    # "in.txt"
        print(args.number)   # 42
        print(args.output)   # "out.txt"

        Implement error handling for missing required arguments, invalid types, etc.
        """
    }
]