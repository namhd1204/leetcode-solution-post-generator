import requests
from config import Config

class LLMClient:
    SYSTEM_PROMPT = """
You are an expert software engineer and competitive programmer specializing in creating clean, pedagogical LeetCode explanations.
Your task is to write a highly detailed, concise, and professional explanation of the provided LeetCode problem based on the user's ACCEPTED code solution.

You MUST write the explanation in ENGLISH.
You MUST format your entire output to match the following markdown structure EXACTLY:

# [Insert Short, Concise Title Here]

# Intuition
[Write a concise description of your first thoughts and insights when analyzing the problem, and the main core idea behind the solution.]

# Approach
[Explain the step-by-step algorithm, how you implemented the solution, and any data structures/techniques utilized. Make sure to embed the provided code solution in a clean markdown code block inside this section.]

# Complexity
- Time complexity:
[State the time complexity using LaTeX formatting like $$O(n)$$ or $$O(n \\log n)$$, and explain why, relating it to the input variables.]

- Space complexity:
[State the space complexity using LaTeX formatting like $$O(1)$$ or $$O(n)$$, and explain why.]

CRITICAL RULES:
1. You MUST start the output with a short, concise, and punchy Title (e.g., "# Simple Greedy Two-Pointer O(N)" or "# Stack-based Linear Scan"). Do NOT keep the brackets around the title, replace "[Insert Short, Concise Title Here]" with the actual title.
2. Do NOT include any HTML placeholder comments (like `<!-- Describe... -->` or `<!-- Add your... -->`) in the generated output. The output must contain ONLY your actual generated content.
3. Do NOT include any intro or outro conversational filler text (like "Here is the explanation:", "I hope this helps!"). Only return the exact markdown format starting with "# [Title]".
4. Use double dollar signs for LaTeX complexity notation (e.g., $$O(n)$$).
5. Use hyphenated bullets for complexity: `- Time complexity:` and `- Space complexity:`.
6. In the Approach section, you must include a code block showing the user's code, prefixed with the correct language syntax (e.g., ```python, ```javascript, etc.).
"""

    def __init__(self):
        Config.validate_llm_config()
        self.provider = Config.LLM_PROVIDER

    def generate_solution_post(self, problem_title, difficulty, description, code, language):
        """Generates a structured LeetCode solution post in markdown format."""
        
        user_prompt = f"""
Problem Title: {problem_title}
Difficulty: {difficulty}

Problem Description:
\"\"\"
{description}
\"\"\"

User's Accepted Code Solution (written in {language}):
\"\"\"
{code}
\"\"\"

Generate the solution post following the system instructions and the exact template.
"""

        if self.provider == "gemini":
            return self._call_gemini(user_prompt)
        elif self.provider == "local":
            return self._call_ollama(user_prompt)
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")

    def _call_gemini(self, prompt):
        """Calls the official Google Gemini API via its REST endpoint."""
        model_name = Config.GEMINI_MODEL
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={Config.GEMINI_API_KEY}"
        
        payload = {
            "systemInstruction": {
                "parts": [{"text": self.SYSTEM_PROMPT}]
            },
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": prompt}]
                }
            ],
            "generationConfig": {
                "temperature": 0.2,
                "maxOutputTokens": 2048
            }
        }
        
        headers = {"Content-Type": "application/json"}
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            if response.status_code != 200:
                return (
                    f"Error: Gemini API returned HTTP status {response.status_code}.\n"
                    f"Details: {response.text}"
                )
                
            res_json = response.json()
            candidates = res_json.get("candidates", [])
            if not candidates:
                return "Error: Gemini API response did not contain any generation candidates."
                
            parts = candidates[0].get("content", {}).get("parts", [])
            if not parts:
                return "Error: Gemini API response text parts were empty."
                
            return parts[0].get("text", "")
            
        except Exception as e:
            return f"Error: Failed to connect to Gemini API: {e}"

    def _call_ollama(self, prompt):
        """Calls the local Ollama API via its REST endpoint."""
        url = f"{Config.OLLAMA_API_BASE}/api/generate"
        
        payload = {
            "model": Config.OLLAMA_MODEL,
            "system": self.SYSTEM_PROMPT,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.2
            }
        }
        
        headers = {"Content-Type": "application/json"}
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=60)
            if response.status_code != 200:
                return (
                    f"Error: Ollama API returned HTTP status {response.status_code}.\n"
                    f"Details: {response.text}"
                )
                
            res_json = response.json()
            generated_text = res_json.get("response", "")
            if not generated_text:
                return "Error: Ollama API response is empty."
                
            return generated_text
            
        except Exception as e:
            return (
                f"Error: Failed to connect to local Ollama service at {Config.OLLAMA_API_BASE}.\n"
                f"Make sure Ollama is running and the model '{Config.OLLAMA_MODEL}' is downloaded (run: ollama pull {Config.OLLAMA_MODEL}).\n"
                f"Details: {e}"
            )
