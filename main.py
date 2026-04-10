#!/usr/bin/env python3
"""
Zero To Sixty - AI Code Review Agent
Main entry point for the application
"""

import sys
import json
from pathlib import Path
from typing import Optional

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from analysis import StaticAnalyzer
from agent import GeminiAgent
from docs import GoogleDocsGenerator


class CodeReviewSystem:
    """Main system orchestrating static analysis + AI review"""

    def __init__(self):
        """Initialize the review system"""
        self.analyzer = StaticAnalyzer()
        self.ai_agent = None
        self.docs_generator = GoogleDocsGenerator()
        
        # Initialize AI agent with fallback for missing API key
        try:
            self.ai_agent = GeminiAgent()
        except (ValueError, ImportError) as e:
            print(f"⚠️  AI Agent not available: {e}")
            print("   Static analysis will still work.\n")

    def review_code(self, code: str, include_docs: bool = False, save_docs: bool = False) -> dict:
        """
        Complete code review pipeline
        
        Args:
            code: Python code to review
            include_docs: Generate documentation
            save_docs: Save documentation to file
            
        Returns:
            Complete review results
        """
        
        print("🔍 Starting code review...\n")

        # Step 1: Static Analysis
        print("Step 1: Running static analysis...")
        static_results = self.analyzer.run_full_analysis(code)
        
        if not static_results.get("syntax_valid"):
            print("❌ Code has syntax errors. Cannot proceed with review.")
            return static_results

        print("✓ Static analysis complete\n")

        # Step 2: AI Review
        review_result = {
            "static_analysis": static_results,
            "ai_review": None,
            "documentation": None
        }

        if self.ai_agent:
            print("Step 2: AI-powered code review (Gemini)...")
            ai_review = self.ai_agent.generate_review(code, static_results)
            review_result["ai_review"] = ai_review
            print("✓ AI review complete\n")
        else:
            print("Step 2: Skipped (AI Agent not available)\n")

        # Step 3: Documentation Generation (Bonus)
        if include_docs and self.ai_agent:
            print("Step 3: Generating documentation...")
            docs = self.ai_agent.generate_documentation(code, static_results["structure"])
            review_result["documentation"] = docs
            print("✓ Documentation generated\n")

            if save_docs and review_result["ai_review"]:
                print("Step 4: Saving documentation...")
                markdown_doc = self.docs_generator.generate_documentation_markdown(
                    review_result["ai_review"],
                    code
                )
                self.docs_generator.save_documentation_locally(markdown_doc)
                print("✓ Documentation saved\n")

        return review_result

    def print_review(self, review_result: dict):
        """Pretty print review results"""
        
        print("\n" + "="*70)
        print("CODE REVIEW RESULTS")
        print("="*70 + "\n")

        # Static Analysis Results
        static = review_result.get("static_analysis", {})
        print("📊 STATIC ANALYSIS")
        print("-" * 70)
        print(f"✓ Syntax Valid: {static.get('syntax_valid', 'N/A')}")
        
        structure = static.get("structure", {})
        if structure and "error" not in structure:
            print(f"  - Functions: {len(structure.get('functions', []))}")
            print(f"  - Classes: {len(structure.get('classes', []))}")
            print(f"  - Imports: {len(structure.get('imports', []))}")
            print(f"  - Lines of Code: {structure.get('total_lines', 'N/A')}")

        complexity = static.get("complexity", {})
        if complexity and "error" not in complexity:
            print(f"\n  Complexity Score: {complexity.get('complexity_score', 'N/A')}")
            print(f"  Rating: {complexity.get('rating', 'N/A')}")

        issues = static.get("issues", {})
        if issues:
            bugs = issues.get("potential_bugs", [])
            if bugs:
                print(f"\n  ⚠️  Potential Bugs: {len(bugs)}")
                for bug in bugs[:3]:  # Show first 3
                    print(f"    - {bug}")

        # AI Review Results
        ai_review = review_result.get("ai_review")
        if ai_review and "error" not in ai_review:
            print("\n🤖 AI REVIEW (Gemini)")
            print("-" * 70)
            print(f"Summary: {ai_review.get('summary', 'N/A')}")
            print(f"Score: {ai_review.get('score', 'N/A')}/10")

            bugs = ai_review.get("bugs", [])
            if bugs:
                print(f"\nBugs Found: {len(bugs)}")
                for bug in bugs[:3]:
                    severity = bug.get('severity', 'unknown').upper()
                    print(f"  [{severity}] {bug.get('issue', 'Unknown')}")

            inefficiencies = ai_review.get("inefficiencies", [])
            if inefficiencies:
                print(f"\nInefficencies: {len(inefficiencies)}")
                for item in inefficiencies[:2]:
                    print(f"  - {item.get('issue', 'Unknown')}")

            security = ai_review.get("security_issues", [])
            if security:
                print(f"\nSecurity Issues: {len(security)}")
                for issue in security[:2]:
                    print(f"  - {issue.get('issue', 'Unknown')}")

        elif ai_review:
            print("\n🤖 AI REVIEW")
            print("-" * 70)
            print("Raw Response:")
            print(ai_review.get("raw_response", "No response"))

        print("\n" + "="*70 + "\n")

    def save_review_json(self, review_result: dict, output_file: str = "review_report.json"):
        """Save review results to JSON file"""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(review_result, f, indent=2)
            print(f"✓ Review saved to {output_file}")
        except Exception as e:
            print(f"Error saving review: {e}")


def get_code_input() -> str:
    """Get code input from user"""
    print("📝 Enter your Python code (end with 'EOF' on a new line):")
    print("-" * 70)
    
    lines = []
    while True:
        line = input()
        if line.strip() == "EOF":
            break
        lines.append(line)
    
    return "\n".join(lines)


def get_code_from_file(filepath: str) -> Optional[str]:
    """Load code from a file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"❌ File not found: {filepath}")
        return None


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Zero To Sixty - AI Code Review Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                    # Interactive mode
  python main.py -f mycode.py       # Review from file
  python main.py -f mycode.py -d   # Generate documentation
        """
    )
    
    parser.add_argument('-f', '--file', 
                       type=str, 
                       help='Python file to review')
    parser.add_argument('-d', '--docs', 
                       action='store_true', 
                       help='Generate documentation')
    parser.add_argument('-s', '--save', 
                       action='store_true', 
                       help='Save results to file')
    parser.add_argument('-j', '--json', 
                       action='store_true', 
                       help='Output as JSON')

    args = parser.parse_args()

    print("\n" + "="*70)
    print("ZERO TO SIXTY - AI Code Review Agent")
    print("="*70 + "\n")

    # Initialize system
    system = CodeReviewSystem()

    # Get code
    if args.file:
        code = get_code_from_file(args.file)
        if not code:
            sys.exit(1)
    else:
        code = get_code_input()

    if not code.strip():
        print("❌ No code provided")
        sys.exit(1)

    # Run review
    review_result = system.review_code(
        code, 
        include_docs=args.docs,
        save_docs=args.save
    )

    # Output results
    if args.json:
        print(json.dumps(review_result, indent=2))
    else:
        system.print_review(review_result)

    # Save if requested
    if args.save:
        system.save_review_json(review_result)


if __name__ == "__main__":
    main()
