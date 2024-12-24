#!/usr/bin/env python3
import os
from pathlib import Path
import re
import argparse
from datetime import datetime
import sys
from typing import Optional, Tuple, Dict, Set, List
from .tree import (
    TreeStats, generate_tree, get_size_str, get_color_for_file,
    get_file_info, compile_ignore_pattern, parse_pattern_file,
    DEFAULT_IGNORE_PATTERNS
)

def main():
    parser = argparse.ArgumentParser(description='Generate a directory tree structure')
    parser.add_argument('path', nargs='?', default='.', help='Directory path to map (default: current directory)')
    parser.add_argument('-d', '--max-depth', type=int, help='Maximum depth to traverse')
    parser.add_argument('-s', '--size', action='store_true', help='Show file sizes')
    parser.add_argument('-t', '--time', action='store_true', help='Show modification times')
    parser.add_argument('-c', '--color', action='store_true', help='Colorize output')
    parser.add_argument('-o', '--output', type=str, help='Output file path (default: tree.txt in target directory)')
    parser.add_argument('--stats', action='store_true', help='Show summary statistics')
    parser.add_argument('--no-color', action='store_true', help='Disable color even if supported')
    
    ignore_group = parser.add_mutually_exclusive_group()
    ignore_group.add_argument('-i', '--ignore-pattern', type=str, help='Additional regex pattern to ignore')
    ignore_group.add_argument('-I', '--ignore-patterns', type=str, help='File containing patterns to ignore')
    ignore_group.add_argument('--no-ignore', action='store_true', help='Disable default ignore patterns')
    ignore_group.add_argument('--show-all', action='store_true', help='Show all files (same as --no-ignore)')
    
    args = parser.parse_args()

    target_dir = Path(args.path).resolve()
    if not target_dir.exists():
        print(f"Error: Directory '{args.path}' does not exist", file=sys.stderr)
        sys.exit(1)
    if not target_dir.is_dir():
        print(f"Error: '{args.path}' is not a directory", file=sys.stderr)
        sys.exit(1)

    patterns_to_ignore = set()
    if not (args.no_ignore or args.show_all):
        patterns_to_ignore.update(DEFAULT_IGNORE_PATTERNS)
        if args.ignore_pattern:
            patterns_to_ignore.add(args.ignore_pattern)
        elif args.ignore_patterns:
            patterns_to_ignore.update(parse_pattern_file(args.ignore_patterns))

    exclude_pattern = compile_ignore_pattern(patterns_to_ignore)
    use_color = args.color and not args.no_color and sys.stdout.isatty()
    stats = TreeStats()
    output_file = args.output if args.output else target_dir / 'tree.txt'
    
    lines = [f"\nDirectory of {target_dir}\n"]
    if patterns_to_ignore:
        lines.append("Ignored patterns:")
        for pattern in sorted(patterns_to_ignore):
            lines.append(f"  {pattern}")
        lines.append("")

    items = list(target_dir.iterdir())
    files = sorted([f for f in items if f.is_file()], key=lambda x: x.name.lower())
    dirs = sorted([d for d in items if d.is_dir()], key=lambda x: x.name.lower())
    
    if exclude_pattern:
        files = [f for f in files if not exclude_pattern.match(f.name)]
        dirs = [d for d in dirs if not exclude_pattern.match(d.name)]
    
    stats.directories += len(dirs)
    stats.files += len(files)
    if args.size:
        stats.total_size += sum(f.stat().st_size for f in files)
    
    for index, item in enumerate(files):
        is_last = index == len(files) - 1 and not dirs
        connector = "└───" if is_last else "├───"
        color_start, color_end = get_color_for_file(item, use_color)
        info = get_file_info(item, args.size, args.time)
        info = f" {info}" if info else ""
        lines.append(f"{connector}{color_start}{item.name}{color_end}{info}")
    
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
    
    if args.stats:
        lines.append("\nSummary:")
        lines.append(f"Directories: {stats.directories}")
        lines.append(f"Files: {stats.files}")
        if args.size:
            lines.append(f"Total size: {get_size_str(stats.total_size)}")
    
    with open(output_file, 'w', encoding='utf-8', newline='\r\n') as f:
        f.write('\n'.join(lines))
    
    print('\n'.join(lines))
    print(f"\nTree structure has been written to {output_file}")

if __name__ == '__main__':
    main()