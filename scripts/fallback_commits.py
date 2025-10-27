#!/usr/bin/env python3
"""
Fallback commit system to ensure daily green squares.
This runs when the main algorithm fetcher fails.
"""

import os
import random
from datetime import datetime
from typing import Optional
import glob

def create_daily_reflection() -> str:
    """Create a simple daily learning reflection."""
    today = datetime.now().strftime('%Y-%m-%d')
    
    reflections = [
        "Reviewing algorithm fundamentals",
        "Practicing problem-solving patterns", 
        "Exploring data structure concepts",
        "Analyzing time complexity",
        "Understanding space complexity",
        "Studying algorithm design patterns",
        "Reviewing sorting techniques",
        "Exploring graph algorithms",
        "Understanding dynamic programming",
        "Practicing recursive thinking"
    ]
    
    reflection = random.choice(reflections)
    
    # Create or update learning log
    log_path = "learning_log.md"
    
    if not os.path.exists(log_path):
        content = f"""# Algorithm Learning Log

Daily reflections and progress tracking.

## {today}
- {reflection}
"""
    else:
        with open(log_path, 'r') as f:
            existing = f.read()
        
        content = existing + f"""
## {today}
- {reflection}
"""
    
    with open(log_path, 'w') as f:
        f.write(content)
    
    return log_path

def update_random_notes() -> Optional[str]:
    """Update notes in a random existing problem folder."""
    problems_dir = "problems"
    
    if not os.path.exists(problems_dir):
        return None
    
    # Find all problem folders
    problem_folders = [f for f in os.listdir(problems_dir) 
                      if os.path.isdir(os.path.join(problems_dir, f))]
    
    if not problem_folders:
        return None
    
    # Pick a random folder
    selected_folder = random.choice(problem_folders)
    folder_path = os.path.join(problems_dir, selected_folder)
    notes_path = os.path.join(folder_path, "notes.md")
    
    if not os.path.exists(notes_path):
        return None
    
    # Read existing notes
    with open(notes_path, 'r') as f:
        content = f.read()
    
    # Add a learning insight
    insights = [
        "- Reviewed implementation details",
        "- Analyzed edge cases", 
        "- Considered optimization opportunities",
        "- Compared with alternative approaches",
        "- Noted practical applications",
        "- Identified related problems",
        "- Studied complexity trade-offs"
    ]
    
    insight = random.choice(insights)
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Add insight to personal notes section
    if "## Personal Notes" in content:
        content = content.replace(
            "## Personal Notes",
            f"## Personal Notes\n\n### {today}\n{insight}"
        )
    else:
        content += f"\n\n### {today}\n{insight}"
    
    with open(notes_path, 'w') as f:
        f.write(content)
    
    return notes_path

def create_progress_update() -> str:
    """Create a simple progress tracking file."""
    today = datetime.now().strftime('%Y-%m-%d')
    progress_path = "PROGRESS.md"
    
    milestones = [
        "Consistent daily learning habit",
        "Algorithm pattern recognition improving", 
        "Problem-solving confidence growing",
        "Understanding complexity analysis better",
        "Building algorithmic intuition",
        "Expanding problem-solving toolkit"
    ]
    
    milestone = random.choice(milestones)
    
    if not os.path.exists(progress_path):
        content = f"""# Learning Progress

Tracking algorithm study journey.

## {today}
✅ {milestone}
"""
    else:
        with open(progress_path, 'r') as f:
            existing = f.read()
        
        content = existing + f"""
## {today}
✅ {milestone}
"""
    
    with open(progress_path, 'w') as f:
        f.write(content)
    
    return progress_path

def execute_fallback() -> tuple[str, str]:
    """Execute fallback strategy and return (file_path, commit_message)."""
    
    # Strategy 1: Update existing problem notes
    updated_file = update_random_notes()
    if updated_file:
        problem_name = os.path.basename(os.path.dirname(updated_file)).split('_', 1)[1].replace('-', ' ').title()
        return updated_file, f"Update {problem_name} notes"
    
    # Strategy 2: Create daily reflection
    reflection_file = create_daily_reflection()
    return reflection_file, "Add daily learning reflection"

if __name__ == "__main__":
    file_path, commit_msg = execute_fallback()
    print(f"Created fallback commit: {commit_msg}")
    print(f"File: {file_path}")