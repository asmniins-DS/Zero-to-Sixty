# Zero To Sixty - AI Code Review Agent

**An intelligent Python code review system combining static analysis with Google Gemini AI for comprehensive code feedback.**

![Status](https://img.shields.io/badge/status-production--ready-brightgreen)
![Python](https://img.shields.io/badge/python-3.10+-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Architecture](#architecture)
4. [Tech Stack](#tech-stack)
5. [Installation](#installation)
6. [How to Use](#how-to-use)
7. [How It Works](#how-it-works)
8. [Example](#example)
9. [Bonus Features](#bonus-features)
10. [Project Structure](#project-structure)
11. [Limitations & Future Work](#limitations--future-work)

---

## 🎯 Overview

**Zero To Sixty** is a production-ready AI-powered code review system that analyzes Python code using **two complementary approaches**:

1. **Static Analysis** - Syntax checking, complexity scoring, basic issue detection
2. **AI-Powered Review** - Google Gemini AI provides intelligent, contextual feedback

The system is designed to catch bugs, identify inefficiencies, highlight security risks, and suggest improvements with detailed explanations.

### Why This Approach?

- **Static analysis** is fast, deterministic, and reduces hallucinations
- **AI adds context** - understands design patterns, architectural implications
- **Combined approach** provides both speed and intelligence

---

## ✨ Features

### Core Features

✅ **Syntax Validation**
- Validates Python syntax before review
- Provides helpful syntax error messages

✅ **Static Code Analysis**
- Extracts code structure (functions, classes, imports)
- Calculates cyclomatic complexity
- Detects patterns: bare except, mutable defaults, unused variables

✅ **AI-Powered Code Review**
- Identifies **bugs** with severity levels
- Finds **inefficiencies** and their impact
- Detects **security vulnerabilities**
- Provides **refactoring suggestions** with examples

✅ **Structured Output**
- JSON-formatted results for programmatic access
- Human-readable console output
- Exportable reviews

### Bonus Features

🚀 **Automated Documentation Generation**
- Generates Google-style docstrings
- Parameters, return types, examples
- Easy integration with existing code

📄 **Google Docs Integration** *(Optional)*
- Export reviews to Google Docs
- Share reviews with team members
- Markdown-formatted documentation

---

## 🏗️ Architecture

### System Components

```
┌─────────────────────────────────────────────┐
│          User Input (Code)                  │
└────────────────┬────────────────────────────┘
                 │
                 v
        ┌────────────────────┐
        │  Input Handler     │
        └────────┬───────────┘
                 │
                 v
┌────────────────────────────────────────────┐
│      Static Analysis Layer                 │
│  (AST | Complexity | Pattern Detection)    │
└────────────────┬───────────────────────────┘
                 │
                 v
        ┌────────────────────┐
        │   Gemini AI Agent  │
        │   (gemini-pro)     │
        └────────┬───────────┘
                 │
                 v
┌────────────────────────────────────────────┐
│    Suggestion & Report Generation          │
│ (Bugs | Inefficiencies | Security | Fixes)│
└────────────────┬───────────────────────────┘
                 │
    ┌────────────┼────────────┐
    v            v            v
┌────────┐ ┌──────────┐ ┌──────────┐
│ Console│ │   JSON   │ │ Markdown │
│ Output │ │  Export  │ │   Docs   │
└────────┘ └──────────┘ └──────────┘
```

### Module Breakdown

| Module | Responsibility |
|--------|-----------------|
| `analysis/` | Static code analysis (AST, complexity, patterns) |
| `agent/` | Gemini AI integration, prompts, templates |
| `docs/` | Documentation generation, Google Docs export |
| `main.py` | CLI entry point, orchestration |

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Language** | Python 3.10+ |
| **AI Model** | Google Gemini (gemini-pro) |
| **Static Analysis** | Python `ast` module |
| **Configuration** | python-dotenv |
| **Optional: Docs** | Google Docs API |

**Why Google Gemini?**
- Free tier available (Perfect for learning)
- Excellent code understanding
- Fast response times
- Easy integration

---

## 📦 Installation

### Prerequisites

- Python 3.10 or higher
- Google Gemini API key (free) from [Google AI Studio](https://makersuite.google.com/app/apikey)
- Virtual environment (recommended)

### Step 1: Clone/Setup

```bash
# Create project directory
mkdir zero-to-sixty
cd zero-to-sixty

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Configure API Key

1. Get your free Gemini API key: https://makersuite.google.com/app/apikey
2. Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_actual_api_key_here
```

### Step 4: Verify Installation

```bash
python main.py --help
```

You should see the help menu.

---

## 🚀 How to Use

### Interactive Mode

```bash
python main.py
```

Then paste your Python code, ending with `EOF` on a new line.

### Review a File

```bash
python main.py -f mycode.py
```

### Generate Documentation

```bash
python main.py -f mycode.py -d
```

### Save Results

```bash
python main.py -f mycode.py -s
```

Creates `code_review_report.json` and `code_review_report.md`.

### Output as JSON

```bash
python main.py -f mycode.py -j
```

Perfect for CI/CD integration.

### Full Example

```bash
python main.py -f app.py -d -s --json
```

Analyzes `app.py`, generates docs, saves results, outputs JSON.

---

## 🔍 How It Works

### Phase 1: Static Analysis (2-3ms)

```python
analyzer = StaticAnalyzer()
results = analyzer.run_full_analysis(code)
```

**Checks:**
- ✓ Syntax validity
- ✓ Code structure (functions, classes)
- ✓ Cyclomatic complexity
- ✓ Basic patterns (mutable defaults, bare except)

**Output:**
```json
{
  "syntax_valid": true,
  "structure": {
    "functions": [...],
    "classes": [...],
    "imports": [...]
  },
  "complexity": {
    "complexity_score": 6,
    "rating": "Medium"
  },
  "issues": {...}
}
```

### Phase 2: AI Review (1-3 seconds)

```python
agent = GeminiAgent()
review = agent.generate_review(code, static_results)
```

**Gemini analyzes:**
- Bug patterns and critical issues
- Code inefficiencies
- Security vulnerabilities
- Refactoring opportunities with examples

**Output:**
```json
{
  "bugs": [
    {
      "issue": "...",
      "severity": "critical",
      "line": "...",
      "fix": "..."
    }
  ],
  "inefficiencies": [...],
  "security_issues": [...],
  "improvements": [...],
  "summary": "...",
  "score": "7/10"
}
```

### Phase 3: Documentation (Optional)

Uses AI to generate Google-style docstrings and exports as Markdown.

---

## 📝 Example

### Input Code
```python
def process_data(data=[]):
    try:
        for item in data:
            if item > 0:
                if item % 2 == 0:
                    print(item)
    except:
        pass
    return data
```

### Static Analysis Results
```
✓ Syntax Valid
  - Functions: 1
  - Cyclomatic Complexity: 4 (Low-Medium)
  
Issues Detected:
  - Mutable default argument: data=[]
  - Bare except clause
```

### AI Review Results
```
BUGS (1):
├─ [Critical] Mutable default argument 'data=[]'
│  ├─ Impact: Will mutate same list across all calls
│  └─ Fix: Use None as default, initialize inside function

INEFFICIENCIES (1):
├─ Nested conditionals could be simplified
│  └─ Suggestion: Replace nested if with single condition

SECURITY (1):
├─ Bare except clause
│  └─ Risk: Catches all exceptions including SystemExit

IMPROVEMENTS (1):
├─ Use list comprehension for filtering
├─ Add input validation
├─ Document function purpose
```

### Refactored Code
```python
def process_data(data: list | None = None) -> list:
    """
    Process and filter data.
    
    Args:
        data: List of integers to process. Defaults to empty list.
        
    Returns:
        Processed list of even positive integers.
    """
    if data is None:
        data = []
    
    try:
        return [item for item in data if item > 0 and item % 2 == 0]
    except (TypeError, ValueError) as e:
        print(f"Error processing data: {e}")
        return []
```

---

## 🎁 Bonus Features

### 1. Automated Documentation Generation

```bash
python main.py -f mycode.py -d -s
```

**Generates:**
- Google-style docstrings
- Type hints
- Parameter documentation
- Usage examples
- Saves as `code_review_report.md`

### 2. Google Docs Export

To enable Google Docs export:

1. Create Google Cloud project
2. Enable Google Docs API
3. Create service account credentials
4. Set `GOOGLE_CREDENTIALS_FILE` in `.env`

```python
from docs import GoogleDocsGenerator

docs_gen = GoogleDocsGenerator()
doc_id = docs_gen.create_google_doc(
    title="Code Review Report",
    content=markdown_content
)
```

### 3. CI/CD Integration

Export as JSON for pipeline integration:

```bash
python main.py -f src.py -j > review.json
```

Use in GitHub Actions:
```yaml
- run: python main.py -f src.py -j > review.json
- uses: some-action/report-results
  with:
    report: review.json
```

---

## 📁 Project Structure

```
zero_to_sixty/
├── agent/                      # AI integration
│   ├── __init__.py
│   ├── gemini_agent.py        # Gemini API wrapper
│   └── prompt_templates.py    # Prompt configurations
│
├── analysis/                   # Static analysis
│   ├── __init__.py
│   └── static_analysis.py     # AST & pattern detection
│
├── docs/                       # Documentation
│   ├── __init__.py
│   └── doc_generator.py       # Docstring generation
│
├── diagrams/                   # System diagrams
│   └── system_diagram.png
│
├── main.py                     # Entry point
├── requirements.txt            # Dependencies
├── .env                        # Configuration (API keys)
├── .env.example               # Template
└── README.md                   # This file
```

---

## ⚙️ Configuration

### Environment Variables

```env
# Required
GEMINI_API_KEY=your_api_key

# Optional
GOOGLE_CREDENTIALS_FILE=path/to/service_account.json
```

### Customizing Prompts

Edit `agent/prompt_templates.py` to customize review focus:

```python
CODE_REVIEW_PROMPT = """Your custom prompt here..."""
```

---

## 🔒 Security Considerations

| Aspect | Handling |
|--------|----------|
| **API Keys** | Stored in `.env`, never committed |
| **Code Privacy** | Sent to Google Gemini API (review their privacy policy) |
| **Output** | Saved locally by default |
| **Credentials** | Service account keys stored securely |

**Note:** By default, code is sent to Google Gemini API. For private/sensitive code, run local static analysis only or use an on-premise AI model.

---

## 📊 Performance

| Operation | Time | Notes |
|-----------|------|-------|
| Static Analysis | 2-3ms | Very fast, local only |
| AI Review | 1-3s | Depends on code length, API latency |
| Documentation | 1-2s | If enabled |
| **Total** | ~3-5s | For typical code |

---

## 🔄 Limitations & Future Work

### Current Limitations

| Limitation | Impact | Workaround |
|-----------|--------|-----------|
| Python only | Can't review other languages | Use language-specific tools |
| Requires API key | Cost if exceeded free tier | Use free tier, monitor usage |
| AI hallucinations | Rare but possible | Always review suggestions |
| Large files slow | 30KB+ may timeout | Break into modules |

### Future Enhancements

- [ ] Support for TypeScript, JavaScript
- [ ] Multi-file project analysis
- [ ] Custom rule configuration
- [ ] Performance profiling integration
- [ ] Git pre-commit hook
- [ ] Web interface
- [ ] Team collaboration features
- [ ] Historical comparison
- [ ] Auto-fix suggestions (with approval)
- [ ] IDE extensions (VS Code, PyCharm)

---

## 🤝 Contributing

Found a bug? Have a suggestion?

1. Test your case locally
2. Document the issue
3. Submit with example code

---

## 📜 License

MIT License - Free for personal and commercial use.

---

## 🙋 FAQ

### Q: Is this free to use?

**A:** Yes! Google Gemini has a generous free tier. Zero To Sixty has no licensing costs.

### Q: Can I use it in production?

**A:** Yes. It's designed for production use. Just monitor your Gemini API usage.

### Q: What about sensitive/private code?

**A:** Code is sent to Google's servers. If you have concerns, run static analysis only (no AI) or deploy a local LLM.

### Q: Can I modify the prompts?

**A:** Absolutely! Edit `agent/prompt_templates.py` to customize review focus.

### Q: Does it support Python 2?

**A:** No. Python 3.10+ only. Can be adapted for earlier 3.x with minor changes.

### Q: How do I use it in CI/CD?

**A:** Export as JSON: `python main.py -f src.py -j > review.json` and integrate into your pipeline.

---

## 📚 References

- [Google Gemini API Docs](https://ai.google.dev/docs)
- [Python AST Module](https://docs.python.org/3/library/ast.html)
- [Google Docs API](https://developers.google.com/docs/api)

---

## 🎓 Learning Resources

This project teaches:
- AI/LLM integration in Python
- Static code analysis with AST
- System design and modularity
- API integration (Google Gemini, Google Docs)
- CLI application design
- Error handling and validation

---

**Made with ❤️ for code quality.**

*Version: 1.0.0 | Last Updated: 2025*
