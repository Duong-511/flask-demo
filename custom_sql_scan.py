import re
import json
import os

issues = []

patterns = [
    {
        "id": "SQLI001",
        "regex": r'f".*SELECT',
        "message": "SQL Injection via f-string"
    },
    {
        "id": "SQLI002",
        "regex": r'\.format\s*\(',
        "message": "SQL Injection via format()"
    },
    {
        "id": "SQLI003",
        "regex": r'".*%.*"',
        "message": "SQL Injection via % formatting"
    },
    {
        "id": "SQLI004",
        "regex": r'SELECT.*\+\s*\w+',
        "message": "SQL Injection via string concatenation"
    }
]

for root, dirs, files in os.walk("."):
    for file in files:

        if file.endswith(".py") and file != "custom_sql_scan.py":

            path = os.path.join(root, file)

            with open(path, encoding="utf-8") as f:
                lines = f.readlines()

            for lineno, line in enumerate(lines, start=1):

                for rule in patterns:

                    if re.search(rule["regex"], line):

                        issues.append({
                            "engineId": "custom-python-sqli",
                            "ruleId": rule["id"],
                            "primaryLocation": {
                                "message": rule["message"],
                                "filePath": path,
                                "textRange": {
                                    "startLine": lineno
                                }
                            },
                            "type": "VULNERABILITY",
                            "severity": "CRITICAL"
                        })

with open("custom-issues.json", "w") as f:
    json.dump({"issues": issues}, f, indent=4)

print("Found", len(issues), "issues")