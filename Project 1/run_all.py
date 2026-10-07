"""Run every Project 1 file in order, one at a time, with a clear header for each.

Usage (from inside the Project 1 folder):
    python3 run_all.py
"""

import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent

FILES = [
    ("tesla_inputs.py", "Tesla FY2023-FY2025 inputs and 10-K checks"),
    ("proforma.py", "Five-year three-statement forecast (BASE, DOWNSIDE, UPSIDE)"),
    ("valuation.py", "FCFF DCF, bridge, sensitivity, reverse DCF, scenarios"),
    ("comps.py", "Comparable companies (P/E and EV/EBITDA)"),
    ("known_answer_test.py", "Known-answer test on the course training case"),
    ("failure_tests.py", "Highest-risk failure tests"),
]

PAUSE_SECONDS = 2
results = []

for number, (file_name, description) in enumerate(FILES, start=1):
    print("\n" + "=" * 90)
    print(f"STEP {number} of {len(FILES)}: {file_name} — {description}")
    print("=" * 90 + "\n", flush=True)
    completed = subprocess.run([sys.executable, file_name], cwd=HERE)
    status = "OK" if completed.returncode == 0 else f"ERROR (exit code {completed.returncode})"
    results.append((file_name, status))
    print(f"\n>>> {file_name}: {status}", flush=True)
    time.sleep(PAUSE_SECONDS)

print("\n" + "=" * 90)
print("SUMMARY")
print("=" * 90)
for file_name, status in results:
    print(f"{file_name:<25} {status}")
all_ok = all(status == "OK" for _, status in results)
print("\nALL FILES RAN WITHOUT ERRORS" if all_ok else "\nAT LEAST ONE FILE FAILED — see above")
sys.exit(0 if all_ok else 1)
