"""Type definitions and shared classes for pytreeprint."""
from pathlib import Path


class TreeStats:
    """Statistics collector for tree generation."""

    def __init__(self):
        self.directories = 0
        self.files = 0
        self.total_size = 0

    def update_from_items(self, files: list[Path], show_size: bool = False) -> None:
        """Update statistics from a list of files."""
        self.files += len(files)
        if show_size:
            self.total_size += sum(f.stat().st_size for f in files)
