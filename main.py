from fastmcp import FastMCP
import random
import subprocess
import os
import uuid

mcp = FastMCP("Debug Lab Generator")

WORKSPACE = "workspaces"
os.makedirs(WORKSPACE, exist_ok=True)


@mcp.tool
def create_workspace() -> str:
    """Create a new debugging workspace"""
    session_id = str(uuid.uuid4())[:8]
    path = os.path.join(WORKSPACE, session_id)
    os.makedirs(path, exist_ok=True)
    return path


BASE_WORKSPACE = "D:\\mcp_workspaces"

@mcp.tool
def clone_repo(repo_url: str) -> str:
    repo_name = repo_url.split("/")[-1].replace(".git", "")
    repo_path = os.path.join(BASE_WORKSPACE, repo_name)

    os.makedirs(BASE_WORKSPACE, exist_ok=True)

    try:
        subprocess.run(
            ["git", "clone", "--depth", "1", repo_url, repo_path],
            check=True,
            timeout=120
        )
    except subprocess.TimeoutExpired:
        return "Clone operation timed out"
    except subprocess.CalledProcessError as e:
        return f"Git error: {e}"

    return f"Repo cloned successfully to {repo_path}"


@mcp.tool
def inject_python_bug(file_path: str) -> str:
    """Inject a simple bug into a python file"""

    bug_types = [
        ("==", "="),
        ("True", "true"),
        ("None", "null"),
    ]

    with open(file_path, "r") as f:
        code = f.read()

    bug = random.choice(bug_types)
    buggy_code = code.replace(bug[0], bug[1], 1)

    with open(file_path, "w") as f:
        f.write(buggy_code)

    return f"Injected bug: replaced {bug[0]} with {bug[1]}"


@mcp.tool
def list_workspace_files(workspace: str) -> list:
    """List files in a workspace"""
    return os.listdir(workspace)


@mcp.tool
def generate_debug_hint() -> str:
    """Generate a hint for the debugging challenge"""

    hints = [
        "Check comparison operators carefully.",
        "Look for incorrect variable types.",
        "Check environment variables.",
        "Look for dependency version mismatches.",
        "Check indentation or syntax errors."
    ]

    return random.choice(hints)


if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)