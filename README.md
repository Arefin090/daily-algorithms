# Daily Algorithms

A collection of algorithmic problems and solutions for continuous learning.

## About

This repository organizes algorithmic problems from various open-source collections into a structured format for study and practice. Each problem gets its own dated folder with the original solution, documentation, and space for personal notes.

## Structure

```
problems/
├── 2024-10-27_binary-search/
│   ├── README.md          # Problem description and metadata
│   ├── solution.py        # Original implementation
│   └── notes.md          # Personal learning notes
└── 2024-10-28_merge-sort/
    ├── README.md
    ├── solution.py
    └── notes.md
```

## Sources

Currently collecting from:
- [TheAlgorithms/Python](https://github.com/TheAlgorithms/Python) - Comprehensive algorithm implementations
- More sources can be added via `config/sources.json`

## Usage

The repository updates daily with new problems automatically. You can also run manually:

```bash
python scripts/fetch_problem.py
```

## Configuration

Edit `config/sources.json` to:
- Enable/disable sources
- Add new algorithm repositories  
- Filter by file types or patterns

## Dependencies

```bash
pip install -r requirements.txt
```

## Learning Notes

Each problem folder includes a `notes.md` template for:
- Key concepts and complexity analysis
- Personal insights and observations
- Related problems and patterns
- Implementation variations

Perfect for building a comprehensive algorithm knowledge base over time.