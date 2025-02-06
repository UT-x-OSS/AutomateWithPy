import os
import subprocess
from pathlib import Path


def find_git_repos(root_dir):
    git_repos = []
    for dirpath, dirnames, _ in os.walk(root_dir):
        if ".git" in dirnames:
            git_repos.append(Path(dirpath).resolve())
            # not pulling in .git directories
            dirnames[:] = [d for d in dirnames if d != ".git"]
    return git_repos


def get_current_branch(repo_path):
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error getting branch for {repo_path}: {e.stderr}")
        return None


def git_pull(repo_path, branch):
    try:
        result = subprocess.run(
            ["git", "pull", "origin", branch],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True,
        )
        print(f"Successfully pulled {repo_path} ({branch})")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error pulling {repo_path} ({branch}): {e.stderr}")


def main():
    root_dir = input("Enter root directory path (default: current dir): ") or "."
    repos = find_git_repos(root_dir)

    if not repos:
        print("No Git repositories found")
        return

    print(f"Found {len(repos)} repositories:")
    for repo in repos:
        print(f" - {repo}")

    print("\nStarting pull operations...")
    for repo in repos:
        print(f"\nProcessing {repo}")
        branch = get_current_branch(repo)
        if branch:
            git_pull(repo, branch)
        else:
            print(f"Skipping {repo} - couldn't determine current branch")


if __name__ == "__main__":
    main()
