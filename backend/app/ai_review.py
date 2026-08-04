import os
import json
from typing import Dict, Any

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

class AIFeedbackModel(BaseModel):
    bugs: list[str] = Field(description="List of detected bugs or logical flaws in the code")
    time_complexity: str = Field(description="Big-O time complexity analysis e.g. O(N log N)")
    space_complexity: str = Field(description="Big-O space complexity analysis e.g. O(1)")
    optimization_tips: list[str] = Field(description="Actionable advice for optimal performance or cleaner code")
    corrected_snippet: str = Field(description="Corrected/Optimized code snippet if bugs exist or optimization is possible")


FEW_SHOT_PROMPT_TEMPLATE = """You are an expert Data Structures & Algorithms (DSA) code reviewer evaluating candidate submissions for placement interviews.

Analyze the candidate's code submission below against the problem requirements and execution test results.
Provide constructive, interview-ready feedback in structured JSON.

--- FEW-SHOT EXAMPLE 1 ---
Problem: Two Sum (Find indices of two numbers that add up to target)
Language: Python
Submitted Code:
def twoSum(nums, target):
    for i in range(len(nums)):
        for j in range(len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]

Execution Status: Passed 4/4 test cases. Runtime: 450ms.
Feedback JSON Output:
{{
  "bugs": ["Double loop allows matching the exact same element twice (e.g. i=0, j=0) when element*2 == target."],
  "time_complexity": "O(N^2)",
  "space_complexity": "O(1)",
  "optimization_tips": [
    "Use a Hash Map to store complement values (target - num) for O(N) linear time lookup.",
    "Start inner loop index at i+1 to avoid checking self-index pairs."
  ],
  "corrected_snippet": "def twoSum(nums, target):\n    seen = {{}}\n    for i, num in enumerate(nums):\n        diff = target - num\n        if diff in seen:\n            return [seen[diff], i]\n        seen[num] = i\n    return []"
}}

--- FEW-SHOT EXAMPLE 2 ---
Problem: Valid Palindrome
Language: C++
Submitted Code:
#include <iostream>
#include <string>
using namespace std;
bool isPalindrome(string s) {{
    int i = 0, j = s.length() - 1;
    while (i < j) {{
        if (s[i] != s[j]) return false;
        i++; j--;
    }}
    return true;
}}

Execution Status: Passed 5/5 test cases. Runtime: 2ms.
Feedback JSON Output:
{{
  "bugs": [],
  "time_complexity": "O(N)",
  "space_complexity": "O(1)",
  "optimization_tips": [
    "Excellent two-pointer implementation operating in linear time and O(1) auxiliary space.",
    "Ensure non-alphanumeric characters and case sensitivity are handled if specified in problem constraints."
  ],
  "corrected_snippet": "bool isPalindrome(string s) {\n    int i = 0, j = s.length() - 1;\n    while (i < j) {\n        if (tolower(s[i]) != tolower(s[j])) return false;\n        i++; j--;\n    }\n    return true;\n}"
}}

--- CURRENT SUBMISSION TO REVIEW ---
Question Title: {title}
Problem Description: {description}
Language: {language}
User Code:
```{language}
{code}
```

Test Results: Passed {passed_count}/{total_tests} test cases. Average Runtime: {runtime_ms} ms.
Error Summary (if any): {errors}

Provide your feedback strictly formatted as valid JSON adhering to this structure:
{{
  "bugs": ["..."],
  "time_complexity": "O(...)",
  "space_complexity": "O(...)",
  "optimization_tips": ["..."],
  "corrected_snippet": "..."
}}
"""


def generate_mock_feedback(code: str, language: str, passed_all: bool, passed_count: int, total_tests: int, runtime_ms: float) -> Dict[str, Any]:
    """
    Fallback deterministic code reviewer that analyzes code structure when OpenAI key is absent.
    """
    code_lower = code.lower()
    bugs = []
    tips = []

    # Detect loops for complexity heuristics
    nested_loops = code_lower.count("for ") > 1 or code_lower.count("while ") > 1
    has_hashmap = "dict" in code_lower or "map" in code_lower or "unordered_map" in code_lower or "set" in code_lower or "seen" in code_lower

    if not passed_all:
        bugs.append(f"Submission failed {total_tests - passed_count} out of {total_tests} test cases. Check boundary conditions and edge cases.")

    if nested_loops and not has_hashmap:
        time_comp = "O(N^2)"
        space_comp = "O(1)"
        tips.append("Consider replacing nested loops with a Hash Map or Two Pointers to reduce time complexity to O(N).")
    elif has_hashmap:
        time_comp = "O(N)"
        space_comp = "O(N)"
        tips.append("Hash Map usage provides efficient O(1) lookups. Watch out for memory overhead on large inputs.")
    else:
        time_comp = "O(N)"
        space_comp = "O(1)"
        tips.append("Clean linear implementation.")

    if passed_all:
        tips.append("All test cases passed! Focus on optimizing code readability and variable naming for interview settings.")
    else:
        tips.append("Review standard edge cases: empty inputs, single element arrays, negative numbers, and boundary limits.")

    return {
        "bugs": bugs,
        "time_complexity": time_comp,
        "space_complexity": space_comp,
        "optimization_tips": tips,
        "corrected_snippet": code if passed_all else f"# Suggested fix for {language}:\n# Ensure edge cases like empty inputs are handled cleanly."
    }


def analyze_code_with_langchain(
    title: str,
    description: str,
    language: str,
    code: str,
    passed_all: bool,
    passed_count: int,
    total_tests: int,
    runtime_ms: float,
    errors: str = ""
) -> Dict[str, Any]:
    """
    LangChain evaluation chain that invokes LLM (OpenAI Chat / Configurable) or falls back to rule engine.
    """
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        # Fallback to local mock analyzer when API key is missing
        return generate_mock_feedback(code, language, passed_all, passed_count, total_tests, runtime_ms)

    try:
        from langchain_openai import ChatOpenAI

        # Flexible model provider (OpenAI default, can switch to Ollama / local via base_url)
        model_name = os.getenv("LLM_MODEL", "gpt-4o-mini")
        base_url = os.getenv("LLM_BASE_URL", None)

        llm = ChatOpenAI(
            model=model_name,
            api_key=api_key,
            base_url=base_url,
            temperature=0.2
        )

        prompt = PromptTemplate.from_template(FEW_SHOT_PROMPT_TEMPLATE)
        chain = prompt | llm | JsonOutputParser()

        formatted_input = {
            "title": title,
            "description": description,
            "language": language,
            "code": code,
            "passed_count": passed_count,
            "total_tests": total_tests,
            "runtime_ms": runtime_ms,
            "errors": errors or "None"
        }

        result = chain.invoke(formatted_input)
        return {
            "bugs": result.get("bugs", []),
            "time_complexity": result.get("time_complexity", "O(N)"),
            "space_complexity": result.get("space_complexity", "O(1)"),
            "optimization_tips": result.get("optimization_tips", []),
            "corrected_snippet": result.get("corrected_snippet", "")
        }
    except Exception as err:
        # Log error & fallback gracefully
        print(f"[LangChain Reviewer Warning] API call failed: {err}. Falling back to mock reviewer.")
        return generate_mock_feedback(code, language, passed_all, passed_count, total_tests, runtime_ms)
