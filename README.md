# Welcome to Zero To Sixty
***

## Task
Zero To Sixty is designed to solve the challenge of reviewing Python code with a mix of deterministic static analysis and intelligent AI feedback. It helps developers identify bugs, inefficiencies, security risks, and improvement opportunities while demonstrating how agentic AI concepts can support real-world workflows.

## Description
This project combines a lightweight Python code review system with a practical AI agent guide. It uses AST-based static analysis to extract structure, evaluate complexity, and detect common issues, then enriches that output with Google Gemini-powered AI review and documentation generation. The repository also includes guidance on AI agents, data agents, ethics, and deployment considerations.

## Installation
### Prerequisites
- Python 3.10 or newer
- A virtual environment is recommended
- Google Gemini API key (obtain from https://makersuite.google.com/app/apikey)

### Setup
```bash
cd /workspaces/Zero-to-Sixty
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Configuration
Create a `.env` file from `.env.example` and add your API key:

```env
GEMINI_API_KEY=your_actual_api_key_here
```

## Usage
### Review a Python file
```bash
python main.py -f examples/sample_code.py
```

### Print the practical AI agent guide
```bash
python main.py -g
```

### Run in interactive mode
```bash
python main.py
```
Then paste your Python code and end with `EOF`.

### Generate documentation for reviewed code
```bash
python main.py -f examples/sample_code.py -d
```

### Save review results to JSON
```bash
python main.py -f examples/sample_code.py -s
```

### Output review as JSON
```bash
python main.py -f examples/sample_code.py -j
```

### Full command example
```bash
python main.py -f examples/sample_code.py -d -s --json
```

### What this project includes
- `main.py`: CLI entrypoint and orchestration
- `analysis/`: static code analysis tools
- `agent/`: AI agent integration and prompts
- `docs/`: documentation generation utilities
- `examples/`: sample Python code for review
- `AGENT_GUIDE.md`: practical guide to AI agents

### Key capabilities
- Syntax validation, structure extraction, and complexity scoring
- Detection of bare `except`, mutable defaults, unused variables, and security concerns
- AI-powered code review summaries, bug tracking, and improvement suggestions
- Optional generation of Google-style documentation and markdown reports

### Notes
- If `GEMINI_API_KEY` is missing, the repository still provides static analysis coverage.
- The `-g` command prints a practical AI agent guide bundled with this project.

### The Core Team

Abubakar Sadik Nasir.
ASMNI_DS.
<span><i>Made at <a href='https://qwasar.io'>Qwasar SV -- Software Engineering School</a></i></span>
<span><img alt='Qwasar SV -- Software Engineering School's Logo' src='https://storage.googleapis.com/qwasar-public/qwasar-logo_50x50.png' width='20px' /></span>
