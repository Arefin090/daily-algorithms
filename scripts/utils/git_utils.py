import subprocess
import os
from typing import Optional


def git_add_and_commit(folder_path: str, commit_message: str) -> bool:
    """Add files and create a git commit."""
    try:
        # Add all changes (new files, modifications, etc.)
        subprocess.run(['git', 'add', '.'], check=True, cwd=os.getcwd())
        
        # Check if there are changes to commit
        result = subprocess.run(['git', 'diff', '--cached', '--quiet'], 
                              cwd=os.getcwd(), capture_output=True)
        
        if result.returncode != 0:  # There are changes
            subprocess.run(['git', 'commit', '-m', commit_message], 
                          check=True, cwd=os.getcwd())
            return True
        else:
            print("No changes to commit")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"Git operation failed: {e}")
        return False


def git_push() -> bool:
    """Push commits to remote repository."""
    try:
        subprocess.run(['git', 'push'], check=True, cwd=os.getcwd())
        return True
    except subprocess.CalledProcessError as e:
        print(f"Git push failed: {e}")
        return False


def get_git_status() -> Optional[str]:
    """Get current git status."""
    try:
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True, cwd=os.getcwd())
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None


def is_git_repo() -> bool:
    """Check if current directory is a git repository."""
    try:
        subprocess.run(['git', 'rev-parse', '--git-dir'], 
                      check=True, capture_output=True, cwd=os.getcwd())
        return True
    except subprocess.CalledProcessError:
        return False