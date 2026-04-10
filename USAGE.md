# Zero To Sixty - Usage Guide

Quick start guide and examples for the AI Code Review Agent.

---

## ⚡ Quick Start

### 1. Setup (2 minutes)

```bash
# Clone/navigate to project
cd zero-to-sixty

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Get Gemini API key
# Visit: https://makersuite.google.com/app/apikey
# Copy your API key

# Create .env file
cp .env.example .env
# Edit .env and paste your API key
```

### 2. Run (30 seconds)

```bash
# Review a file
python main.py -f examples/sample_code.py

# Or interactive mode
python main.py
```

---

## 📖 Usage Modes

### Interactive Mode

Paste code directly in terminal:

```bash
$ python main.py
Enter your Python code (end with 'EOF' on a new line):
def hello():
    print("hello")
    return None
EOF
```

### Review File

```bash
python main.py -f mycode.py
```

### Generate Documentation

```bash
python main.py -f mycode.py -d
```

Creates:
- `code_review_report.md` - Formatted review
- Includes generated docstrings

### Save Results

```bash
python main.py -f mycode.py -s
```

Creates:
- `code_review_report.json` - Structured data
- `code_review_report.md` - Markdown report

### JSON Output (For Scripting)

```bash
python main.py -f mycode.py -j
```

Output:
```json
{
  "static_analysis": {...},
  "ai_review": {...},
  "documentation": null
}
```

### Full Options

```bash
python main.py -f mycode.py -d -s --json
```

---

## 📝 Examples

### Example 1: Review Sample Code

```bash
python main.py -f examples/sample_code.py
```

**Issues it will find:**
- ❌ Mutable default argument `numbers=[]`
- ❌ Bare except clause
- ⚠️ No input validation
- ⚠️ Nested conditionals
- 🔒 Security: Unsafe string parsing

**Expected output:**
```
🔍 Starting code review...

Step 1: Running static analysis...
✓ Static analysis complete

Step 2: AI-powered code review (Gemini)...
✓ AI review complete

======================================================================
CODE REVIEW RESULTS
======================================================================

📊 STATIC ANALYSIS
----------------------------------------------------------------------
✓ Syntax Valid: True  
  - Functions: 3
  - Classes: 1
  - Imports: 0
  - Lines of Code: 50
  
  Complexity Score: 8
  Rating: Medium
  
  ⚠️  Potential Bugs: 2
    - Mutable default argument in function 'calculate_average'
    - Bare 'except' clause...

🤖 AI REVIEW (Gemini)
----------------------------------------------------------------------
Summary: Code has functional issues and security concerns that need attention
Score: 4/10

Bugs Found: 3
  [CRITICAL] Mutable default argument
  [HIGH] Bare exception handling
  [HIGH] Missing input validation
...
```

### Example 2: Review Good Code

```bash
python main.py -f examples/good_code.py
```

**Expected result:** High score (8+/10), clear structure, proper error handling

### Example 3: Use in CI/CD

```bash
# In GitHub Actions workflow
- name: Code Review
  run: python main.py -f src/**/*.py -j > review.json

- name: Upload Results
  uses: actions/upload-artifact@v2
  with:
    name: code-review
    path: review.json
```

### Example 4: Batch Review Multiple Files

```bash
# Create a simple script
for file in src/*.py; do
  echo "Reviewing $file..."
  python main.py -f "$file" -s
  echo "---"
done
```

---

## 🛠️ Troubleshooting

### "GEMINI_API_KEY not found"

