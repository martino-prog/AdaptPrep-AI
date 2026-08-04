import os
import sys
import time
import subprocess
import tempfile
from typing import List, Dict, Any

def run_python_submission(code: str, test_cases: List[Dict[str, str]], timeout_seconds: float = 5.0) -> Dict[str, Any]:
    """
    Executes Python submission code in an isolated subprocess for each test case.
    Captures stdout/stderr, execution time, and pass/fail per test case.
    """
    results = []
    total_time_ms = 0.0
    passed_count = 0

    with tempfile.TemporaryDirectory() as temp_dir:
        script_path = os.path.join(temp_dir, "solution.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(code)

        for idx, tc in enumerate(test_cases, 1):
            input_data = tc.get("input", "")
            expected = tc.get("expected", "").strip()

            start_time = time.perf_counter()
            try:
                proc = subprocess.run(
                    [sys.executable, script_path],
                    input=input_data,
                    text=True,
                    capture_output=True,
                    timeout=timeout_seconds,
                    cwd=temp_dir
                )
                end_time = time.perf_counter()
                elapsed_ms = (end_time - start_time) * 1000.0
                total_time_ms += elapsed_ms

                actual_stdout = proc.stdout.strip()
                actual_stderr = proc.stderr.strip()

                if proc.returncode != 0:
                    results.append({
                        "test_case": idx,
                        "passed": False,
                        "input": input_data,
                        "expected": expected,
                        "actual": actual_stderr or f"Process exited with code {proc.returncode}",
                        "execution_time_ms": round(elapsed_ms, 2),
                        "error": actual_stderr or "Runtime Error"
                    })
                else:
                    passed = (actual_stdout == expected)
                    if passed:
                        passed_count += 1
                    results.append({
                        "test_case": idx,
                        "passed": passed,
                        "input": input_data,
                        "expected": expected,
                        "actual": actual_stdout,
                        "execution_time_ms": round(elapsed_ms, 2),
                        "error": None if passed else f"Output mismatch (Got '{actual_stdout}', Expected '{expected}')"
                    })

            except subprocess.TimeoutExpired:
                end_time = time.perf_counter()
                elapsed_ms = (end_time - start_time) * 1000.0
                results.append({
                    "test_case": idx,
                    "passed": False,
                    "input": input_data,
                    "expected": expected,
                    "actual": "Time Limit Exceeded (> 5 seconds)",
                    "execution_time_ms": round(elapsed_ms, 2),
                    "error": "Time Limit Exceeded"
                })

    avg_runtime = round(total_time_ms / len(test_cases), 2) if test_cases else 0.0
    return {
        "passed_all": (passed_count == len(test_cases)),
        "passed_count": passed_count,
        "total_tests": len(test_cases),
        "avg_runtime_ms": avg_runtime,
        "results": results
    }


def run_cpp_submission(code: str, test_cases: List[Dict[str, str]], timeout_seconds: float = 5.0) -> Dict[str, Any]:
    """
    Compiles and executes C++ submission code using g++ in an isolated temporary directory.
    If g++ is unavailable, returns a descriptive fallback error.
    """
    results = []
    total_time_ms = 0.0
    passed_count = 0

    with tempfile.TemporaryDirectory() as temp_dir:
        cpp_file = os.path.join(temp_dir, "main.cpp")
        exe_file = os.path.join(temp_dir, "main.exe" if os.name == "nt" else "main.out")

        with open(cpp_file, "w", encoding="utf-8") as f:
            f.write(code)

        # Compile with g++
        try:
            compile_proc = subprocess.run(
                ["g++", "-O2", cpp_file, "-o", exe_file],
                capture_output=True,
                text=True,
                timeout=15.0,
                cwd=temp_dir
            )
        except FileNotFoundError:
            # Fallback when g++ compiler is not installed on host machine
            return {
                "passed_all": False,
                "passed_count": 0,
                "total_tests": len(test_cases),
                "avg_runtime_ms": 0.0,
                "results": [{
                    "test_case": i + 1,
                    "passed": False,
                    "input": tc.get("input", ""),
                    "expected": tc.get("expected", ""),
                    "actual": "Compilation Error: g++ compiler not found on host machine. Please install g++ or use Python execution mode.",
                    "execution_time_ms": 0.0,
                    "error": "Compiler Not Available"
                } for i, tc in enumerate(test_cases)]
            }
        except subprocess.TimeoutExpired:
            return {
                "passed_all": False,
                "passed_count": 0,
                "total_tests": len(test_cases),
                "avg_runtime_ms": 0.0,
                "results": [{
                    "test_case": 1,
                    "passed": False,
                    "input": "",
                    "expected": "",
                    "actual": "Compilation Timed Out (> 15s)",
                    "execution_time_ms": 0.0,
                    "error": "Compilation Timeout"
                }]
            }

        if compile_proc.returncode != 0:
            compile_error = compile_proc.stderr.strip() or "C++ Compilation Error"
            return {
                "passed_all": False,
                "passed_count": 0,
                "total_tests": len(test_cases),
                "avg_runtime_ms": 0.0,
                "results": [{
                    "test_case": i + 1,
                    "passed": False,
                    "input": tc.get("input", ""),
                    "expected": tc.get("expected", ""),
                    "actual": compile_error,
                    "execution_time_ms": 0.0,
                    "error": "Compilation Error"
                } for i, tc in enumerate(test_cases)]
            }

        # Run binary for each test case
        for idx, tc in enumerate(test_cases, 1):
            input_data = tc.get("input", "")
            expected = tc.get("expected", "").strip()

            start_time = time.perf_counter()
            try:
                proc = subprocess.run(
                    [exe_file],
                    input=input_data,
                    text=True,
                    capture_output=True,
                    timeout=timeout_seconds,
                    cwd=temp_dir
                )
                end_time = time.perf_counter()
                elapsed_ms = (end_time - start_time) * 1000.0
                total_time_ms += elapsed_ms

                actual_stdout = proc.stdout.strip()
                actual_stderr = proc.stderr.strip()

                if proc.returncode != 0:
                    results.append({
                        "test_case": idx,
                        "passed": False,
                        "input": input_data,
                        "expected": expected,
                        "actual": actual_stderr or f"Process exited with code {proc.returncode}",
                        "execution_time_ms": round(elapsed_ms, 2),
                        "error": actual_stderr or "Runtime Error"
                    })
                else:
                    passed = (actual_stdout == expected)
                    if passed:
                        passed_count += 1
                    results.append({
                        "test_case": idx,
                        "passed": passed,
                        "input": input_data,
                        "expected": expected,
                        "actual": actual_stdout,
                        "execution_time_ms": round(elapsed_ms, 2),
                        "error": None if passed else f"Output mismatch (Got '{actual_stdout}', Expected '{expected}')"
                    })

            except subprocess.TimeoutExpired:
                end_time = time.perf_counter()
                elapsed_ms = (end_time - start_time) * 1000.0
                results.append({
                    "test_case": idx,
                    "passed": False,
                    "input": input_data,
                    "expected": expected,
                    "actual": "Time Limit Exceeded (> 5 seconds)",
                    "execution_time_ms": round(elapsed_ms, 2),
                    "error": "Time Limit Exceeded"
                })

    avg_runtime = round(total_time_ms / len(test_cases), 2) if test_cases else 0.0
    return {
        "passed_all": (passed_count == len(test_cases)),
        "passed_count": passed_count,
        "total_tests": len(test_cases),
        "avg_runtime_ms": avg_runtime,
        "results": results
    }


def execute_submission(language: str, code: str, test_cases: List[Dict[str, str]]) -> Dict[str, Any]:
    """
    Main entrypoint for code execution sandbox routing to Python or C++.
    """
    lang = language.lower().strip()
    if lang in ["python", "py", "python3"]:
        return run_python_submission(code, test_cases)
    elif lang in ["cpp", "c++", "c"]:
        return run_cpp_submission(code, test_cases)
    else:
        raise ValueError(f"Unsupported language '{language}'. Supported languages: 'python', 'cpp'.")
