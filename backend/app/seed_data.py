import json
from sqlalchemy.orm import Session
from . import models

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
    
    seen = {}
    for i, num in enumerate(nums):
        diff = target - num
        if diff in seen:
            print(f"{seen[diff]} {i}")
            return
        seen[num] = i

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
    
    unordered_map<int, int> seen;
    for (int i = 0; i < nums.size(); i++) {
        int diff = target - nums[i];
        if (seen.count(diff)) {
            cout << seen[diff] << " " << i << endl;
            return 0;
        }
        seen[nums[i]] = i;
    }
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
    
    max_sum = current_sum = nums[0]
    for x in nums[1:]:
        current_sum = max(x, current_sum + x)
        max_sum = max(max_sum, current_sum)
    print(max_sum)

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
    
    int max_sum = nums[0], curr_sum = nums[0];
    for (size_t i = 1; i < nums.size(); i++) {
        curr_sum = max(nums[i], curr_sum + nums[i]);
        max_sum = max(max_sum, curr_sum);
    }
    cout << max_sum << endl;
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
    l, r = 0, len(heights) - 1
    max_area = 0
    while l < r:
        area = min(heights[l], heights[r]) * (r - l)
        max_area = max(max_area, area)
        if heights[l] < heights[r]: l += 1
        else: r -= 1
    print(max_area)

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
    int l = 0, r = h.size() - 1, max_area = 0;
    while (l < r) {
        int area = min(h[l], h[r]) * (r - l);
        max_area = max(max_area, area);
        if (h[l] < h[r]) l++; else r--;
    }
    cout << max_area << endl;
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
    n = len(nums)
    res = [1] * n
    prefix = 1
    for i in range(n):
        res[i] = prefix
        prefix *= nums[i]
    suffix = 1
    for i in range(n - 1, -1, -1):
        res[i] *= suffix
        suffix *= nums[i]
    print(' '.join(map(str, res)))

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
    int n = nums.size();
    vector<int> res(n, 1);
    int prefix = 1;
    for (int i = 0; i < n; i++) {
        res[i] = prefix;
        prefix *= nums[i];
    }
    int suffix = 1;
    for (int i = n - 1; i >= 0; i--) {
        res[i] *= suffix;
        suffix *= nums[i];
    }
    for (int i = 0; i < n; i++) cout << res[i] << (i == n - 1 ? "" : " ");
    cout << endl;
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
    filtered = [ch.lower() for ch in s if ch.isalnum()]
    print('true' if filtered == filtered[::-1] else 'false')

if __name__ == '__main__':
    main()""",
            "cpp": """#include <iostream>
#include <string>
#include <cctype>
using namespace std;

