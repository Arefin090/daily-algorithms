#!/usr/bin/env python3
"""
Multiple commit strategies to create natural-looking activity.
"""

import os
import random
from datetime import datetime
from typing import Optional, List, Tuple
import json

def add_algorithm_study() -> Tuple[str, str]:
    """Add a new algorithm - main strategy."""
    from fetch_problem import ProblemFetcher
    
    fetcher = ProblemFetcher()
    if fetcher.fetch_daily_problem():
        # Find latest problem folder
        problems_dir = 'problems'
        if os.path.exists(problems_dir):
            folders = [f for f in os.listdir(problems_dir) 
                     if os.path.isdir(os.path.join(problems_dir, f))]
            if folders:
                latest = max(folders)
                title = latest.split('_', 1)[1].replace('-', ' ').title()
                return os.path.join(problems_dir, latest), f"Add {title} algorithm"
    
    return None, None

def improve_existing_notes() -> Tuple[str, str]:
    """Enhance notes in existing problem."""
    problems_dir = "problems"
    
    if not os.path.exists(problems_dir):
        return None, None
    
    folders = [f for f in os.listdir(problems_dir) 
              if os.path.isdir(os.path.join(problems_dir, f))]
    
    if not folders:
        return None, None
    
    # Pick random folder
    folder = random.choice(folders)
    notes_path = os.path.join(problems_dir, folder, "notes.md")
    
    if not os.path.exists(notes_path):
        return None, None
    
    with open(notes_path, 'r') as f:
        content = f.read()
    
    # Add study insights
    insights = [
        "- Edge case: empty input handling",
        "- Optimization: early termination condition", 
        "- Alternative: iterative vs recursive approach",
        "- Memory usage: O(1) space optimization possible",
        "- Performance: best/average/worst case analysis",
        "- Real-world application in search engines",
        "- Comparison with similar algorithms",
        "- Implementation variant in different languages"
    ]
    
    insight = random.choice(insights)
    
    # Add to personal notes section
    if "## Personal Notes" in content:
        content = content.replace(
            "## Personal Notes",
            f"## Personal Notes\n\n{insight}"
        )
    else:
        content += f"\n\n{insight}"
    
    with open(notes_path, 'w') as f:
        f.write(content)
    
    problem_name = folder.split('_', 1)[1].replace('-', ' ').title()
    return notes_path, f"Update {problem_name} analysis"

def refactor_code() -> Tuple[str, str]:
    """Make small code improvements."""
    problems_dir = "problems"
    
    if not os.path.exists(problems_dir):
        return None, None
    
    folders = [f for f in os.listdir(problems_dir) 
              if os.path.isdir(os.path.join(problems_dir, f))]
    
    if not folders:
        return None, None
    
    # Find solution files
    for folder in random.sample(folders, min(3, len(folders))):
        folder_path = os.path.join(problems_dir, folder)
        for file in os.listdir(folder_path):
            if file.startswith('solution.') and file.endswith(('.py', '.java')):
                file_path = os.path.join(folder_path, file)
                
                with open(file_path, 'r') as f:
                    content = f.read()
                
                # Make small improvements
                improvements = [
                    ('\t', '    '),  # Convert tabs to spaces
                    ('  \n', '\n'),  # Remove trailing spaces
                    ('\n\n\n', '\n\n'),  # Fix multiple newlines
                ]
                
                original = content
                for old, new in improvements:
                    content = content.replace(old, new)
                
                if content != original:
                    with open(file_path, 'w') as f:
                        f.write(content)
                    
                    problem_name = folder.split('_', 1)[1].replace('-', ' ').title()
                    return file_path, f"Refactor {problem_name} implementation"
    
    return None, None

def update_documentation() -> Tuple[str, str]:
    """Small documentation updates."""
    
    files_to_update = ['README.md']
    
    for file_path in files_to_update:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Minor improvements
            improvements = [
                ('## Sources', '## Algorithm Sources'),
                ('## Notes', '## Study Notes'),
                ('study notes', 'learning notes'),
                ('problems and solutions', 'algorithmic problems and solutions'),
            ]
            
            for old, new in improvements:
                if old in content and new not in content:
                    content = content.replace(old, new)
                    
                    with open(file_path, 'w') as f:
                        f.write(content)
                    
                    return file_path, "Update documentation"
    
    return None, None

def get_commit_strategy() -> Tuple[str, str]:
    """Choose and execute a commit strategy."""
    
    strategies = [
        (add_algorithm_study, 0.6),      # 60% - new algorithms
        (improve_existing_notes, 0.25),  # 25% - improve notes  
        (refactor_code, 0.1),            # 10% - code improvements
        (update_documentation, 0.05),    # 5% - documentation
    ]
    
    # Weighted random selection
    rand = random.random()
    cumulative = 0
    
    for strategy, weight in strategies:
        cumulative += weight
        if rand <= cumulative:
            try:
                file_path, commit_msg = strategy()
                if file_path and commit_msg:
                    return file_path, commit_msg
            except Exception as e:
                print(f"Strategy {strategy.__name__} failed: {e}")
                continue
    
    # Final fallback
    return update_documentation()