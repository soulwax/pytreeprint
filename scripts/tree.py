#!/usr/bin/env python3
# File: scripts/tree.py
# Copyright (c) 2025, Konstantin Kling, Germany, https://github.com/soulwax

import os
from pathlib import Path
import re
import argparse
from datetime import datetime
import sys
from typing import Optional, Tuple, Dict, Set, List

# Default patterns to ignore (can be overridden)
DEFAULT_IGNORE_PATTERNS = {
    r'^\.git$',              # Git directory
    r'^\.pytest_cache$',     # Pytest cache
    r'^\.mypy_cache$',       # MyPy cache
    r'^__pycache__$',        # Python cache
    r'^node_modules$',       # Node.js modules
    r'^\.vscode$',           # VSCode settings
    r'^\.idea$',             # IntelliJ settings
    r'^\.vs$',              # Visual Studio settings
    r'^\.venv$',            # Virtual environment
    r'^venv$',              # Virtual environment
    r'^env$',               # Virtual environment
    r'^\.env$',             # Environment variables
    r'^\.tox$',             # Tox testing
    r'^\.coverage$',         # Coverage data
    r'^\.sass-cache$',       # SASS cache
    r'^\.next$',            # Next.js build
    r'^dist$',              # Distribution directories
    r'^build$',             # Build directories
    r'^\..+_cache$',        # Any cache directory
}

# ANSI color codes
COLORS = {
    'reset': '\033[0m',
    'blue': '\033[94m',     # directories
    'green': '\033[92m',    # executable files
    'yellow': '\033[93m',   # symlinks
    'cyan': '\033[96m',     # media files
    'magenta': '\033[95m',  # archives
    'red': '\033[91m',      # special files
}

FILE_COLORS = {
    # Executables
    '.exe': 'green', '.sh': 'green', '.bat': 'green', '.cmd': 'green', '.ps1': 'green', '.py': 'green',
    # Media
    '.mp3': 'cyan', '.wav': 'cyan', '.flac': 'cyan', '.m4a': 'cyan', '.ogg': 'cyan',
    '.mp4': 'cyan', '.avi': 'cyan', '.mkv': 'cyan', '.mov': 'cyan',
    '.jpg': 'cyan', '.jpeg': 'cyan', '.png': 'cyan', '.gif': 'cyan', '.bmp': 'cyan',
    # Archives
    '.zip': 'magenta', '.rar': 'magenta', '.7z': 'magenta', '.tar': 'magenta', '.gz': 'magenta',
    # Special
    '.json': 'red', '.xml': 'red', '.yaml': 'red', '.yml': 'red', '.ini': 'red', '.conf': 'red'
}

class TreeStats:
    def __init__(self):
        self.directories = 0
        self.files = 0
        self.total_size = 0

