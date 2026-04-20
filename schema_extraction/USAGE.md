# Usage Instructions - GitHub Issue Extraction

This tool extracts issues from GitHub repositories and converts them into structured Markdown files for LLM processing.

## Getting Started

### 1. Prerequisites
Ensure you have the necessary dependencies installed:
```bash
pip install -r requirements.txt
```

### 2. Configuration
Define the repositories you want to extract issues from in `config.yaml`:
```yaml
repositories:
  - "owner/repo"
```

### 3. Authentication (Optional)
To avoid GitHub API rate limits, it is highly recommended to use a Personal Access Token.
```bash
export GITHUB_TOKEN=your_personal_access_token
```

## Running the tool
Run the extraction script:
```bash
python extract_issues.py
```

## Features
- **Incremental Extraction**: The script checks the `issues/` folder and skips issues that have already been converted to Markdown.
- **PR Filtering**: Pull requests are automatically excluded from the extraction.
- **Comment Inclusion**: All comments associated with an issue are fetched and appended to the Markdown file.
- **LLM-Friendly Format**: Outputs are structured with clear headings and metadata for optimal context retrieval by LLMs.

## Directory Structure
- `issues/{owner}_{repo}/`: Contains individual `.md` files for each issue.
- `extract_issues.py`: Main execution script.
- `format_utils.py`: Markdown formatting logic.
- `config.yaml`: Repository configuration.
