"""
Gemini AI Agent for Code Review
Interacts with Google Gemini API to provide intelligent code feedback
"""

import json
import os
from typing import Dict, Any, Optional

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = lambda: None

# Load environment variables
load_dotenv()

try:
    import google.generativeai as genai
except ImportError:
    genai = None


class GeminiAgent:
    """AI-powered code review agent using Google Gemini"""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize Gemini agent with API key"""
        if genai is None:
            raise ImportError("google-generativeai not installed. Run: pip install google-generativeai")

        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")

        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel("gemini-pro")

    def generate_review(self, code: str, static_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate AI-powered code review
        
        Args:
            code: Python code snippet to review
            static_analysis: Results from static analysis
            
        Returns:
            Structured review with bugs, inefficiencies, security issues, and improvements
        """

        analysis_summary = json.dumps(static_analysis, indent=2)

        prompt = f"""You are an expert Python code reviewer with 10+ years of experience. 
Your task is to review the following Python code and provide constructive feedback.

CODE TO REVIEW:
```python
{code}
```

STATIC ANALYSIS RESULTS:
{analysis_summary}

Please analyze the code and provide:

1. **BUGS** - Critical issues that will cause crashes or incorrect behavior
2. **INEFFICIENCIES** - Code that works but could be optimized or simplified
3. **SECURITY RISKS** - Potential security vulnerabilities
4. **IMPROVEMENTS** - Suggested refactoring with explanations

Format your response as JSON with this structure:
{{
    "bugs": [
        {{"issue": "description", "severity": "critical/high/medium", "line": "approximate line", "fix": "suggested fix"}}
    ],
    "inefficiencies": [
        {{"issue": "description", "impact": "performance/readability/maintainability", "suggestion": "how to improve"}}
    ],
    "security_issues": [
        {{"issue": "description", "risk_level": "critical/high/medium", "recommendation": "what to do"}}
    ],
    "improvements": [
        {{"current": "current code pattern", "improved": "improved pattern", "reason": "why this is better", "example": "code example"}}
    ],
    "summary": "Brief overall assessment",
    "score": "rating out of 10"
}}

Be specific, actionable, and focus on the most impactful issues first."""

        try:
            response = self.model.generate_content(prompt)
            response_text = response.text

            # Try to parse as JSON
            try:
                # Find JSON in response (model might add extra text)
                start_idx = response_text.find('{')
                end_idx = response_text.rfind('}') + 1
                if start_idx >= 0 and end_idx > start_idx:
                    json_str = response_text[start_idx:end_idx]
                    review = json.loads(json_str)
                else:
                    review = {"raw_response": response_text}
            except json.JSONDecodeError:
                review = {"raw_response": response_text}

            return review

        except Exception as e:
            return {
                "error": f"Gemini API error: {str(e)}",
                "raw_response": str(e)
            }

    def generate_documentation(self, code: str, parsed_structure: Dict[str, Any]) -> str:
        """
        Generate Google-style docstrings for functions and classes
        
        Args:
            code: Python code snippet
            parsed_structure: AST structure from static analysis
            
        Returns:
            Generated documentation as string
        """

        structure_summary = json.dumps(parsed_structure, indent=2)

        prompt = f"""You are a Python documentation expert. 
Generate comprehensive Google-style docstrings for the following code.

CODE:
```python
{code}
```

STRUCTURE:
{structure_summary}

Generate docstrings in Google format with:
- Brief description
- Args: (with types)
- Returns: (with type)
- Raises: (if applicable)
- Examples: (where helpful)

Return ONLY the documented code with docstrings added, no explanations."""

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating documentation: {str(e)}"

    def generate_refactored_code(self, code: str, issue_highlights: List[str]) -> str:
        """
        Generate refactored version of code addressing key issues
        
        Args:
            code: Original Python code
            issue_highlights: List of key issues to address
            
        Returns:
            Refactored code
        """

        issues_text = "\n".join(f"- {issue}" for issue in issue_highlights)

        prompt = f"""You are an expert Python refactoring specialist.
Refactor the following code to address these issues:

ISSUES TO ADDRESS:
{issues_text}

ORIGINAL CODE:
```python
{code}
```

Return ONLY the refactored Python code that addresses all issues. 
Keep the same functionality but improve structure, readability, and efficiency.
Add brief comments where changes were made."""

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating refactored code: {str(e)}"
