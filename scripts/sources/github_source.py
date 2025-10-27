import requests
import base64
import re
import os
import time
from typing import Dict, List, Optional, Any
from .base_source import BaseSource, ProblemContent


class GitHubSource(BaseSource):
    """GitHub repository source for algorithmic problems."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.owner = config['owner']
        self.repo = config['repo']
        self.base_path = config.get('base_path', '')
        self.file_patterns = config.get('file_patterns', ['*.py'])
        self.exclude_patterns = config.get('exclude_patterns', [])
        self.api_base = 'https://api.github.com'
        self.headers = {}
        
        # Use GitHub token if available for higher rate limits
        github_token = os.environ.get('GITHUB_TOKEN')
        if github_token:
            self.headers['Authorization'] = f'token {github_token}'
    
    def fetch_available_problems(self) -> List[Dict[str, Any]]:
        """Fetch Python files from specific algorithm directories."""
        try:
            # Instead of fetching all files, target specific algorithm directories
            algorithm_dirs = [
                'sorts', 'searches', 'data_structures/binary_tree',
                'data_structures/linked_list', 'dynamic_programming',
                'graph', 'backtracking', 'greedy', 'divide_and_conquer'
            ]
            
            all_files = []
            for directory in algorithm_dirs:
                try:
                    files = self._get_repository_files(directory)
                    all_files.extend(files)
                    time.sleep(0.1)  # Rate limiting
                except Exception as e:
                    print(f"Could not fetch from {directory}: {e}")
                    continue
            
            filtered_files = self._filter_files(all_files)
            return [{'path': f['path'], 'sha': f['sha'], 'url': f['url']} for f in filtered_files]
        except Exception as e:
            print(f"Error fetching from {self.name}: {e}")
            return []
    
    def get_problem_content(self, problem_info: Dict[str, Any]) -> Optional[ProblemContent]:
        """Get content for a specific file."""
        try:
            url = f"{self.api_base}/repos/{self.owner}/{self.repo}/contents/{problem_info['path']}"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            data = response.json()
            content = base64.b64decode(data['content']).decode('utf-8')
            
            # Extract metadata from content
            title = self._extract_title_from_path(problem_info['path'])
            description = self._extract_description_from_content(content)
            language = self._get_language_from_extension(problem_info['path'])
            tags = self._extract_tags_from_path(problem_info['path'])
            
            source_url = f"https://github.com/{self.owner}/{self.repo}/blob/master/{problem_info['path']}"
            
            return ProblemContent(
                title=title,
                file_path=problem_info['path'],
                content=content,
                language=language,	
                source_url=source_url,
                description=description,
                tags=tags
            )
        except Exception as e:
            print(f"Error getting content for {problem_info['path']}: {e}")
            return None
    
    def _get_repository_files(self, path: str = '') -> List[Dict[str, Any]]:
        """Recursively get all files from repository."""
        url = f"{self.api_base}/repos/{self.owner}/{self.repo}/contents/{path}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        
        items = response.json()
        files = []
        
        for item in items:
            if item['type'] == 'file':
                files.append(item)
            elif item['type'] == 'dir' and not self._should_exclude_path(item['path']):
                files.extend(self._get_repository_files(item['path']))
        
        return files
    
    def _filter_files(self, files: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filter files based on patterns."""
        filtered = []
        for file in files:
            path = file['path']
            
            # Check if file should be excluded
            if self._should_exclude_path(path):
                continue
            
            # Check if file matches include patterns
            if self._matches_patterns(path, self.file_patterns):
                filtered.append(file)
        
        return filtered
    
    def _should_exclude_path(self, path: str) -> bool:
        """Check if path should be excluded."""
        return any(pattern in path.lower() for pattern in self.exclude_patterns)
    
    def _matches_patterns(self, path: str, patterns: List[str]) -> bool:
        """Check if path matches any of the patterns."""
        for pattern in patterns:
            if pattern.startswith('*.'):
                extension = pattern[2:]
                if path.lower().endswith(f'.{extension}'):
                    return True
            elif pattern in path:
                return True
        return False
    
    def _extract_title_from_path(self, path: str) -> str:
        """Extract a readable title from file path."""
        filename = path.split('/')[-1]
        name = filename.split('.')[0]
        
        # Convert snake_case or camelCase to Title Case
        title = re.sub(r'[_-]', ' ', name)
        title = re.sub(r'([a-z])([A-Z])', r'\1 \2', title)
        return title.title()
    
    def _extract_description_from_content(self, content: str) -> Optional[str]:
        """Extract description from file content (docstrings, comments)."""
        lines = content.split('\n')
        description_lines = []
        
        # Look for docstrings or initial comments
        in_docstring = False
        docstring_quotes = None
        
        for line in lines:
            stripped = line.strip()
            
            if not stripped or stripped.startswith('#'):
                if stripped.startswith('#'):
                    desc = stripped[1:].strip()
                    if desc:
                        description_lines.append(desc)
                continue
            
            # Handle docstrings
            if '"""' in stripped or "'''" in stripped:
                if not in_docstring:
                    in_docstring = True
                    docstring_quotes = '"""' if '"""' in stripped else "'''"
                    desc = stripped.replace(docstring_quotes, '').strip()
                    if desc:
                        description_lines.append(desc)
                else:
                    desc = stripped.replace(docstring_quotes, '').strip()
                    if desc:
                        description_lines.append(desc)
                    in_docstring = False
                    break
            elif in_docstring:
                description_lines.append(stripped)
            else:
                break
        
        return '\n'.join(description_lines[:3]) if description_lines else None
    
    def _get_language_from_extension(self, path: str) -> str:
        """Get programming language from file extension."""
        extension = path.split('.')[-1].lower()
        language_map = {
            'py': 'python',
            'java': 'java',
            'js': 'javascript',
            'cpp': 'cpp',
            'c': 'c',
            'go': 'go',
            'rs': 'rust'
        }
        return language_map.get(extension, extension)
    
    def _extract_tags_from_path(self, path: str) -> List[str]:
        """Extract tags from file path."""
        tags = []
        path_parts = path.split('/')
        
        # Use directory names as tags
        for part in path_parts[:-1]:  # Exclude filename
            if part and not part.startswith('.'):
                # Clean up directory names
                tag = re.sub(r'[_-]', ' ', part).title()
                tags.append(tag)
        
        return tags