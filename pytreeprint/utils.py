"""Utility functions for directory tree processing."""
from pathlib import Path
from typing import List, Tuple, Optional, Pattern

from .tree import TreeStats


def process_directory_items(
    items: List[Path],
    stats: TreeStats,
    exclude_pattern: Optional[Pattern] = None,
) -> Tuple[List[Path], List[Path]]:
    """Process directory items, sorting them and updating statistics."""
    files = sorted([f for f in items if f.is_file()],
                   key=lambda x: x.name.lower())
    dirs = sorted([d for d in items if d.is_dir()],
                  key=lambda x: x.name.lower())

    if exclude_pattern:
        files = [f for f in files if not exclude_pattern.match(f.name)]
        dirs = [d for d in dirs if not exclude_pattern.match(d.name)]

    stats.directories += len(dirs)
    stats.files += len(files)

    return files, dirs
