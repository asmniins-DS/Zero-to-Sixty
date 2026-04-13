"""
Prompt templates for various code review scenarios
"""

SYSTEM_PROMPT = """You are an expert Python software engineer and AI agent specialist with deep knowledge of:
- Software design patterns
- Security best practices
- Performance optimization
- Code quality standards
- Python idioms and best practices
- Agentic AI and data agent workflows

Your role is to provide constructive, actionable code reviews that consider how the code supports autonomous AI agents and secure data access."""

CODE_REVIEW_PROMPT = """Analyze this Python code and provide a structured review including:
1. Bugs and critical issues
2. Code inefficiencies
3. Security vulnerabilities
4. Refactoring suggestions
5. Considerations for AI agent workflows, data access, and explainability

Code:
{code}

Provide specific, actionable feedback."""

SECURITY_REVIEW_PROMPT = """Perform a security-focused review of this Python code.
Identify:
- Input validation issues
- Injection vulnerabilities
- Authentication/authorization problems
- Data exposure risks
- Dependency vulnerabilities
- Risks for AI agent integration and data governance

Code:
{code}

Severity levels: critical, high, medium, low"""

DOCUMENTATION_PROMPT = """Generate comprehensive Google-style docstrings for this code.
Include type hints, parameters, returns, examples, and notes about how the code supports AI agent behavior.

Code:
{code}"""

REFACTORING_PROMPT = """Suggest refactoring improvements for this code.
Focus on:
- Readability
- Maintainability
- DRY principle
- Design patterns
- Support for agentic AI flows

Code:
{code}"""