**Solution:**
```bash
# Make sure .env exists and has your key
cat .env
# Should show: GEMINI_API_KEY=sk-...

# Or reload shell
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### "Module not found: google.generativeai"

**Solution:**
```bash
pip install --upgrade google-generativeai
```

### Timeout or slow response

**Causes:**
- Large file (>50KB)
- API rate limit
- Network latency

**Solutions:**
```bash
# Break large files into smaller modules
# Or use static analysis only (no AI)
python analysis/static_analysis.py
```

### "Invalid JSON response"

**Solution:** Gemini sometimes returns extra text. The system handles this, but if you see raw response:
```json
{
  "raw_response": "Here's the analysis..."
}
```

This is still usable - just check the text response.

---

## 📊 Understanding Output

### Static Analysis

```json
{
  "syntax_valid": true,
  "structure": {
    "functions": ["func1", "func2"],
    "classes": ["Class1"],
    "total_lines": 42
  },
  "complexity": {
    "complexity_score": 5,
    "rating": "Low"
  }
}
```

### AI Review

```json
{
  "bugs": [
    {
      "issue": "Mutable default argument",
      "severity": "critical",
      "line": "15",
      "fix": "Use None as default, initialize inside function"
    }
  ],
  "inefficiencies": [...],
  "security_issues": [...],
  "improvements": [...],
  "score": "7/10"
}
```

---

## 🔧 Customization

### Change Review Focus

Edit `agent/prompt_templates.py`:

```python
# For security-focused reviews
CODE_REVIEW_PROMPT = """
Focus on security vulnerabilities...
"""

# For performance reviews
REFACTORING_PROMPT = """
Focus on optimization opportunities...
"""
```

Then restart the agent:

```bash
python main.py -f mycode.py
```

### Adjust Complexity Thresholds

In `analysis/static_analysis.py`:

```python
def calculate_complexity(self, code: str):
    # Change thresholds
    if complexity_score <= 3:  # Was 5
        rating = "Low"
```

---

## 🚀 Advanced Usage

### Programmatic API

```python
from analysis import StaticAnalyzer
from agent import GeminiAgent

# Static analysis only
analyzer = StaticAnalyzer()
results = analyzer.run_full_analysis(code)
print(results)

# With AI review
agent = GeminiAgent()
review = agent.generate_review(code, results)
print(review)

# Generate documentation
docs = agent.generate_documentation(code, results["structure"])
print(docs)
```

### Integration with IDEs

**VS Code Extension (Future)**
```bash
# Would add code-on-save review
```

**Pre-commit Hook**
```bash
# .git/hooks/pre-commit
#!/bin/bash
python main.py -f $(git diff --cache --name-only) -j
```

---

## 📈 Performance Tips

| Optimization | Result |
|--------------|--------|
| Break large files | 20-40% faster |
| Cache results | Avoid re-analysis |
| Batch reviews | Better resource use |
| Use JSON output | Fastest response |

---

## 🔐 Privacy & Security

**Data Handling:**
- Code **IS** sent to Google Gemini API
- Review Google's [privacy policy](https://policies.google.com/privacy)
- For sensitive code: Use static analysis only
- Results saved locally by default

**Best Practices:**
```bash
# Don't commit API keys
echo ".env" >> .gitignore

# Use service account for teams
# Export results, not code
python main.py -f sensitive.py -j > review.json
```

---

## 📚 Examples in Repo

- `examples/sample_code.py` - Code with issues
- `examples/good_code.py` - Well-written example

Compare them:
```bash
python main.py -f examples/sample_code.py
python main.py -f examples/good_code.py
```

---

## ✅ Checklist

Before submitting code:

- [ ] Run Zero To Sixty review
- [ ] Address critical bugs
- [ ] High complexity (>10) refactored
- [ ] Security issues resolved
- [ ] Added docstrings (use -d flag)

Example workflow:
```bash
python main.py -f mycode.py -d -s
# Review results in code_review_report.md
# Fix critical issues
# Re-run for verification
python main.py -f mycode.py
```

---

## 🤔 FAQ

**Q: Can I use this in production?**
A: Yes! Monitor your Gemini API usage quota.

**Q: Does it support other languages?**
A: Currently Python only. Can be extended.

**Q: Is this free?**
A: Yes! Gemini has free tier. Zero To Sixty has no fees.

**Q: Can I modify prompts?**
A: Yes! Edit `agent/prompt_templates.py`

**Q: How fast is it?**
A: ~3-5 seconds per file (1-3s API, 2-3ms static analysis)

---

## 📞 Support

- Check README.md for architecture
- Review examples/ for patterns
- Check agent/prompt_templates.py for customization
- See requirements.txt for dependencies

---

**Happy reviewing! 🚀**