def get_size_str(size: int) -> str:
    """Convert size in bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.1f}{unit}"
        size /= 1024
    return f"{size:.1f}PB"

def compile_ignore_pattern(patterns: Set[str]) -> Optional[re.Pattern]:
    """Compile multiple patterns into a single regex pattern"""
    if not patterns:
        return None
    combined_pattern = '|'.join(f'(?:{pattern})' for pattern in patterns)
    return re.compile(combined_pattern)

def parse_pattern_file(file_path: str) -> Set[str]:
    """Parse a file containing ignore patterns"""
    patterns = set()
    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    patterns.add(line)
    except Exception as e:
        print(f"Warning: Could not read pattern file {file_path}: {e}", file=sys.stderr)
    return patterns

def get_color_for_file(path: Path, use_color: bool) -> Tuple[str, str]:
    """Get the color code for a file and its reset code"""
    if not use_color:
        return '', ''
    
    if path.is_dir():
        return COLORS['blue'], COLORS['reset']
    elif path.is_symlink():
        return COLORS['yellow'], COLORS['reset']
    else:
        color = FILE_COLORS.get(path.suffix.lower(), '')
        return COLORS.get(color, ''), COLORS['reset']

def get_file_info(path: Path, show_size: bool, show_date: bool) -> str:
    """Get additional file information based on flags"""
    info_parts = []
    
    if show_size and path.is_file():
        size = path.stat().st_size
        info_parts.append(f"[{get_size_str(size)}]")
    
    if show_date:
        mtime = datetime.fromtimestamp(path.stat().st_mtime)
        info_parts.append(mtime.strftime("[%Y-%m-%d %H:%M]"))
    
    return " ".join(info_parts)

def generate_tree(
    directory: Path,
    prefix: str = "",
    is_last: bool = True,
    max_depth: Optional[int] = None,
    current_depth: int = 0,
    stats: TreeStats = None,
    exclude_pattern: Optional[re.Pattern] = None,
    show_size: bool = False,
    show_date: bool = False,
    use_color: bool = False
) -> list[str]:
    """Generate a Windows-style ASCII tree structure for the given directory."""
    if stats is None:
        stats = TreeStats()
    
    if max_depth is not None and current_depth > max_depth:
        return []
    
    lines = []
    
    # Separate and sort files and directories
    items = list(directory.iterdir())
    files = sorted([f for f in items if f.is_file()], key=lambda x: x.name.lower())
    dirs = sorted([d for d in items if d.is_dir()], key=lambda x: x.name.lower())
    
    # Filter out excluded items
    if exclude_pattern:
        files = [f for f in files if not exclude_pattern.match(f.name)]
        dirs = [d for d in dirs if not exclude_pattern.match(d.name)]
    
    # Update stats
    stats.directories += len(dirs)
    stats.files += len(files)
    if show_size:
        stats.total_size += sum(f.stat().st_size for f in files)
    
    # Process all files first
    for index, item in enumerate(files):
        is_last_item = (index == len(files) - 1) and not dirs
        connector = "└───" if is_last_item else "├───"
        
        # Get color and additional info
        color_start, color_end = get_color_for_file(item, use_color)
        info = get_file_info(item, show_size, show_date)
        info = f" {info}" if info else ""
        
        lines.append(f"{prefix}{connector}{color_start}{item.name}{color_end}{info}")
    
    # Then process all directories
    for index, item in enumerate(dirs):
        is_last_item = index == len(dirs) - 1
        connector = "└───" if is_last_item else "├───"
        
        # Get color for directory
        color_start, color_end = get_color_for_file(item, use_color)
        info = get_file_info(item, show_size, show_date)
        info = f" {info}" if info else ""
        
        # Add the directory
        lines.append(f"{prefix}{connector}{color_start}{item.name}{color_end}{info}")
        
        # Process the directory's contents
        new_prefix = prefix + ("    " if is_last_item else "│   ")
        lines.extend(generate_tree(
            item, new_prefix, is_last_item, max_depth, current_depth + 1,
            stats, exclude_pattern, show_size, show_date, use_color
        ))
    
    return lines

def main():
    parser = argparse.ArgumentParser(description='Generate a directory tree structure')
    parser.add_argument('-d', '--max-depth', type=int, help='Maximum depth to traverse')
    parser.add_argument('-s', '--size', action='store_true', help='Show file sizes')
    parser.add_argument('-t', '--time', action='store_true', help='Show modification times')
    parser.add_argument('-c', '--color', action='store_true', help='Colorize output')
    parser.add_argument('--stats', action='store_true', help='Show summary statistics')
    parser.add_argument('--no-color', action='store_true', help='Disable color even if supported')
    
    # Pattern handling arguments
    ignore_group = parser.add_mutually_exclusive_group()
    ignore_group.add_argument('-i', '--ignore-pattern', type=str, help='Additional regex pattern to ignore')
    ignore_group.add_argument('-I', '--ignore-patterns', type=str, help='File containing patterns to ignore')
    ignore_group.add_argument('--no-ignore', action='store_true', help='Disable default ignore patterns')
    ignore_group.add_argument('--show-all', action='store_true', help='Show all files (same as --no-ignore)')
    
    args = parser.parse_args()

    # Get the project root (one directory up from the script location)
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent
    os.chdir(project_root)
    
    # Handle ignore patterns
    patterns_to_ignore = set()
    
    if not (args.no_ignore or args.show_all):
        # Start with default patterns
        patterns_to_ignore.update(DEFAULT_IGNORE_PATTERNS)
        
        # Add additional patterns if specified
        if args.ignore_pattern:
            patterns_to_ignore.add(args.ignore_pattern)
        elif args.ignore_patterns:
            patterns_to_ignore.update(parse_pattern_file(args.ignore_patterns))
    
    # Compile the ignore pattern
    exclude_pattern = compile_ignore_pattern(patterns_to_ignore)
    
    # Check if color should be enabled
    use_color = args.color and not args.no_color and sys.stdout.isatty()
    
    # Initialize stats
    stats = TreeStats()
    
    # Generate tree output
    lines = [f"\nDirectory of {project_root}\n"]
    
    if patterns_to_ignore:
        lines.append("Ignored patterns:")
        for pattern in sorted(patterns_to_ignore):
            lines.append(f"  {pattern}")
        lines.append("")
    
    # Get all items in the root directory
    items = list(project_root.iterdir())
    files = sorted([f for f in items if f.is_file()], key=lambda x: x.name.lower())
    dirs = sorted([d for d in items if d.is_dir()], key=lambda x: x.name.lower())
    
    if exclude_pattern:
        files = [f for f in files if not exclude_pattern.match(f.name)]
        dirs = [d for d in dirs if not exclude_pattern.match(d.name)]
    
    # Update root stats
    stats.directories += len(dirs)
    stats.files += len(files)
    if args.size:
        stats.total_size += sum(f.stat().st_size for f in files)
    
    # Process files first
    for index, item in enumerate(files):
        is_last = index == len(files) - 1 and not dirs
        connector = "└───" if is_last else "├───"
        color_start, color_end = get_color_for_file(item, use_color)
        info = get_file_info(item, args.size, args.time)
        info = f" {info}" if info else ""
        lines.append(f"{connector}{color_start}{item.name}{color_end}{info}")
    
    # Then process directories
    for index, item in enumerate(dirs):
        is_last = index == len(dirs) - 1
        connector = "└───" if is_last else "├───"
        color_start, color_end = get_color_for_file(item, use_color)
        info = get_file_info(item, args.size, args.time)
        info = f" {info}" if info else ""
        
        lines.append(f"{connector}{color_start}{item.name}{color_end}{info}")
        subtree = generate_tree(
            item, "    " if is_last else "│   ", is_last, args.max_depth, 1,
            stats, exclude_pattern, args.size, args.time, use_color
        )
        lines.extend(subtree)
    
    # Add summary statistics if requested
    if args.stats:
        lines.append("\nSummary:")
        lines.append(f"Directories: {stats.directories}")
        lines.append(f"Files: {stats.files}")
        if args.size:
            lines.append(f"Total size: {get_size_str(stats.total_size)}")
    
    # Write to file using Windows-style line endings
    with open('tree.txt', 'w', encoding='utf-8', newline='\r\n') as f:
        f.write('\n'.join(lines))
    
    # Also print to console with colors
    print('\n'.join(lines))
    
    print(f"\nTree structure has been written to {project_root / 'tree.txt'}")

if __name__ == '__main__':
    main()