int main() {
    string s;
    getline(cin, s);
    string filtered = "";
    for (char c : s) if (isalnum(c)) filtered += tolower(c);
    string rev = string(filtered.rbegin(), filtered.rend());
    cout << (filtered == rev ? "true" : "false") << endl;
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
from collections import Counter

def main():
    lines = sys.stdin.read().strip().split('\\n')
    if len(lines) < 2: return
    s, t = lines[0].strip(), lines[1].strip()
    print('true' if Counter(s) == Counter(t) else 'false')

if __name__ == '__main__':
    main()""",
            "cpp": """#include <iostream>
#include <string>
#include <algorithm>
using namespace std;

int main() {
    string s, t;
    if (!(cin >> s >> t)) return 0;
    sort(s.begin(), s.end());
    sort(t.begin(), t.end());
    cout << (s == t ? "true" : "false") << endl;
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
    seen = {}
    start = max_len = 0
    for i, ch in enumerate(s):
        if ch in seen and seen[ch] >= start:
            start = seen[ch] + 1
        seen[ch] = i
        max_len = max(max_len, i - start + 1)
    print(max_len)

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
    unordered_map<char, int> seen;
    int start = 0, max_len = 0;
    for (int i = 0; i < s.length(); i++) {
        if (seen.count(s[i]) && seen[s[i]] >= start) {
            start = seen[s[i]] + 1;
        }
        seen[s[i]] = i;
        max_len = max(max_len, i - start + 1);
    }
    cout << max_len << endl;
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
from collections import defaultdict

def main():
    words = sys.stdin.read().split()
    groups = defaultdict(list)
    for w in words:
        key = ''.join(sorted(w))
        groups[key].append(w)
    print(len(groups))

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
    unordered_map<string, int> groups;
    while (ss >> word) {
        string key = word;
        sort(key.begin(), key.end());
        groups[key]++;
    }
    cout << groups.size() << endl;
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
    if n <= 2:
        print(n)
        return
    a, b = 1, 2
    for _ in range(3, n + 1):
        a, b = b, a + b
    print(b)

if __name__ == '__main__':
    main()""",
            "cpp": """#include <iostream>
using namespace std;

int main() {
    int n;
    if (!(cin >> n)) return 0;
    if (n <= 2) { cout << n << endl; return 0; }
    int a = 1, b = 2;
    for (int i = 3; i <= n; i++) {
        int temp = a + b;
        a = b;
        b = temp;
    }
    cout << b << endl;
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
    
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for coin in coins:
        for i in range(coin, amount + 1):
            dp[i] = min(dp[i], dp[i - coin] + 1)
    print(dp[amount] if dp[amount] != float('inf') else -1)

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
    
    vector<int> dp(amount + 1, amount + 1);
    dp[0] = 0;
    for (int coin : coins) {
        for (int i = coin; i <= amount; i++) {
            dp[i] = min(dp[i], dp[i - coin] + 1);
        }
    }
    cout << (dp[amount] > amount ? -1 : dp[amount]) << endl;
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
    if not nums: return
    prev1 = prev2 = 0
    for num in nums:
        temp = max(prev1, prev2 + num)
        prev2 = prev1
        prev1 = temp
    print(prev1)

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
    int prev1 = 0, prev2 = 0;
    for (int num : nums) {
        int temp = max(prev1, prev2 + num);
        prev2 = prev1;
        prev1 = temp;
    }
    cout << prev1 << endl;
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
import bisect

def main():
    nums = list(map(int, sys.stdin.read().split()))
    if not nums: return
    tails = []
    for x in nums:
        idx = bisect.bisect_left(tails, x)
        if idx == len(tails): tails.append(x)
        else: tails[idx] = x
    print(len(tails))

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
    vector<int> tails;
    for (int x : nums) {
        auto it = lower_bound(tails.begin(), tails.end(), x);
        if (it == tails.end()) tails.push_back(x);
        else *it = x;
    }
    cout << tails.size() << endl;
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
    
    islands = 0
    def dfs(r, c):
        if r < 0 or r >= m or c < 0 or c >= n or grid[r][c] == '0':
            return
        grid[r][c] = '0'
        dfs(r+1, c); dfs(r-1, c); dfs(r, c+1); dfs(r, c-1)

    for r in range(m):
        for c in range(n):
            if grid[r][c] == '1':
                islands += 1
                dfs(r, c)
    print(islands)

if __name__ == '__main__':
    main()""",
            "cpp": """#include <iostream>
#include <vector>
using namespace std;

void dfs(vector<vector<char>>& grid, int r, int c, int m, int n) {
    if (r < 0 || r >= m || c < 0 || c >= n || grid[r][c] == '0') return;
    grid[r][c] = '0';
    dfs(grid, r+1, c, m, n);
    dfs(grid, r-1, c, m, n);
    dfs(grid, r, c+1, m, n);
    dfs(grid, r, c-1, m, n);
}

int main() {
    int m, n;
    if (!(cin >> m >> n)) return 0;
    vector<vector<char>> grid(m, vector<char>(n));
    for (int i = 0; i < m; i++)
        for (int j = 0; j < n; j++)
            cin >> grid[i][j];
    int islands = 0;
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            if (grid[i][j] == '1') {
                islands++;
                dfs(grid, i, j, m, n);
            }
        }
    }
    cout << islands << endl;
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
from collections import defaultdict

def main():
    lines = sys.stdin.read().strip().split('\\n')
    if not lines or not lines[0]: return
    num_courses, num_prereqs = map(int, lines[0].split())
    adj = defaultdict(list)
    for i in range(1, num_prereqs + 1):
        if i < len(lines):
            u, v = map(int, lines[i].split())
            adj[v].append(u)
    
    state = [0] * num_courses
    def has_cycle(u):
        if state[u] == 1: return True
        if state[u] == 2: return False
        state[u] = 1
        for v in adj[u]:
            if has_cycle(v): return True
        state[u] = 2
        return False

    for c in range(num_courses):
        if state[c] == 0 and has_cycle(c):
            print('false')
            return
    print('true')

if __name__ == '__main__':
    main()""",
            "cpp": """#include <iostream>
#include <vector>
using namespace std;

bool dfs(int u, vector<vector<int>>& adj, vector<int>& state) {
    if (state[u] == 1) return true;
    if (state[u] == 2) return false;
    state[u] = 1;
    for (int v : adj[u]) if (dfs(v, adj, state)) return true;
    state[u] = 2;
    return false;
}

int main() {
    int num_courses, num_prereqs;
    if (!(cin >> num_courses >> num_prereqs)) return 0;
    vector<vector<int>> adj(num_courses);
    for (int i = 0; i < num_prereqs; i++) {
        int u, v;
        cin >> u >> v;
        adj[v].push_back(u);
    }
    vector<int> state(num_courses, 0);
    for (int i = 0; i < num_courses; i++) {
        if (state[i] == 0 && dfs(i, adj, state)) {
            cout << "false" << endl;
            return 0;
        }
    }
    cout << "true" << endl;
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
from collections import deque, defaultdict

def main():
    lines = sys.stdin.read().strip().split('\\n')
    if not lines or not lines[0]: return
    V, E = map(int, lines[0].split())
    adj = defaultdict(list)
    for i in range(1, E + 1):
        if i < len(lines):
            u, v = map(int, lines[i].split())
            adj[u].append(v); adj[v].append(u)

    dist = [-1] * V
    dist[0] = 0
    q = deque([0])
    while q:
        curr = q.popleft()
        if curr == V - 1:
            print(dist[curr])
            return
        for nxt in adj[curr]:
            if dist[nxt] == -1:
                dist[nxt] = dist[curr] + 1
                q.append(nxt)
    print(dist[V - 1])

if __name__ == '__main__':
    main()""",
            "cpp": """#include <iostream>
#include <vector>
#include <queue>
using namespace std;

int main() {
    int V, E;
    if (!(cin >> V >> E)) return 0;
    vector<vector<int>> adj(V);
    for (int i = 0; i < E; i++) {
        int u, v;
        cin >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u);
    }
    vector<int> dist(V, -1);
    dist[0] = 0;
    queue<int> q;
    q.push(0);
    while (!q.empty()) {
        int curr = q.front(); q.pop();
        for (int nxt : adj[curr]) {
            if (dist[nxt] == -1) {
                dist[nxt] = dist[curr] + 1;
                q.push(nxt);
            }
        }
    }
    cout << dist[V - 1] << endl;
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
    parent = list(range(n))
    
    def find(i):
        if parent[i] == i: return i
        parent[i] = find(parent[i])
        return parent[i]
        
    def union(i, j):
        root_i, root_j = find(i), find(j)
        if root_i != root_j:
            parent[root_i] = root_j
            return True
        return False

    components = n
    for i in range(1, E + 1):
        if i < len(lines):
            u, v = map(int, lines[i].split())
            if union(u, v): components -= 1
    print(components)

if __name__ == '__main__':
    main()""",
            "cpp": """#include <iostream>
#include <vector>
using namespace std;

int find_set(int i, vector<int>& parent) {
    if (parent[i] == i) return i;
    return parent[i] = find_set(parent[i], parent);
}

int main() {
    int n, E;
    if (!(cin >> n >> E)) return 0;
    vector<int> parent(n);
    for (int i = 0; i < n; i++) parent[i] = i;
    int comp = n;
    for (int i = 0; i < E; i++) {
        int u, v;
        cin >> u >> v;
        int r1 = find_set(u, parent), r2 = find_set(v, parent);
        if (r1 != r2) { parent[r1] = r2; comp--; }
    }
    cout << comp << endl;
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

def get_depth(arr, idx):
    if idx >= len(arr) or arr[idx] == -1:
        return 0
    return 1 + max(get_depth(arr, 2 * idx + 1), get_depth(arr, 2 * idx + 2))

def main():
    nums = list(map(int, sys.stdin.read().split()))
    if not nums: return
    print(get_depth(nums, 0))

if __name__ == '__main__':
    main()""",
            "cpp": """#include <iostream>
#include <vector>
#include <sstream>
#include <algorithm>
using namespace std;

int get_depth(const vector<int>& arr, int idx) {
    if (idx >= arr.size() || arr[idx] == -1) return 0;
    return 1 + max(get_depth(arr, 2 * idx + 1), get_depth(arr, 2 * idx + 2));
}

int main() {
    string line;
    getline(cin, line);
    stringstream ss(line);
    vector<int> nums;
    int val;
    while (ss >> val) nums.push_back(val);
    cout << get_depth(nums, 0) << endl;
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
    print(' '.join(reversed(nums)))

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
    reverse(nums.begin(), nums.end());
    for (size_t i = 0; i < nums.size(); i++)
        cout << nums[i] << (i + 1 == nums.size() ? "" : " ");
    cout << endl;
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

def is_valid_bst(arr, idx, min_val, max_val):
    if idx >= len(arr) or arr[idx] == -1:
        return True
    val = arr[idx]
    if val <= min_val or val >= max_val:
        return False
    return (is_valid_bst(arr, 2*idx+1, min_val, val) and 
            is_valid_bst(arr, 2*idx+2, val, max_val))

def main():
    nums = list(map(int, sys.stdin.read().split()))
    if not nums:
        print('true')
        return
    print('true' if is_valid_bst(nums, 0, float('-inf'), float('inf')) else 'false')

if __name__ == '__main__':
    main()""",
            "cpp": """#include <iostream>
#include <vector>
#include <sstream>
#include <climits>
using namespace std;

bool validate(const vector<int>& arr, int idx, long long min_val, long long max_val) {
    if (idx >= arr.size() || arr[idx] == -1) return true;
    long long val = arr[idx];
    if (val <= min_val || val >= max_val) return false;
    return validate(arr, 2*idx+1, min_val, val) && validate(arr, 2*idx+2, val, max_val);
}

int main() {
    string line;
    getline(cin, line);
    stringstream ss(line);
    vector<int> nums;
    int val;
    while (ss >> val) nums.push_back(val);
    cout << (validate(nums, 0, LLONG_MIN, LLONG_MAX) ? "true" : "false") << endl;
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
    
    idx = 0
    while idx < len(arr) and arr[idx] != -1:
        val = arr[idx]
        if p < val and q < val:
            idx = 2 * idx + 1
        elif p > val and q > val:
            idx = 2 * idx + 2
        else:
            print(val)
            return

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
    
    int idx = 0;
    while (idx < arr.size() && arr[idx] != -1) {
        int curr = arr[idx];
        if (p < curr && q < curr) idx = 2 * idx + 1;
        else if (p > curr && q > curr) idx = 2 * idx + 2;
        else { cout << curr << endl; return 0; }
    }
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
