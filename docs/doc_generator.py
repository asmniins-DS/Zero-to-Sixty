"""
Google Docs Integration
Handles documentation generation and upload to Google Docs (Bonus Feature)
"""

import os
import json
from typing import Optional, List, Dict, Any
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


class GoogleDocsGenerator:
    """Generates documentation and uploads to Google Docs"""

    def __init__(self, credentials_file: Optional[str] = None):
        """
        Initialize Google Docs generator
        
        Args:
            credentials_file: Path to Google service account credentials JSON
        """
        self.credentials_file = credentials_file or os.getenv("GOOGLE_CREDENTIALS_FILE")
        self.service = None
        
        # Initialize service if credentials available
        if self.credentials_file and os.path.exists(self.credentials_file):
            self._initialize_service()

    def _initialize_service(self):
        """Initialize Google Docs API service"""
        try:
            from google.auth.transport.requests import Request
            from google.oauth2.service_account import Credentials
            from googleapiclient.discovery import build
            
            credentials = Credentials.from_service_account_file(
                self.credentials_file,
                scopes=["https://www.googleapis.com/auth/documents"]
            )
            self.service = build("docs", "v1", credentials=credentials)
        except ImportError:
            print("Google API libraries not installed. Skipping Google Docs integration.")
        except Exception as e:
            print(f"Error initializing Google Docs: {e}")

    def generate_documentation_markdown(self, 
                                        code_review: Dict[str, Any],
                                        code: str) -> str:
        """
        Generate markdown documentation from code review
        
        Args:
            code_review: AI review results
            code: Original code
            
        Returns:
            Markdown formatted documentation
        """
        
        doc = f"""# Code Review Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary
{code_review.get('summary', 'No summary available')}

**Overall Score:** {code_review.get('score', 'N/A')}/10

---

## Original Code
```python
{code}
```

---

## Bugs Found
"""
        
        bugs = code_review.get('bugs', [])
        if bugs:
            for bug in bugs:
                doc += f"""
### {bug.get('issue', 'Unknown bug')}
- **Severity:** {bug.get('severity', 'unknown')}
- **Line:** {bug.get('line', 'unknown')}
- **Fix:** {bug.get('fix', 'No fix provided')}
"""
        else:
            doc += "\nNo bugs detected.\n"

        doc += f"""
---

## Inefficiencies
"""
        
        inefficiencies = code_review.get('inefficiencies', [])
        if inefficiencies:
            for item in inefficiencies:
                doc += f"""
### {item.get('issue', 'Unknown inefficiency')}
- **Impact:** {item.get('impact', 'unknown')}
- **Suggestion:** {item.get('suggestion', 'No suggestion provided')}
"""
        else:
            doc += "\nNo inefficiencies found.\n"

        doc += f"""
---

## Security Issues
"""
        
        security = code_review.get('security_issues', [])
        if security:
            for issue in security:
                doc += f"""
### {issue.get('issue', 'Unknown security issue')}
- **Risk Level:** {issue.get('risk_level', 'unknown')}
- **Recommendation:** {issue.get('recommendation', 'No recommendation')}
"""
        else:
            doc += "\nNo security issues detected.\n"

        doc += f"""
---

## Improvements
"""
        
        improvements = code_review.get('improvements', [])
        if improvements:
            for improvement in improvements:
                doc += f"""
### {improvement.get('reason', 'Improvement')}

**Current:**
```python
{improvement.get('current', 'N/A')}
```

**Improved:**
```python
{improvement.get('improved', 'N/A')}
```
"""
        else:
            doc += "\nNo improvements suggested.\n"

        return doc

    def create_google_doc(self, title: str, content: str) -> Optional[str]:
        """
        Create a Google Doc with content
        
        Args:
            title: Document title
            content: Document content (markdown will be converted)
            
        Returns:
            Document ID if successful, None otherwise
        """
        
        if not self.service:
            print("Google Docs service not initialized. Cannot create document.")
            return None

        try:
            from googleapiclient.errors import HttpError
            
            document = {
                "title": title,
                "body": {
                    "content": [
                        {
                            "paragraph": {
                                "text": content
                            }
                        }
                    ]
                }
            }
            
            doc = self.service.documents().create(body=document).execute()
            doc_id = doc.get('documentId')
            return doc_id
            
        except Exception as e:
            print(f"Error creating Google Doc: {e}")
            return None

    def save_documentation_locally(self, 
                                   documentation: str, 
                                   output_file: str = "code_review_report.md") -> bool:
        """
        Save documentation to local file
        
        Args:
            documentation: Documentation content
            output_file: Output file path
            
        Returns:
            True if successful
        """
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(documentation)
            print(f"Documentation saved to {output_file}")
            return True
        except Exception as e:
            print(f"Error saving documentation: {e}")
            return False
