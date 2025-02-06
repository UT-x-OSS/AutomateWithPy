## Copyright 2025 kawakibulula
##
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at
##
##     http://www.apache.org/licenses/LICENSE-2.0
##
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.

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
