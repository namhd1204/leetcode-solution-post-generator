import os
import sys

# Custom robust .env parser in case python-dotenv is not installed
def load_env_file(filepath=".env"):
    if not os.path.exists(filepath):
        return False
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, val = line.split("=", 1)
                    key = key.strip()
                    val = val.strip()
                    # Strip surrounding quotes if present
                    if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                        val = val[1:-1]
                    if key and key not in os.environ:
                        os.environ[key] = val
        return True
    except Exception:
        return False

# Attempt to load using standard python-dotenv, fallback to custom parser
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    load_env_file()

class Config:
    # LLM settings
    LLM_PROVIDER = os.environ.get("LLM_PROVIDER", "gemini").strip().lower()
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
    GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash").strip()
    
    # Ollama settings
    OLLAMA_API_BASE = os.environ.get("OLLAMA_API_BASE", "http://localhost:11434").strip()
    OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3").strip()
    
    # LeetCode settings
    LEETCODE_SESSION = os.environ.get("LEETCODE_SESSION", "").strip()
    CSRF_TOKEN = os.environ.get("CSRF_TOKEN", "").strip()

    @classmethod
    def validate_llm_config(cls):
        """Validates only the LLM configuration based on the chosen provider."""
        if cls.LLM_PROVIDER not in ["gemini", "local"]:
            print("\033[91m[Error] Invalid LLM_PROVIDER in configuration. Must be 'gemini' or 'local'.\033[0m")
            sys.exit(1)
            
        if cls.LLM_PROVIDER == "gemini":
            if not cls.GEMINI_API_KEY or cls.GEMINI_API_KEY == "your_gemini_api_key_here":
                print("\033[91m[Error] GEMINI_API_KEY is missing or invalid in your .env file.\033[0m")
                print("Please register a free API Key at: https://aistudio.google.com/")
                sys.exit(1)
        elif cls.LLM_PROVIDER == "local":
            if not cls.OLLAMA_API_BASE:
                print("\033[91m[Error] OLLAMA_API_BASE is not configured in your .env file.\033[0m")
                sys.exit(1)

    @classmethod
    def is_leetcode_configured(cls):
        """Returns True if LeetCode session values look populated."""
        has_session = bool(cls.LEETCODE_SESSION) and cls.LEETCODE_SESSION != "your_leetcode_session_cookie_here"
        return has_session
