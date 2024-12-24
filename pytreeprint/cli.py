"""Command line interface for pytreeprint."""
from pathlib import Path
from re import Pattern
import sys
import argparse
from typing import Set, Optional

from .tree import (TreeStats, generate_tree, get_color_for_file,
                   get_file_info, compile_ignore_pattern, parse_pattern_file,
                   DEFAULT_IGNORE_PATTERNS)
from .utils import process_directory_items


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        description='Generate a directory tree structure')
    parser.add_argument('path', nargs='?', default='.',
                        help='Directory path to map (default: current directory)')
    parser.add_argument('-d', '--max-depth', type=int,
                        help='Maximum depth to traverse')
    parser.add_argument('-s', '--size', action='store_true',
                        help='Show file sizes')
    parser.add_argument('-t', '--time', action='store_true',
                        help='Show modification times')
    parser.add_argument('-c', '--color', action='store_true',
                        help='Colorize output')
    parser.add_argument('-o', '--output', type=str,
                        help='Output file path (default: tree.txt in target directory)')
    parser.add_argument('--stats', action='store_true',
                        help='Show summary statistics')
    parser.add_argument('--no-color', action='store_true',
                        help='Disable color even if supported')

    ignore_group = parser.add_mutually_exclusive_group()
    ignore_group.add_argument('-i', '--ignore-pattern', type=str,
                              help='Additional regex pattern to ignore')
    ignore_group.add_argument('-I', '--ignore-patterns', type=str,
                              help='File containing patterns to ignore')
    ignore_group.add_argument('--no-ignore', action='store_true',
                              help='Disable default ignore patterns')
    ignore_group.add_argument('--show-all', action='store_true',
                              help='Show all files (same as --no-ignore)')

    return parser


def get_ignore_patterns(args) -> Set[str]:
    """Determine which patterns to ignore based on arguments."""
    if args.no_ignore or args.show_all:
        return set()

    patterns = set(DEFAULT_IGNORE_PATTERNS)
    if args.ignore_pattern:
        patterns.add(args.ignore_pattern)
    elif args.ignore_patterns:
        patterns.update(parse_pattern_file(args.ignore_patterns))

    return patterns


def process_root_directory(
    directory: Path,
    stats: TreeStats,
    exclude_pattern: Optional[Pattern],
    args
) -> list[str]:
    """Process the root directory and generate initial output lines."""
    lines = [f"\nDirectory of {directory}\n"]

    items = list(directory.iterdir())
    files, dirs = process_directory_items(items, stats, exclude_pattern)

    if args.size:
        stats.total_size += sum(f.stat().st_size for f in files)

    # Process files
    for index, item in enumerate(files):
        is_last = index == len(files) - 1 and not dirs
        connector = "└───" if is_last else "├───"
        color_start, color_end = get_color_for_file(item, args.color)
        info = get_file_info(item, args.size, args.time)
        info = f" {info}" if info else ""
        lines.append(f"{connector}{color_start}{item.name}{color_end}{info}")

    # Process directories
    for index, item in enumerate(dirs):
        is_last = index == len(dirs) - 1
        connector = "└───" if is_last else "├───"
        color_start, color_end = get_color_for_file(item, args.color)
        info = get_file_info(item, args.size, args.time)
        info = f" {info}" if info else ""

        lines.append(f"{connector}{color_start}{item.name}{color_end}{info}")
        subtree = generate_tree(
            directory=item,
            prefix="    " if is_last else "│   ",
            max_depth=args.max_depth,
            current_depth=1,
            stats=stats,
            exclude_pattern=exclude_pattern,
            show_size=args.size,
            show_date=args.time,
            use_color=args.color
        )
        lines.extend(subtree)

    return lines


def main() -> None:
    """Main entry point for the CLI."""
    parser = create_parser()
    args = parser.parse_args()

    # Validate directory
    target_dir = Path(args.path).resolve()
    if not target_dir.exists():
        print(
            f"Error: Directory '{args.path}' does not exist", file=sys.stderr)
        sys.exit(1)
    if not target_dir.is_dir():
        print(f"Error: '{args.path}' is not a directory", file=sys.stderr)
        sys.exit(1)

    # Setup
    patterns_to_ignore = get_ignore_patterns(args)
    exclude_pattern = compile_ignore_pattern(patterns_to_ignore)
    use_color = args.color and not args.no_color and sys.stdout.isatty()
    stats = TreeStats()
    output_file = args.output if args.output else target_dir / 'tree.txt'

    # Generate tree
    lines = process_root_directory(target_dir, stats, exclude_pattern, args)

    # Add statistics if requested
    if args.stats:
        lines.extend([
            "\nSummary:",
            f"Directories: {stats.directories}",
            f"Files: {stats.files}",
            *(f"Total size: {stats.total_size}" if args.size else [])
        ])

    # Write output
    with open(output_file, 'w', encoding='utf-8', newline='\r\n') as f:
        f.write('\n'.join(lines))

    print('\n'.join(lines))
    print(f"\nTree structure has been written to {output_file}")


if __name__ == '__main__':
    main()
