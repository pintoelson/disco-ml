import requests
import os
import yaml
import json
from pathlib import Path
from format_utils import format_issue_as_markdown, format_comment_as_markdown, format_discussion_as_markdown

GITHUB_API_BASE = "https://api.github.com"
GITHUB_GRAPHQL_URL = "https://api.github.com/graphql"

def get_config(config_path="config.yaml"):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def load_dotenv(dotenv_path):
    if os.path.exists(dotenv_path):
        print("Loading environment variables from .env...")
        with open(dotenv_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    if '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip().strip('"').strip("'")

def fetch_issues(repo, token=None):
    url = f"{GITHUB_API_BASE}/repos/{repo}/issues"
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"
    
    params = {"state": "all", "per_page": 100}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def fetch_comments(repo, issue_number, token=None):
    url = f"{GITHUB_API_BASE}/repos/{repo}/issues/{issue_number}/comments"
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def fetch_discussions(repo, token=None):
    owner, name = repo.split('/')
    query = """
    query($owner: String!, $name: String!) {
      repository(owner: $owner, name: $name) {
        discussions(first: 50, orderBy: {field: CREATED_AT, direction: DESC}) {
          edges {
            node {
              number
              title
              body
              createdAt
              author {
                login
              }
              comments(first: 50) {
                edges {
                  node {
                    author {
                      login
                    }
                    createdAt
                    body
                  }
                }
              }
            }
          }
        }
      }
    }
    """
    variables = {"owner": owner, "name": name}
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    
    response = requests.post(
        GITHUB_GRAPHQL_URL,
        json={'query': query, 'variables': variables},
        headers=headers
    )
    response.raise_for_status()
    data = response.json()
    if 'errors' in data:
        raise Exception(f"GraphQL Errors: {data['errors']}")
    return data['data']['repository']['discussions']['edges']

def main():
    base_dir = Path(__file__).parent
    load_dotenv(base_dir.parent / ".env")
    config = get_config(base_dir / "config.yaml")
    repos = config.get('repositories', [])
    token = os.getenv("GITHUB_TOKEN")
    
    if not token:
        print("Warning: GITHUB_TOKEN not found. Rate limits will be strict.")
    
    issues_dir = base_dir / "issues"
    os.makedirs(issues_dir, exist_ok=True)
    
    for repo in repos:
        repo_dir = issues_dir / repo.replace("/", "_")
        os.makedirs(repo_dir, exist_ok=True)
        
        print(f"Fetching issues for {repo}...")
        try:
            issues = fetch_issues(repo, token)
            print(f"  API returned {len(issues)} items.")
            for issue in issues:
                is_pr = 'pull_request' in issue
                prefix = "pr" if is_pr else "issue"
                issue_number = issue['number']
                
                file_path = os.path.join(repo_dir, f"{prefix}_{issue_number}.md")
                
                if os.path.exists(file_path):
                    continue
                
                print(f"  Processing {prefix.capitalize()} #{issue_number}: {issue['title']}")
                md_content = format_issue_as_markdown(issue, repo)
                
                try:
                    comments = fetch_comments(repo, issue_number, token)
                    if comments:
                        md_content += "\n## Comments\n"
                        for comment in comments:
                            md_content += format_comment_as_markdown(comment)
                except Exception as e:
                    print(f"    Warning: Could not fetch comments for #{issue_number}: {e}")
                
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(md_content)
            
            # Fetch Discussions
            print(f"Fetching discussions for {repo}...")
            discussions = fetch_discussions(repo, token)
            print(f"  API returned {len(discussions)} discussions.")
            for edge in discussions:
                node = edge['node']
                number = node['number']
                file_path = os.path.join(repo_dir, f"discussion_{number}.md")
                
                if os.path.exists(file_path):
                    continue
                
                print(f"  Processing Discussion #{number}: {node['title']}")
                md_content = format_discussion_as_markdown(node, repo)
                
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(md_content)
                    
        except Exception as e:
            print(f"Error processing repository {repo}: {e}")

if __name__ == "__main__":
    main()
