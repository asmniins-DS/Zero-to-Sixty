"""
Agent module - AI-powered code review components
"""

from .gemini_agent import GeminiAgent
from .prompt_templates import (
    SYSTEM_PROMPT,
    CODE_REVIEW_PROMPT,
    SECURITY_REVIEW_PROMPT,
    DOCUMENTATION_PROMPT,
    REFACTORING_PROMPT
)

__all__ = [
    "GeminiAgent",
    "SYSTEM_PROMPT",
    "CODE_REVIEW_PROMPT",
    "SECURITY_REVIEW_PROMPT",
    "DOCUMENTATION_PROMPT",
    "REFACTORING_PROMPT"
]
