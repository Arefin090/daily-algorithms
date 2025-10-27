from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from dataclasses import dataclass


@dataclass
class ProblemContent:
    """Represents a single algorithmic problem/solution."""
    title: str
    file_path: str
    content: str
    language: str
    source_url: str
    description: Optional[str] = None
    difficulty: Optional[str] = None
    tags: List[str] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []


class BaseSource(ABC):
    """Abstract base class for problem sources."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.name = config.get('name', 'Unknown')
        self.enabled = config.get('enabled', True)
    
    @abstractmethod
    def fetch_available_problems(self) -> List[Dict[str, Any]]:
        """Fetch list of available problems from the source."""
        pass
    
    @abstractmethod
    def get_problem_content(self, problem_info: Dict[str, Any]) -> Optional[ProblemContent]:
        """Get detailed content for a specific problem."""
        pass
    
    def is_enabled(self) -> bool:
        """Check if this source is enabled."""
        return self.enabled
    
    def get_source_name(self) -> str:
        """Get the source name."""
        return self.name