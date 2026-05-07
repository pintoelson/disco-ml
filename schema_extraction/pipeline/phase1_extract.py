import os
import yaml
import json
import requests
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from .models import GitHubItem, GitHubComment

GITHUB_API_BASE = "https://api.github.com"
GITHUB_GRAPHQL_URL = "https://api.github.com/graphql"

def get_config(config_path):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def fetch_issues(repo, token=None, limit=10):
    url = f"{GITHUB_API_BASE}/repos/{repo}/issues"
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"
    
    params = {"state": "all", "per_page": 100}
    issues = []
    
    while url:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        page_issues = response.json()
        issues.extend(page_issues)
        
        if limit > 0 and len(issues) >= limit:
            issues = issues[:limit]
            break
            
        if 'next' in response.links:
            url = response.links['next']['url']
            params = {}  # params are included in the next URL
        else:
            break
            
    return issues

def fetch_single_issue(repo, issue_number, token=None):
    url = f"{GITHUB_API_BASE}/repos/{repo}/issues/{issue_number}"
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"
    
    response = requests.get(url, headers=headers)
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

def run_phase1(limit: int = 10, issue_number: int = None):
    base_dir = Path(__file__).parent.parent
    load_dotenv(base_dir.parent / ".env")
    config = get_config(base_dir / "config.yaml")
    repos = config.get('repositories', [])
    token = os.getenv("GITHUB_TOKEN")
    
    if not token:
        print("Warning: GITHUB_TOKEN not found. Rate limits will be strict.")
    
    raw_dir = Path(__file__).parent / "data" / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    
    for repo in repos:
        repo_safe = repo.replace("/", "_")
        repo_dir = raw_dir / repo_safe
        repo_dir.mkdir(exist_ok=True)
        
        if issue_number:
            print(f"Fetching single issue #{issue_number} for {repo}...")
            try:
                issue = fetch_single_issue(repo, issue_number, token)
                issues = [issue]
            except Exception as e:
                print(f"Error fetching issue #{issue_number} from {repo}: {e}")
                continue
        else:
            print(f"Fetching up to {limit} issues for {repo}...")
            try:
                issues = fetch_issues(repo, token, limit=limit)
            except Exception as e:
                print(f"Error processing repository {repo}: {e}")
                continue

        print(f"  API returned {len(issues)} items.")
        for issue in issues:
            is_pr = 'pull_request' in issue
            item_type = "pr" if is_pr else "issue"
            issue_num = issue['number']
            
            file_path = repo_dir / f"{item_type}_{issue_num}.json"
            if file_path.exists():
                print(f"  Skipping {item_type.capitalize()} #{issue_num} (already exists)")
                continue
            
            print(f"  Processing {item_type.capitalize()} #{issue_num}: {issue['title']}")
            import time
            time.sleep(0.5) # Sleep to avoid secondary rate limits
            # Fetch comments
            try:
                comments_data = fetch_comments(repo, issue_num, token)
            except Exception as e:
                print(f"    Warning: Could not fetch comments for #{issue_num}: {e}")
                comments_data = []
            
            comments = []
            for c in comments_data:
                comments.append(GitHubComment(
                    id=str(c['id']),
                    author=c['user']['login'] if c.get('user') else 'unknown',
                    timestamp=datetime.strptime(c['created_at'], "%Y-%m-%dT%H:%M:%SZ"),
                    body=c['body'] or ""
                ))
            
            item = GitHubItem(
                id=str(issue['id']),
                item_type=item_type,
                number=issue_num,
                title=issue['title'],
                body=issue['body'] or "",
                author=issue['user']['login'] if issue.get('user') else 'unknown',
                timestamp=datetime.strptime(issue['created_at'], "%Y-%m-%dT%H:%M:%SZ"),
                status=issue['state'],
                comments=comments
            )
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(item.model_dump_json(indent=2))

if __name__ == "__main__":
    run_phase1()
