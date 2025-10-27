import os
import json
from datetime import datetime
from typing import Dict, Any, List
from slugify import slugify


def load_json_file(file_path: str) -> Dict[str, Any]:
    """Load JSON file with error handling."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        print(f"Warning: Invalid JSON in {file_path}, returning empty dict")
        return {}


def save_json_file(file_path: str, data: Dict[str, Any]) -> bool:
    """Save data to JSON file."""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving JSON file {file_path}: {e}")
        return False


def create_daily_folder(base_path: str, title: str) -> str:
    """Create a dated folder for today's problem."""
    today = datetime.now().strftime('%Y-%m-%d')
    slug = slugify(title, max_length=50)
    folder_name = f"{today}_{slug}"
    folder_path = os.path.join(base_path, 'problems', folder_name)
    
    os.makedirs(folder_path, exist_ok=True)
    return folder_path


def create_readme_file(folder_path: str, problem_content) -> str:
    """Create README.md file for the problem."""
    readme_content = f"""# {problem_content.title}

**Source**: [{problem_content.source_url}]({problem_content.source_url})
**Language**: {problem_content.language.title()}
**Path**: `{problem_content.file_path}`

## Description

{problem_content.description or 'No description available.'}

## Tags

{', '.join([f'`{tag}`' for tag in problem_content.tags]) if problem_content.tags else 'No tags'}

---

*Automatically fetched on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    readme_path = os.path.join(folder_path, 'README.md')
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    return readme_path


def create_solution_file(folder_path: str, problem_content) -> str:
    """Create solution file with the original content."""
    extension_map = {
        'python': 'py',
        'java': 'java',
        'javascript': 'js',
        'cpp': 'cpp',
        'c': 'c',
        'go': 'go',
        'rust': 'rs'
    }
    
    extension = extension_map.get(problem_content.language.lower(), 'txt')
    solution_path = os.path.join(folder_path, f'solution.{extension}')
    
    with open(solution_path, 'w', encoding='utf-8') as f:
        f.write(problem_content.content)
    
    return solution_path


def create_notes_file(folder_path: str, problem_content) -> str:
    """Create notes.md file for personal notes."""
    notes_content = f"""# Notes for {problem_content.title}

## Key Concepts

- 

## Time Complexity

- 

## Space Complexity

- 

## Personal Notes

- 

## Related Problems

- 

---

*Add your learning notes here*
"""
    
    notes_path = os.path.join(folder_path, 'notes.md')
    with open(notes_path, 'w', encoding='utf-8') as f:
        f.write(notes_content)
    
    return notes_path


def is_file_already_processed(processed_data: Dict[str, Any], file_path: str, source_name: str) -> bool:
    """Check if a file has already been processed."""
    processed_files = processed_data.get('processed_files', [])
    
    for processed in processed_files:
        if (processed.get('file_path') == file_path and 
            processed.get('source') == source_name):
            return True
    
    return False


def mark_file_as_processed(processed_data: Dict[str, Any], file_path: str, source_name: str, folder_name: str) -> None:
    """Mark a file as processed."""
    if 'processed_files' not in processed_data:
        processed_data['processed_files'] = []
    
    processed_data['processed_files'].append({
        'file_path': file_path,
        'source': source_name,
        'folder_name': folder_name,
        'processed_date': datetime.now().isoformat()
    })
    
    processed_data['last_updated'] = datetime.now().isoformat()


def get_unprocessed_problems(all_problems: List[Dict[str, Any]], processed_data: Dict[str, Any], source_name: str) -> List[Dict[str, Any]]:
    """Filter out already processed problems."""
    unprocessed = []
    
    for problem in all_problems:
        if not is_file_already_processed(processed_data, problem['path'], source_name):
            unprocessed.append(problem)
    
    return unprocessed