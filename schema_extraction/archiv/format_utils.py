import re

def clean_body(text):
    if not text:
        return ""
    # Optional: Basic cleaning of common artifacts if needed
    return text.strip()

def format_issue_as_markdown(issue_data, repo_full_name):
    """
    Converts issue data (from GitHub API) into a clean Markdown string.
    """
    issue_number = issue_data.get('number')
    title = issue_data.get('title')
    user = issue_data.get('user', {}).get('login')
    state = issue_data.get('state')
    created_at = issue_data.get('created_at')
    body = clean_body(issue_data.get('body'))
    
    md = [
        f"# Issue #{issue_number}: {title}",
        f"**Repository:** {repo_full_name}",
        f"**Author:** {user}",
        f"**Status:** {state}",
        f"**Created At:** {created_at}",
        "",
        "## Description",
        body,
        ""
    ]
    
    return "\n".join(md)

def format_comment_as_markdown(comment_data):
    """
    Converts a single comment into Markdown format.
    """
    user = comment_data.get('user', {}).get('login')
    created_at = comment_data.get('created_at')
    body = clean_body(comment_data.get('body'))
    
    md = [
        f"### Comment by {user} at {created_at}",
        body,
        ""
    ]
    return "\n".join(md)

def format_discussion_as_markdown(discussion_node, repo_full_name):
    """
    Converts discussion data (from GraphQL) into Markdown.
    """
    number = discussion_node.get('number')
    title = discussion_node.get('title')
    user = discussion_node.get('author', {}).get('login') if discussion_node.get('author') else "ghost"
    created_at = discussion_node.get('createdAt')
    body = clean_body(discussion_node.get('body'))
    
    md = [
        f"# Discussion #{number}: {title}",
        f"**Repository:** {repo_full_name}",
        f"**Author:** {user}",
        f"**Created At:** {created_at}",
        "",
        "## Description",
        body,
        ""
    ]
    
    # Add comments if present in the node
    comments_data = discussion_node.get('comments', {}).get('edges', [])
    if comments_data:
        md.append("## Comments")
        for edge in comments_data:
            comment_node = edge.get('node', {})
            md.append(format_discussion_comment_as_markdown(comment_node))
            
    return "\n".join(md)

def format_discussion_comment_as_markdown(comment_node):
    """
    Converts a single discussion comment into Markdown format.
    """
    user = comment_node.get('author', {}).get('login') if comment_node.get('author') else "ghost"
    created_at = comment_node.get('createdAt')
    body = clean_body(comment_node.get('body'))
    
    md = [
        f"### Comment by {user} at {created_at}",
        body,
        ""
    ]
    return "\n".join(md)
