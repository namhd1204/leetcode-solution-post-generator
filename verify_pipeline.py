#!/usr/bin/env python3
import os
import sys
from config import Config
from llm_client import LLMClient

# ANSI colors for premium terminal UI
CYAN = "\033[96m"
GREEN = "\033[92m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"

# Force UTF-8 output on standard streams to avoid UnicodeEncodeErrors on Windows terminals
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

def main():
    print(f"{CYAN}{BOLD}========================================================================{RESET}")
    print(f"{CYAN}{BOLD} 🧪  PIPELINE VERIFICATION & MOCK TESTING{RESET}")
    print(f"{CYAN}{BOLD}========================================================================{RESET}")
    
    # 1. Validate LLM Config
    print(f"\n1. Validating LLM configuration...")
    Config.validate_llm_config()
    model_name = "gemini-1.5-flash" if Config.LLM_PROVIDER == "gemini" else Config.OLLAMA_MODEL
    print(f"{GREEN}✔ Config valid. Provider: {BOLD}{Config.LLM_PROVIDER.upper()}{RESET} (Model: {model_name})")
    
    # 2. Setup Mock Data
    print(f"\n2. Setting up mock LeetCode problem and accepted code...")
    mock_title = "Two Sum"
    mock_difficulty = "Easy"
    mock_description = """
Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to `target`.
You may assume that each input would have exactly one solution, and you may not use the same element twice.
You can return the answer in any order.

Example 1:
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].

Constraints:
* 2 <= nums.length <= 10^4
* -10^9 <= nums[i] <= 10^9
* -10^9 <= target <= 10^9
* Only one valid answer exists.
"""
    mock_code = """
class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        seen = {}
        for i, num in enumerate(nums):
            diff = target - num
            if diff in seen:
                return [seen[diff], i]
            seen[num] = i
        return []
"""
    mock_language = "Python3"
    
    print(f"  • Problem: {BOLD}{mock_title}{RESET} ({mock_difficulty})")
    print(f"  • Code Language: {BOLD}{mock_language}{RESET}")
    
    # 3. Trigger LLM generation
    print(f"\n3. Prompting LLM and generating solution post...")
    try:
        llm = LLMClient()
        post_markdown = llm.generate_solution_post(
            problem_title=mock_title,
            difficulty=mock_difficulty,
            description=mock_description,
            code=mock_code,
            language=mock_language
        )
        
        if not post_markdown or post_markdown.startswith("Error"):
            print(f"{RED}{BOLD}[Error] LLM generation failed:{RESET}")
            print(post_markdown)
            sys.exit(1)
            
        print(f"{GREEN}✔ Solution post generated successfully!{RESET}")
        
        # 4. Save and Preview
        output_path = os.path.join("solutions", "mock-two-sum.md")
        os.makedirs("solutions", exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(post_markdown)
            
        print(f"{GREEN}{BOLD}✔ Test solution saved to: {output_path}{RESET}")
        print(f"\n{CYAN}{BOLD}Preview:{RESET}")
        print(post_markdown)
        
    except Exception as e:
        print(f"{RED}[Error] Verification pipeline failed: {e}{RESET}")
        sys.exit(1)

if __name__ == "__main__":
    main()
