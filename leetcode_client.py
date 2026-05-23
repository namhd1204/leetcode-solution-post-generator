import re
import sys
import requests
from bs4 import BeautifulSoup
from config import Config

class LeetCodeClient:
    GRAPHQL_URL = "https://leetcode.com/graphql/"
    
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            "Content-Type": "application/json",
            "Referer": "https://leetcode.com",
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        }
        
        # Inject cookies and CSRF token if configured
        if Config.LEETCODE_SESSION:
            # Set cookies individually
            self.session.cookies.set("LEETCODE_SESSION", Config.LEETCODE_SESSION, domain=".leetcode.com")
            if Config.CSRF_TOKEN:
                self.session.cookies.set("csrftoken", Config.CSRF_TOKEN, domain=".leetcode.com")
                self.headers["x-csrftoken"] = Config.CSRF_TOKEN
                
        self.session.headers.update(self.headers)

    @staticmethod
    def extract_title_slug(url):
        """Extracts the problem titleSlug from any valid LeetCode URL."""
        if not url:
            return None
        url = url.strip()
        
        # Regex to handle leetcode.com/problems/<slug>/...
        match = re.search(r'leetcode\.com/problems/([^/]+)', url)
        if match:
            return match.group(1)
            
        # Fallback regex for direct path segments containing problems
        match = re.search(r'/problems/([^/]+)', url)
        if match:
            return match.group(1)
            
        return None

    def print_auth_warning_and_exit(self):
        """Prints a beautiful, highly detailed warning message and halts execution."""
        warning_box = """
========================================================================
                      ⚠️  LEETCODE AUTHENTICATION ERROR ⚠️
========================================================================
The tool could not retrieve your LeetCode submissions. This usually
means your session cookies are either missing, incorrect, or expired.

To fix this:
1. Open https://leetcode.com in your web browser and log in.
2. Open Developer Tools (press F12 or right-click -> Inspect).
3. Go to the "Application" tab (Chrome/Edge) or "Storage" tab (Firefox).
4. Expand "Cookies" on the left menu and select "https://leetcode.com".
5. Find these two cookies and copy their values:
   - LEETCODE_SESSION
   - csrftoken
6. Open your .env file in this directory and paste the values:
   LEETCODE_SESSION=your_copied_session_value
   CSRF_TOKEN=your_copied_csrftoken_value
7. Save the .env file and run this tool again!
========================================================================
"""
        print("\033[93m" + warning_box + "\033[0m")
        sys.exit(1)

    def check_authentication(self):
        """Checks if the user session is active and signed in using a lightweight GraphQL query."""
        if not Config.LEETCODE_SESSION:
            print("\033[93m[Warning] LEETCODE_SESSION is not set in your .env file.\033[0m")
            self.print_auth_warning_and_exit()
            
        query = """
        query currentUser {
          userStatus {
            isSignedIn
            username
          }
        }
        """
        try:
            response = self.session.post(self.GRAPHQL_URL, json={"query": query}, timeout=10)
            if response.status_code != 200:
                print(f"\033[91m[Error] LeetCode server responded with HTTP {response.status_code}\033[0m")
                self.print_auth_warning_and_exit()
                
            data = response.json()
            user_status = data.get("data", {}).get("userStatus", {})
            if not user_status or not user_status.get("isSignedIn", False):
                print("\033[93m[Warning] LeetCode rejected your session. The cookie may have expired.\033[0m")
                self.print_auth_warning_and_exit()
                
            return user_status.get("username", "User")
        except Exception as e:
            print(f"\033[91m[Error] Network error while verifying authentication: {e}\033[0m")
            self.print_auth_warning_and_exit()

    def sanitize_description_html(self, html_content):
        """Converts raw HTML description into clean, readable Markdown-like text."""
        if not html_content:
            return ""
        
        soup = BeautifulSoup(html_content, "html.parser")
        
        # Convert <code> tags to inline backticks
        for code_tag in soup.find_all("code"):
            code_tag.insert_before("`")
            code_tag.insert_after("`")
            code_tag.unwrap()
            
        # Convert bold tags
        for bold_tag in soup.find_all(["strong", "b"]):
            bold_tag.insert_before("**")
            bold_tag.insert_after("**")
            bold_tag.unwrap()
            
        # Convert lists
        for li_tag in soup.find_all("li"):
            li_tag.insert_before("\n* ")
            li_tag.unwrap()
            
        for p_tag in soup.find_all("p"):
            p_tag.insert_before("\n")
            p_tag.unwrap()
            
        # Get raw text
        text = soup.get_text()
        
        # Cleanup extra newlines while preserving single empty line breaks
        lines = [line.rstrip() for line in text.split("\n")]
        cleaned_text = []
        for line in lines:
            if line:
                cleaned_text.append(line)
            elif not cleaned_text or cleaned_text[-1] != "":
                cleaned_text.append("")
                
        return "\n".join(cleaned_text).strip()

    def get_problem_details(self, slug):
        """Retrieves problem title, difficulty, and sanitized description."""
        query = """
        query questionData($titleSlug: String!) {
          question(titleSlug: $titleSlug) {
            title
            content
            difficulty
          }
        }
        """
        try:
            response = self.session.post(
                self.GRAPHQL_URL, 
                json={"query": query, "variables": {"titleSlug": slug}},
                timeout=10
            )
            if response.status_code != 200:
                print(f"\033[91m[Error] Failed to fetch problem details. LeetCode returned HTTP {response.status_code}\033[0m")
                return None
                
            res_json = response.json()
            question = res_json.get("data", {}).get("question")
            if not question:
                print(f"\033[91m[Error] Problem with slug '{slug}' not found on LeetCode.\033[0m")
                return None
                
            raw_html = question.get("content", "")
            sanitized_description = self.sanitize_description_html(raw_html)
            
            return {
                "title": question.get("title", ""),
                "difficulty": question.get("difficulty", "Unknown"),
                "description": sanitized_description
            }
        except Exception as e:
            print(f"\033[91m[Error] Exception during problem details retrieval: {e}\033[0m")
            return None

    def get_latest_accepted_submission(self, slug):
        """Retrieves the user's latest accepted submission code for the given slug."""
        # First, ensure we are signed in
        self.check_authentication()
        
        submission_list_query = """
        query submissionList($questionSlug: String!, $offset: Int, $limit: Int) {
          submissionList(questionSlug: $questionSlug, offset: $offset, limit: $limit) {
            submissions {
              id
              statusDisplay
              lang
              runtime
              timestamp
            }
          }
        }
        """
        try:
            response = self.session.post(
                self.GRAPHQL_URL,
                json={
                    "query": submission_list_query,
                    "variables": {"questionSlug": slug, "offset": 0, "limit": 20}
                },
                timeout=10
            )
            
            if response.status_code != 200:
                print(f"\033[91m[Error] Failed to query submissions list: HTTP {response.status_code}\033[0m")
                self.print_auth_warning_and_exit()
                
            res_json = response.json()
            submissions_data = res_json.get("data", {}).get("submissionList", {})
            if not submissions_data or "submissions" not in submissions_data:
                print("\033[91m[Error] Submissions data structure is missing or malformed.\033[0m")
                self.print_auth_warning_and_exit()
                
            submissions = submissions_data.get("submissions", [])
            if not submissions:
                print(f"\033[91m[Error] No submissions found for problem '{slug}' on your account.\033[0m")
                print("Please submit a solution on LeetCode first, then run this tool.")
                sys.exit(1)
                
            # Filter submissions to locate the latest "Accepted" solution
            accepted_sub = None
            for sub in submissions:
                if sub.get("statusDisplay") == "Accepted":
                    accepted_sub = sub
                    break
                    
            if not accepted_sub:
                print(f"\033[91m[Error] You have submissions for '{slug}', but NONE of them are 'Accepted'.\033[0m")
                print("This tool only extracts successful solutions to avoid generating posts with buggy code.")
                sys.exit(1)
                
            # Fetch the actual code for this submission ID
            submission_id = int(accepted_sub["id"])
            return self.get_submission_details(submission_id)
            
        except Exception as e:
            print(f"\033[91m[Error] Exception during submission extraction: {e}\033[0m")
            self.print_auth_warning_and_exit()

    def get_submission_details(self, submission_id):
        """Retrieves details of a specific submission, including code and language."""
        details_query = """
        query submissionDetails($submissionId: Int!) {
          submissionDetails(submissionId: $submissionId) {
            code
            runtime
            memory
            lang {
              name
              verboseName
            }
          }
        }
        """
        try:
            response = self.session.post(
                self.GRAPHQL_URL,
                json={"query": details_query, "variables": {"submissionId": submission_id}},
                timeout=10
            )
            if response.status_code != 200:
                print(f"\033[91m[Error] Failed to fetch submission details for ID {submission_id}\033[0m")
                self.print_auth_warning_and_exit()
                
            res_json = response.json()
            details = res_json.get("data", {}).get("submissionDetails")
            if not details or not details.get("code"):
                print(f"\033[91m[Error] Empty submission content returned for ID {submission_id}\033[0m")
                self.print_auth_warning_and_exit()
                
            return {
                "id": submission_id,
                "code": details.get("code", ""),
                "runtime": details.get("runtime", ""),
                "memory": details.get("memory", ""),
                "lang_name": details.get("lang", {}).get("name", "python3"),
                "lang_verbose": details.get("lang", {}).get("verboseName", "Python3")
            }
        except Exception as e:
            print(f"\033[91m[Error] Exception during submission details query: {e}\033[0m")
            self.print_auth_warning_and_exit()
