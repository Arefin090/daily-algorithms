#!/usr/bin/env python3
"""
Algorithm Collection Script

Fetches algorithmic problems from various sources and organizes them
into a structured learning repository.
"""

import os
import sys
import random
from datetime import datetime
from typing import List, Dict, Any, Optional

# Add the scripts directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sources.github_source import GitHubSource
from sources.base_source import BaseSource, ProblemContent
from utils.file_utils import (
    load_json_file, save_json_file, create_daily_folder,
    create_readme_file, create_solution_file, create_notes_file,
    is_file_already_processed, mark_file_as_processed, get_unprocessed_problems
)
from utils.git_utils import git_add_and_commit, git_push, is_git_repo


class ProblemFetcher:
    """Main class for fetching and processing algorithmic problems."""
    
    def __init__(self, config_dir: str = 'config'):
        self.config_dir = config_dir
        self.sources_config = load_json_file(os.path.join(config_dir, 'sources.json'))
        self.processed_data = load_json_file(os.path.join(config_dir, 'processed.json'))
        self.sources: List[BaseSource] = []
        self._initialize_sources()
    
    def _initialize_sources(self):
        """Initialize source objects from configuration."""
        sources_list = self.sources_config.get('sources', [])
        
        for source_config in sources_list:
            if not source_config.get('enabled', True):
                continue
                
            source_type = source_config.get('type', '').lower()
            
            if source_type == 'github':
                source = GitHubSource(source_config)
                self.sources.append(source)
            else:
                print(f"Warning: Unknown source type '{source_type}' for {source_config.get('name')}")
    
    def fetch_daily_problem(self) -> bool:
        """Fetch and process a single problem for today."""
        if not self.sources:
            print("No enabled sources found!")
            return False
        
        # Collect all available problems from all sources
        all_candidates = []
        
        for source in self.sources:
            print(f"Fetching problems from {source.get_source_name()}...")
            try:
                problems = source.fetch_available_problems()
                unprocessed = get_unprocessed_problems(problems, self.processed_data, source.get_source_name())
                
                for problem in unprocessed:
                    all_candidates.append((source, problem))
                
                print(f"Found {len(unprocessed)} unprocessed problems from {source.get_source_name()}")
            except Exception as e:
                print(f"Error fetching from {source.get_source_name()}: {e}")
                continue
        
        if not all_candidates:
            print("No unprocessed problems found across all sources!")
            return False
        
        # Randomly select one problem
        selected_source, selected_problem = random.choice(all_candidates)
        print(f"Selected: {selected_problem['path']} from {selected_source.get_source_name()}")
        
        # Get problem content
        problem_content = selected_source.get_problem_content(selected_problem)
        if not problem_content:
            print("Failed to fetch problem content!")
            return False
        
        # Create daily folder and files
        folder_path = create_daily_folder('.', problem_content.title)
        folder_name = os.path.basename(folder_path)
        
        create_readme_file(folder_path, problem_content)
        create_solution_file(folder_path, problem_content)
        create_notes_file(folder_path, problem_content)
        
        # Mark as processed
        mark_file_as_processed(
            self.processed_data,
            selected_problem['path'],
            selected_source.get_source_name(),
            folder_name
        )
        
        # Save updated processed data
        processed_file_path = os.path.join(self.config_dir, 'processed.json')
        save_json_file(processed_file_path, self.processed_data)
        
        print(f"Created daily problem folder: {folder_path}")
        return True
    
    def commit_and_push(self, folder_path: str, problem_title: str) -> bool:
        """Commit changes and push to repository."""
        if not is_git_repo():
            print("Not in a git repository, skipping commit")
            return False
        
        commit_message = f"Add {problem_title} algorithm"
        
        if git_add_and_commit(folder_path, commit_message):
            print("Changes committed successfully")
            
            if git_push():
                print("Changes pushed to remote repository")
                return True
            else:
                print("Failed to push changes")
                return False
        else:
            print("No changes to commit")
            return False
    
    def run(self) -> bool:
        """Main entry point to fetch daily problem."""
        print(f"Starting algorithm collection at {datetime.now()}")
        
        try:
            success = self.fetch_daily_problem()
            if success:
                # Find the most recently created folder
                problems_dir = 'problems'
                if os.path.exists(problems_dir):
                    folders = [f for f in os.listdir(problems_dir) 
                             if os.path.isdir(os.path.join(problems_dir, f))]
                    if folders:
                        latest_folder = max(folders)
                        folder_path = os.path.join(problems_dir, latest_folder)
                        
                        # Extract title from folder name
                        title_part = latest_folder.split('_', 1)[1] if '_' in latest_folder else latest_folder
                        title = title_part.replace('-', ' ').title()
                        
                        self.commit_and_push(folder_path, title)
                
                print("Algorithm collection completed successfully!")
                return True
            else:
                print("Primary algorithm fetch failed, executing fallback...")
                return self._execute_fallback()
                
        except Exception as e:
            print(f"Error during problem fetch: {e}")
            print("Executing fallback strategy...")
            return self._execute_fallback()
    
    def _execute_fallback(self) -> bool:
        """Execute fallback strategy to ensure daily commit."""
        try:
            # Import fallback module
            import sys
            sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
            from fallback_commits import execute_fallback
            
            file_path, commit_msg = execute_fallback()
            
            if self.commit_and_push_fallback(file_path, commit_msg):
                print(f"Fallback completed successfully: {commit_msg}")
                return True
            else:
                print("Fallback commit failed")
                return False
                
        except Exception as e:
            print(f"Fallback execution failed: {e}")
            return False
    
    def commit_and_push_fallback(self, file_path: str, commit_message: str) -> bool:
        """Commit fallback changes and push."""
        if not is_git_repo():
            print("Not in a git repository, skipping commit")
            return False
        
        if git_add_and_commit(file_path, commit_message):
            print("Fallback changes committed successfully")
            
            if git_push():
                print("Fallback changes pushed to remote repository")
                return True
            else:
                print("Failed to push fallback changes")
                return False
        else:
            print("No fallback changes to commit")
            return False


def main():
    """Main function."""
    # Change to script directory to ensure relative paths work
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(os.path.dirname(script_dir))
    
    fetcher = ProblemFetcher()
    success = fetcher.run()
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()