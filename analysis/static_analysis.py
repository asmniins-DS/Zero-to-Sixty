"""
Static Analysis Module
Performs AST parsing, complexity scoring, and security scanning
"""

import ast
import json
from typing import Dict, List, Any
from pathlib import Path


class StaticAnalyzer:
    """Analyzes Python code without AI"""

    def __init__(self):
        self.errors = []
        self.warnings = []

    def check_syntax(self, code: str) -> bool:
        """Check if code is valid Python syntax"""
        try:
            ast.parse(code)
            return True
        except SyntaxError as e:
            self.errors.append(f"Syntax Error: {e.msg} at line {e.lineno}")
            return False

    def extract_structure(self, code: str) -> Dict[str, Any]:
        """Extract AST structure: functions, classes, imports"""
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return {"error": "Invalid syntax"}

        structure = {
            "imports": [],
            "functions": [],
            "classes": [],
            "total_lines": len(code.split('\n'))
        }

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    structure["imports"].append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                structure["imports"].append(f"from {node.module}")
            elif isinstance(node, ast.FunctionDef):
                structure["functions"].append({
                    "name": node.name,
                    "args": [arg.arg for arg in node.args.args],
                    "lineno": node.lineno
                })
            elif isinstance(node, ast.ClassDef):
                structure["classes"].append({
                    "name": node.name,
                    "methods": [m.name for m in node.body if isinstance(m, ast.FunctionDef)],
                    "lineno": node.lineno
                })

        return structure

    def calculate_complexity(self, code: str) -> Dict[str, Any]:
        """
        Calculate cyclomatic complexity manually
        Counts: if, elif, else, for, while, and, or, except
        """
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return {"error": "Invalid syntax"}

        complexity_score = 1  # Base complexity

        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.For, ast.While, ast.ExceptHandler)):
                complexity_score += 1
            elif isinstance(node, ast.BoolOp):
                complexity_score += len(node.values) - 1

        # Classify complexity
        if complexity_score <= 5:
            rating = "Low"
        elif complexity_score <= 10:
            rating = "Medium"
        else:
            rating = "High"

        return {
            "complexity_score": complexity_score,
            "rating": rating,
            "recommendation": "Consider refactoring" if rating == "High" else "OK"
        }

    def scan_for_issues(self, code: str) -> Dict[str, List[str]]:
        """Basic issue detection"""
        issues = {
            "potential_bugs": [],
            "code_smells": [],
            "performance_concerns": []
        }

        try:
            tree = ast.parse(code)
        except SyntaxError:
            return {"error": "Invalid syntax"}

        # Check for bare except
        for node in ast.walk(tree):
            if isinstance(node, ast.ExceptHandler):
                if node.type is None:
                    issues["potential_bugs"].append(
                        f"Line {node.lineno}: Bare 'except' clause - catches all exceptions including SystemExit"
                    )

            # Check for unused variables
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        issues["code_smells"].append(
                            f"Potential unused variable: {target.id}"
                        )

            # Check for mutable default arguments
            if isinstance(node, ast.FunctionDef):
                for default in node.args.defaults:
                    if isinstance(default, (ast.List, ast.Dict)):
                        issues["potential_bugs"].append(
                            f"Line {node.lineno}: Mutable default argument in function '{node.name}'"
                        )

        return issues

    def run_full_analysis(self, code: str) -> Dict[str, Any]:
        """Run complete static analysis"""
        return {
            "syntax_valid": self.check_syntax(code),
            "structure": self.extract_structure(code),
            "complexity": self.calculate_complexity(code),
            "issues": self.scan_for_issues(code)
        }
