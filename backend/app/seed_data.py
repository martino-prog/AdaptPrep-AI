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
