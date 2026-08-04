import json
from sqlalchemy.orm import Session
from . import models

# Minimal LeetCode-style starter code templates
PYTHON_BOILERPLATE = """import sys

def main():
    # Read input from standard input
    input_str = sys.stdin.read().strip()
    if not input_str:
        return

    # TODO: Write your solution logic here
    pass

if __name__ == '__main__':
    main()"""

CPP_BOILERPLATE = """#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <algorithm>
using namespace std;

int main() {
    // Read input from standard input
    string line;
    if (!getline(cin, line)) return 0;
    
    // TODO: Write your solution logic here

    return 0;
}"""

SAMPLE_QUESTIONS = [
    # --- ARRAYS (4 Questions) ---
    {
        "title": "Two Sum",
        "topic": "arrays",
        "difficulty": "easy",
        "description": "Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to `target` as a space-separated pair `i j` (0-indexed). Assume exactly one solution exists.\n\nInput Format:\nFirst line: space-separated integers for `nums`.\nSecond line: `target` integer.\n\nOutput Format:\nSpace-separated indices `i j`.",
        "starter_code": json.dumps({
            "python": """import sys

def main():
    lines = sys.stdin.read().strip().split('\\n')
    if len(lines) < 2: return
    nums = list(map(int, lines[0].split()))
    target = int(lines[1])
    
    # TODO: Find indices of two numbers that add up to target
    # Print: i j
    pass

if __name__ == '__main__':
    main()""",
            "cpp": """#include <iostream>
#include <vector>
#include <unordered_map>
#include <sstream>
using namespace std;

int main() {
    string line;
    if (!getline(cin, line)) return 0;
    stringstream ss(line);
    vector<int> nums;
    int val, target;
    while (ss >> val) nums.push_back(val);
    cin >> target;
    
    // TODO: Find indices of two numbers that add up to target
    // Output: cout << i << " " << j << endl;

    return 0;
}"""
        }),
        "test_cases": json.dumps([
            {"input": "2 7 11 15\n9", "expected": "0 1"},
            {"input": "3 2 4\n6", "expected": "1 2"},
            {"input": "3 3\n6", "expected": "0 1"}
        ])
    },
    {
        "title": "Maximum Subarray (Kadane's Algorithm)",
        "topic": "arrays",
        "difficulty": "medium",
        "description": "Given an integer array `nums`, find the contiguous subarray (containing at least one number) which has the largest sum and print its sum.\n\nInput Format:\nSpace-separated integers.\n\nOutput Format:\nSingle integer representing maximum subarray sum.",
        "starter_code": json.dumps({
            "python": """import sys

def main():
    input_str = sys.stdin.read().strip()
    if not input_str: return
    nums = list(map(int, input_str.split()))
    
    # TODO: Implement Kadane's Algorithm to find maximum subarray sum
    pass

if __name__ == '__main__':
    main()""",
            "cpp": """#include <iostream>
#include <vector>
#include <sstream>
#include <algorithm>
using namespace std;

int main() {
    string line;
    if (!getline(cin, line)) return 0;
    stringstream ss(line);
    vector<int> nums;
    int val;
    while (ss >> val) nums.push_back(val);
    
    // TODO: Implement Kadane's Algorithm to find maximum subarray sum

    return 0;
}"""
        }),
        "test_cases": json.dumps([
            {"input": "-2 1 -3 4 -1 2 1 -5 4", "expected": "6"},
            {"input": "1", "expected": "1"},
            {"input": "5 4 -1 7 8", "expected": "23"}
        ])
    },
    {
        "title": "Container With Most Water",
        "topic": "arrays",
        "difficulty": "medium",
        "description": "Given an integer array `height` representing vertical lines on a graph, find two lines that together with the x-axis form a container containing the most water. Print the maximum area.\n\nInput Format:\nSpace-separated non-negative integers.",
        "starter_code": json.dumps({
            "python": """import sys

def main():
    heights = list(map(int, sys.stdin.read().split()))
    
    # TODO: Calculate maximum water container area using two-pointers
    pass

if __name__ == '__main__':
    main()""",
            "cpp": """#include <iostream>
#include <vector>
#include <sstream>
#include <algorithm>
using namespace std;

int main() {
    string line;
    getline(cin, line);
    stringstream ss(line);
    vector<int> h;
    int val;
    while (ss >> val) h.push_back(val);
    
    // TODO: Calculate maximum water container area using two-pointers

    return 0;
}"""
        }),
        "test_cases": json.dumps([
            {"input": "1 8 6 2 5 4 8 3 7", "expected": "49"},
            {"input": "1 1", "expected": "1"}
        ])
    },
    {
        "title": "Product of Array Except Self",
        "topic": "arrays",
        "difficulty": "medium",
        "description": "Given an integer array `nums`, return an array `output` such that `output[i]` is equal to the product of all elements of `nums` except `nums[i]` in space-separated format without using division.\n\nInput Format:\nSpace-separated integers.",
        "starter_code": json.dumps({
            "python": """import sys

def main():
    nums = list(map(int, sys.stdin.read().split()))
    
    # TODO: Calculate prefix and suffix products without using division
    pass

if __name__ == '__main__':
    main()""",
            "cpp": """#include <iostream>
#include <vector>
#include <sstream>
using namespace std;

int main() {
    string line;
    getline(cin, line);
    stringstream ss(line);
    vector<int> nums;
    int val;
    while (ss >> val) nums.push_back(val);
    
    // TODO: Calculate prefix and suffix products without using division

    return 0;
}"""
        }),
        "test_cases": json.dumps([
            {"input": "1 2 3 4", "expected": "24 12 8 6"},
            {"input": "-1 1 0 -3 3", "expected": "0 0 9 0 0"}
        ])
    },

    # --- STRINGS (4 Questions) ---
    {
        "title": "Valid Palindrome",
        "topic": "strings",
        "difficulty": "easy",
        "description": "Given a string `s`, return `true` if it is a palindrome considering only alphanumeric characters and ignoring cases, otherwise return `false`.\n\nInput Format:\nA single string line.",
        "starter_code": json.dumps({
            "python": """import sys

def main():
    s = sys.stdin.read().strip()
    
    # TODO: Filter non-alphanumeric characters and check if palindrome
    # Print: true or false
    pass

if __name__ == '__main__':
    main()""",
            "cpp": """#include <iostream>
#include <string>
#include <cctype>
using namespace std;

int main() {
    string s;
    getline(cin, s);
    
    // TODO: Filter non-alphanumeric characters and check if palindrome
    // Output: cout << "true" or "false" << endl;

    return 0;
}"""
        }),
        "test_cases": json.dumps([
            {"input": "A man, a plan, a canal: Panama", "expected": "true"},
            {"input": "race a car", "expected": "false"},
            {"input": " ", "expected": "true"}
        ])
    },
    {
        "title": "Valid Anagram",
        "topic": "strings",
        "difficulty": "easy",
        "description": "Given two strings `s` and `t` on separate lines, print `true` if `t` is an anagram of `s`, and `false` otherwise.",
        "starter_code": json.dumps({
            "python": """import sys

def main():
    lines = sys.stdin.read().strip().split('\\n')
    if len(lines) < 2: return
    s, t = lines[0].strip(), lines[1].strip()
    
    # TODO: Check if t is an anagram of s
    pass

if __name__ == '__main__':
    main()""",
            "cpp": """#include <iostream>
#include <string>
#include <algorithm>
using namespace std;

int main() {
    string s, t;
    if (!(cin >> s >> t)) return 0;
    
    // TODO: Check if t is an anagram of s

    return 0;
}"""
        }),
        "test_cases": json.dumps([
            {"input": "anagram\nagaram", "expected": "true"},
            {"input": "rat\ncar", "expected": "false"}
        ])
    },
    {
        "title": "Longest Substring Without Repeating Characters",
        "topic": "strings",
        "difficulty": "medium",
        "description": "Given a string `s`, find the length of the longest substring without repeating characters.\n\nInput Format:\nSingle line string.",
        "starter_code": json.dumps({
            "python": """import sys

def main():
    s = sys.stdin.read().rstrip('\\r\\n')
    
    # TODO: Sliding window algorithm for longest unique substring
    pass

if __name__ == '__main__':
    main()""",
            "cpp": """#include <iostream>
#include <string>
#include <unordered_map>
#include <algorithm>
using namespace std;

int main() {
    string s;
    getline(cin, s);
    
    // TODO: Sliding window algorithm for longest unique substring

    return 0;
}"""
        }),
        "test_cases": json.dumps([
            {"input": "abcabcbb", "expected": "3"},
            {"input": "bbbbb", "expected": "1"},
            {"input": "pwwkew", "expected": "3"}
        ])
    },
    {
        "title": "Group Anagrams",
        "topic": "strings",
        "difficulty": "medium",
        "description": "Given an array of strings, group the anagrams together. Print the total count of distinct anagram groups.\n\nInput Format:\nSpace-separated strings.",
        "starter_code": json.dumps({
            "python": """import sys

def main():
    words = sys.stdin.read().split()
    
    # TODO: Group anagrams using a Hash Map
    pass

if __name__ == '__main__':
    main()""",
            "cpp": """#include <iostream>
#include <vector>
#include <string>
#include <unordered_map>
#include <algorithm>
#include <sstream>
using namespace std;

int main() {
    string line;
    getline(cin, line);
    stringstream ss(line);
    string word;
    
    // TODO: Group anagrams using a Hash Map

    return 0;
}"""
        }),
        "test_cases": json.dumps([
            {"input": "eat tea tan ate nat bat", "expected": "3"},
            {"input": "a", "expected": "1"}
        ])
    },

    # --- DYNAMIC PROGRAMMING (4 Questions) ---
    {
        "title": "Climbing Stairs",
        "topic": "dp",
        "difficulty": "easy",
        "description": "You are climbing a staircase with `n` steps. Each time you can climb 1 or 2 steps. In how many distinct ways can you climb to the top?\n\nInput Format:\nSingle integer `n`.",
        "starter_code": json.dumps({
            "python": """import sys

def main():
    input_str = sys.stdin.read().strip()
    if not input_str: return
    n = int(input_str)
    
    # TODO: Calculate Fibonacci/DP ways to climb n stairs
    pass

if __name__ == '__main__':
    main()""",
            "cpp": """#include <iostream>
using namespace std;

int main() {
    int n;
    if (!(cin >> n)) return 0;
    
    // TODO: Calculate Fibonacci/DP ways to climb n stairs

    return 0;
}"""
        }),
        "test_cases": json.dumps([
            {"input": "2", "expected": "2"},
            {"input": "3", "expected": "3"},
            {"input": "5", "expected": "8"}
        ])
    },
    {
        "title": "Coin Change",
        "topic": "dp",
        "difficulty": "medium",
        "description": "You are given an integer array `coins` representing coins of different denominations and an integer `amount`. Print the fewest number of coins needed to make up that amount. If impossible, print `-1`.\n\nInput Format:\nFirst line: space-separated coin denominations.\nSecond line: target `amount`.",
        "starter_code": json.dumps({
            "python": """import sys

def main():
    lines = sys.stdin.read().strip().split('\\n')
    if len(lines) < 2: return
    coins = list(map(int, lines[0].split()))
    amount = int(lines[1])
    
    # TODO: Dynamic Programming table for min coin change
    pass

if __name__ == '__main__':
    main()""",
            "cpp": """#include <iostream>
#include <vector>
#include <sstream>
#include <algorithm>
using namespace std;

int main() {
    string line;
    if (!getline(cin, line)) return 0;
    stringstream ss(line);
    vector<int> coins;
    int val, amount;
    while (ss >> val) coins.push_back(val);
    cin >> amount;
    
    // TODO: Dynamic Programming table for min coin change

    return 0;
}"""
        }),
        "test_cases": json.dumps([
            {"input": "1 2 5\n11", "expected": "3"},
            {"input": "2\n3", "expected": "-1"},
            {"input": "1\n0", "expected": "0"}
        ])
    },
    {
        "title": "House Robber",
        "topic": "dp",
        "difficulty": "medium",
        "description": "You are a professional robber planning to rob houses along a street. Adjacent houses have security systems connected. Print the maximum amount of money you can rob without alerting the police.\n\nInput Format:\nSpace-separated integers representing money in each house.",
        "starter_code": json.dumps({
            "python": """import sys

def main():
    nums = list(map(int, sys.stdin.read().split()))
    
    # TODO: Dynamic Programming for non-adjacent house robbery
    pass

if __name__ == '__main__':
    main()""",
            "cpp": """#include <iostream>
#include <vector>
#include <sstream>
#include <algorithm>
using namespace std;

int main() {
    string line;
    getline(cin, line);
    stringstream ss(line);
    vector<int> nums;
    int val;
    while (ss >> val) nums.push_back(val);
    
    // TODO: Dynamic Programming for non-adjacent house robbery

    return 0;
}"""
        }),
        "test_cases": json.dumps([
            {"input": "1 2 3 1", "expected": "4"},
            {"input": "2 7 9 3 1", "expected": "12"}
        ])
    },
    {
        "title": "Longest Increasing Subsequence",
        "topic": "dp",
        "difficulty": "medium",
        "description": "Given an integer array `nums`, return the length of the longest strictly increasing subsequence.\n\nInput Format:\nSpace-separated integers.",
        "starter_code": json.dumps({
            "python": """import sys

def main():
    nums = list(map(int, sys.stdin.read().split()))
    
    # TODO: Longest Increasing Subsequence (DP or Binary Search)
    pass

if __name__ == '__main__':
    main()""",
            "cpp": """#include <iostream>
#include <vector>
#include <sstream>
#include <algorithm>
using namespace std;

int main() {
    string line;
    getline(cin, line);
    stringstream ss(line);
    vector<int> nums;
    int val;
    while (ss >> val) nums.push_back(val);
    
    // TODO: Longest Increasing Subsequence (DP or Binary Search)

    return 0;
}"""
        }),
        "test_cases": json.dumps([
            {"input": "10 9 2 5 3 7 101 18", "expected": "4"},
            {"input": "0 1 0 3 2 3", "expected": "4"},
            {"input": "7 7 7 7 7 7 7", "expected": "1"}
        ])
    },

    # --- GRAPHS (4 Questions) ---
    {
        "title": "Number of Islands",
        "topic": "graphs",
        "difficulty": "medium",
        "description": "Given an `m x n` 2D binary grid map of `'1'`s (land) and `'0'`s (water), count and print the number of islands. An island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically.\n\nInput Format:\nFirst line: `m n` (rows and columns).\nNext `m` lines: `n` space-separated grid characters (1 or 0).",
        "starter_code": json.dumps({
            "python": """import sys

def main():
    lines = sys.stdin.read().strip().split('\\n')
    if not lines or not lines[0]: return
    m, n = map(int, lines[0].split())
    grid = [lines[i+1].split() for i in range(m)]
    
    # TODO: Count connected islands using DFS or BFS
    pass

if __name__ == '__main__':
    main()""",
            "cpp": """#include <iostream>
#include <vector>
using namespace std;

int main() {
    int m, n;
    if (!(cin >> m >> n)) return 0;
    vector<vector<char>> grid(m, vector<char>(n));
    for (int i = 0; i < m; i++)
        for (int j = 0; j < n; j++)
            cin >> grid[i][j];
            
    // TODO: Count connected islands using DFS or BFS

    return 0;
}"""
        }),
        "test_cases": json.dumps([
            {"input": "4 5\n1 1 1 1 0\n1 1 0 1 0\n1 1 0 0 0\n0 0 0 0 0", "expected": "1"},
            {"input": "4 5\n1 1 0 0 0\n1 1 0 0 0\n0 0 1 0 0\n0 0 0 1 1", "expected": "3"}
        ])
    },
    {
        "title": "Course Schedule (Cycle Detection)",
        "topic": "graphs",
        "difficulty": "medium",
        "description": "There are `numCourses` courses labeled `0` to `numCourses-1`. Given prerequisites `[a, b]` meaning to take course `a` you must first take course `b`, print `true` if you can finish all courses, else `false`.\n\nInput Format:\nFirst line: `numCourses` and `numPrerequisites`.\nNext lines: `a b` pairs.",
        "starter_code": json.dumps({
            "python": """import sys

def main():
    lines = sys.stdin.read().strip().split('\\n')
    if not lines or not lines[0]: return
    num_courses, num_prereqs = map(int, lines[0].split())
    
    # TODO: Cycle detection in directed graph (Topological Sort / DFS)
    pass

if __name__ == '__main__':
    main()""",
            "cpp": """#include <iostream>
#include <vector>
using namespace std;

int main() {
    int num_courses, num_prereqs;
    if (!(cin >> num_courses >> num_prereqs)) return 0;
    
    // TODO: Cycle detection in directed graph (Topological Sort / DFS)

    return 0;
}"""
        }),
        "test_cases": json.dumps([
            {"input": "2 1\n1 0", "expected": "true"},
            {"input": "2 2\n1 0\n0 1", "expected": "false"}
        ])
    },
    {
        "title": "Shortest Path in Unweighted Graph (BFS)",
        "topic": "graphs",
        "difficulty": "medium",
        "description": "Given an unweighted graph with `V` vertices (0 to V-1) and `E` edges, find the shortest distance from node `0` to node `V-1`. Print `-1` if unreachable.\n\nInput Format:\nFirst line: `V E`.\nNext `E` lines: `u v` edge pairs.",
        "starter_code": json.dumps({
            "python": """import sys

def main():
    lines = sys.stdin.read().strip().split('\\n')
    if not lines or not lines[0]: return
    V, E = map(int, lines[0].split())
    
    # TODO: BFS shortest path algorithm from node 0 to node V-1
    pass

if __name__ == '__main__':
    main()""",
            "cpp": """#include <iostream>
#include <vector>
#include <queue>
using namespace std;

int main() {
    int V, E;
    if (!(cin >> V >> E)) return 0;
    
    // TODO: BFS shortest path algorithm from node 0 to node V-1

    return 0;
}"""
        }),
        "test_cases": json.dumps([
            {"input": "4 4\n0 1\n1 2\n2 3\n0 3", "expected": "1"},
            {"input": "5 3\n0 1\n1 2\n3 4", "expected": "-1"}
        ])
    },
    {
        "title": "Connected Components in Undirected Graph",
        "topic": "graphs",
        "difficulty": "medium",
        "description": "Given `n` nodes labeled `0` to `n-1` and an edge list, count and print the total number of connected components in the graph.\n\nInput Format:\nFirst line: `n E`.\nNext `E` lines: `u v` edge pairs.",
        "starter_code": json.dumps({
            "python": """import sys

def main():
    lines = sys.stdin.read().strip().split('\\n')
    if not lines or not lines[0]: return
    n, E = map(int, lines[0].split())
    
    # TODO: Disjoint Set Union (DSU) or BFS/DFS connected components
    pass

if __name__ == '__main__':
    main()""",
            "cpp": """#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n, E;
    if (!(cin >> n >> E)) return 0;
    
    // TODO: Disjoint Set Union (DSU) or BFS/DFS connected components

    return 0;
}"""
        }),
        "test_cases": json.dumps([
            {"input": "5 3\n0 1\n1 2\n3 4", "expected": "2"},
            {"input": "5 4\n0 1\n1 2\n2 3\n3 4", "expected": "1"}
        ])
    },

    # --- TREES & LINKED LISTS (4 Questions) ---
    {
        "title": "Invert Binary Tree (Height Calculation)",
        "topic": "trees",
        "difficulty": "easy",
        "description": "Given a binary tree represented as an array in level-order format (where -1 represents NULL), compute and print the maximum height (depth) of the tree.\n\nInput Format:\nSpace-separated integers representing level-order array.",
        "starter_code": json.dumps({
            "python": """import sys

def main():
    nums = list(map(int, sys.stdin.read().split()))
    
    # TODO: Compute maximum height of binary tree from array representation
    pass

if __name__ == '__main__':
    main()""",
            "cpp": """#include <iostream>
#include <vector>
#include <sstream>
using namespace std;

int main() {
    string line;
    getline(cin, line);
    stringstream ss(line);
    vector<int> nums;
    int val;
    while (ss >> val) nums.push_back(val);
    
    // TODO: Compute maximum height of binary tree from array representation

    return 0;
}"""
        }),
        "test_cases": json.dumps([
            {"input": "4 2 7 1 3 6 9", "expected": "3"},
            {"input": "2 1 3", "expected": "2"},
            {"input": "", "expected": "0"}
        ])
    },
    {
        "title": "Reverse a Linked List",
        "topic": "trees",
        "difficulty": "easy",
        "description": "Given the head of a singly linked list represented as space-separated integers, reverse the list and print the space-separated elements of the reversed list.\n\nInput Format:\nSpace-separated integers.",
        "starter_code": json.dumps({
            "python": """import sys

def main():
    nums = sys.stdin.read().split()
    
    # TODO: Reverse elements of the list
    pass

if __name__ == '__main__':
    main()""",
            "cpp": """#include <iostream>
#include <vector>
#include <sstream>
#include <algorithm>
using namespace std;

int main() {
    string line;
    getline(cin, line);
    stringstream ss(line);
    vector<string> nums;
    string val;
    while (ss >> val) nums.push_back(val);
    
    // TODO: Reverse elements of the list

    return 0;
}"""
        }),
        "test_cases": json.dumps([
            {"input": "1 2 3 4 5", "expected": "5 4 3 2 1"},
            {"input": "1 2", "expected": "2 1"}
        ])
    },
    {
        "title": "Validate Binary Search Tree",
        "topic": "trees",
        "difficulty": "medium",
        "description": "Given an array representation of a binary tree in level order (where -1 is NULL), print `true` if it is a valid Binary Search Tree (BST), else `false`.\n\nInput Format:\nSpace-separated integers.",
        "starter_code": json.dumps({
            "python": """import sys

def main():
    nums = list(map(int, sys.stdin.read().split()))
    
    # TODO: Check if level-order array forms a valid BST
    pass

if __name__ == '__main__':
    main()""",
            "cpp": """#include <iostream>
#include <vector>
#include <sstream>
using namespace std;

int main() {
    string line;
    getline(cin, line);
    stringstream ss(line);
    vector<int> nums;
    int val;
    while (ss >> val) nums.push_back(val);
    
    // TODO: Check if level-order array forms a valid BST

    return 0;
}"""
        }),
        "test_cases": json.dumps([
            {"input": "2 1 3", "expected": "true"},
            {"input": "5 1 4 -1 -1 3 6", "expected": "false"}
        ])
    },
    {
        "title": "Lowest Common Ancestor in BST",
        "topic": "trees",
        "difficulty": "medium",
        "description": "Given a Binary Search Tree in level-order array format and two node values `p` and `q`, find the lowest common ancestor (LCA) value.\n\nInput Format:\nFirst line: level-order array values (space-separated).\nSecond line: `p q`.",
        "starter_code": json.dumps({
            "python": """import sys

def main():
    lines = sys.stdin.read().strip().split('\\n')
    if len(lines) < 2: return
    arr = list(map(int, lines[0].split()))
    p, q = map(int, lines[1].split())
    
    # TODO: Find Lowest Common Ancestor (LCA) in BST
    pass

if __name__ == '__main__':
    main()""",
            "cpp": """#include <iostream>
#include <vector>
#include <sstream>
using namespace std;

int main() {
    string line;
    if (!getline(cin, line)) return 0;
    stringstream ss(line);
    vector<int> arr;
    int val, p, q;
    while (ss >> val) arr.push_back(val);
    cin >> p >> q;
    
    // TODO: Find Lowest Common Ancestor (LCA) in BST

    return 0;
}"""
        }),
        "test_cases": json.dumps([
            {"input": "6 2 8 0 4 7 9\n2 8", "expected": "6"},
            {"input": "6 2 8 0 4 7 9\n2 4", "expected": "2"}
        ])
    }
]

def seed_sample_questions(db: Session):
    existing_count = db.query(models.Question).count()
    if existing_count == 0:
        print(f"[Database Seeder] Seeding {len(SAMPLE_QUESTIONS)} DSA questions...")
        for q_data in SAMPLE_QUESTIONS:
            q = models.Question(
                title=q_data["title"],
                topic=q_data["topic"],
                difficulty=q_data["difficulty"],
                description=q_data["description"],
                starter_code=q_data["starter_code"],
                test_cases=q_data["test_cases"]
            )
            db.add(q)
        db.commit()
        print("[Database Seeder] Seeding completed successfully!")
    else:
        # Update existing question starter codes to minimal templates if already seeded!
        questions = db.query(models.Question).all()
        q_map = {q.title: q for q in questions}
        for q_data in SAMPLE_QUESTIONS:
            if q_data["title"] in q_map:
                q_map[q_data["title"]].starter_code = q_data["starter_code"]
        db.commit()
