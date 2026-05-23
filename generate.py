#!/usr/bin/env python3
import os
import sys
import argparse

# Force UTF-8 output on standard streams to avoid UnicodeEncodeErrors on Windows terminals
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")
from config import Config
from leetcode_client import LeetCodeClient
from llm_client import LLMClient

# ANSI colors for premium terminal UI
BLUE = "\033[94m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"

def print_header():
    header = f"""{CYAN}{BOLD}
========================================================================
 🚀  LEETCODE SOLUTION POST GENERATOR
========================================================================{RESET}"""
    print(header)

def main():
    print_header()
    
    # 1. Parse CLI arguments
    parser = argparse.ArgumentParser(
        description="Generate a beautiful LeetCode solution post from a problem URL."
    )
    parser.add_argument(
        "url",
        help="LeetCode problem URL or solutions tab URL"
    )
    parser.add_argument(
        "--provider", "-p",
        choices=["gemini", "local"],
        help="Override the LLM provider configured in .env ('gemini' or 'local')"
    )
    parser.add_argument(
        "--model", "-m",
        help="Override the local Ollama model (only applicable if provider is local)"
    )
    parser.add_argument(
        "--output", "-o",
        help="Custom file path to save the generated markdown. Defaults to 'solutions/<slug>.md'"
    )
    
    args = parser.parse_args()
    
    # 2. Extract and validate problem slug
    print(f"\n{BLUE}[1/5] Extracting LeetCode problem ID...{RESET}")
    slug = LeetCodeClient.extract_title_slug(args.url)
    if not slug:
        print(f"{RED}{BOLD}[Error] Could not extract a valid problem slug from the URL: '{args.url}'{RESET}")
        print("Please verify the URL. It should look like:")
        print(" - https://leetcode.com/problems/unique-number-of-occurrences/")
        print(" - https://leetcode.com/problems/unique-number-of-occurrences/solutions/")
        sys.exit(1)
        
    print(f"{GREEN}✔ Successfully identified problem: {BOLD}{slug}{RESET}")
    
    # 3. Apply overrides to Config
    if args.provider:
        Config.LLM_PROVIDER = args.provider.lower()
    if args.model:
        Config.OLLAMA_MODEL = args.model
        
    # Validate the selected provider
    Config.validate_llm_config()
    
    # 4. Fetch private Accepted Submission
    print(f"\n{BLUE}[2/5] Connecting to LeetCode & extracting your solution...{RESET}")
    client = LeetCodeClient()
    
    # This will check session validation internally and stop cleanly with warning if invalid
    username = client.check_authentication()
    print(f"{GREEN}✔ Session verified! Welcome, {BOLD}{username}{RESET}.")
    
    print(f"{CYAN}⏳ Searching for your latest accepted submission for '{slug}'...{RESET}")
    submission = client.get_latest_accepted_submission(slug)
    
    print(f"{GREEN}✔ Accepted submission retrieved!{RESET}")
    print(f"  • Submission ID: {BOLD}{submission['id']}{RESET}")
    print(f"  • Language: {BOLD}{submission['lang_verbose']}{RESET}")
    print(f"  • Execution Runtime: {BOLD}{submission['runtime']}{RESET}")
    print(f"  • Memory Used: {BOLD}{submission['memory']}{RESET}")
    
    # 5. Fetch Problem Description
    print(f"\n{BLUE}[3/5] Extracting LeetCode problem details...{RESET}")
    print(f"{CYAN}⏳ Fetching description and difficulty level...{RESET}")
    problem = client.get_problem_details(slug)
    
    if not problem:
        print(f"{RED}{BOLD}[Error] Failed to fetch problem details for slug '{slug}'. Exiting.{RESET}")
        sys.exit(1)
        
    print(f"{GREEN}✔ Problem details retrieved!{RESET}")
    print(f"  • Title: {BOLD}{problem['title']}{RESET}")
    print(f"  • Difficulty: {BOLD}{problem['difficulty']}{RESET}")
    
    # 6. Generate the Post via chosen LLM
    model_name = "gemini-1.5-flash" if Config.LLM_PROVIDER == "gemini" else Config.OLLAMA_MODEL
    print(f"\n{BLUE}[4/5] Prompting LLM ({Config.LLM_PROVIDER.upper()} - {model_name})...{RESET}")
    print(f"{CYAN}⏳ Thinking and structuring markdown solution post...{RESET}")
    
    llm = LLMClient()
    post_markdown = llm.generate_solution_post(
        problem_title=problem["title"],
        difficulty=problem["difficulty"],
        description=problem["description"],
        code=submission["code"],
        language=submission["lang_verbose"]
    )
    
    if not post_markdown or post_markdown.startswith("Error"):
        print(f"{RED}{BOLD}[Error] LLM failed to generate solution content.{RESET}")
        print(post_markdown)
        sys.exit(1)
        
    print(f"{GREEN}✔ Solution post generated successfully!{RESET}")
    
    # 7. Write output markdown file
    print(f"\n{BLUE}[5/5] Saving solution post...{RESET}")
    if args.output:
        output_path = args.output
    else:
        # Default save path: solutions/<slug>.md
        output_path = os.path.join("solutions", f"{slug}.md")
        
    # Ensure directory exists
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(post_markdown)
        print(f"{GREEN}{BOLD}✔ Solution saved to: {output_path}{RESET}")
    except Exception as e:
        print(f"{RED}[Error] Failed to write solution file: {e}{RESET}")
        print("Displaying output in terminal instead:\n")
        print(post_markdown)
        sys.exit(1)
        
    # Elegant finish screen
    print(f"\n{GREEN}{BOLD}========================================================================{RESET}")
    print(f"{GREEN}{BOLD} 🎉  SUCCESS! Your LeetCode solution post is ready for upload.{RESET}")
    print(f"{GREEN}{BOLD}========================================================================{RESET}")
    print(f"📝 You can copy the generated markdown from: {BOLD}{output_path}{RESET}")
    
    # Print first few lines as a beautiful teaser
    print(f"\n{CYAN}{BOLD}Preview:{RESET}")
    preview_lines = post_markdown.strip().split("\n")
    teaser = "\n".join(preview_lines[:15])
    print(f"{teaser}\n{CYAN}... [truncated] ...{RESET}\n")

if __name__ == "__main__":
    main()
