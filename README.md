# TreeVI

A Python-based enhanced tree command that displays directory structures with additional features and customization options.
This tool provides a more versatile alternative to the standard Windows `tree` command but probably not as powerful as the `tree` command in Unix-based systems yet.
Helpful for understanding project structure and file distribution, as well as extending the standard `tree` command with additional features.
Uses vary from codebase analysis to project documentation and file management.

It is intended to be __put into a subdirectory of a project__ and __run from the main project directory__ to visualize the project structure in a tree.txt file or console output for now.

## Features

- Windows-style directory tree visualization
- Smart file and directory grouping
- Colorized output for different file types
- File size and timestamp information
- Configurable ignore patterns
- Summary statistics
- Depth control

## Installation

1. Clone this repository
2. Ensure Python 3.6+ is installed
3. Place the script in your project's `scripts` directory

## Usage

```bash
python tree.py [options]
```

### Basic Examples

```bash
# Simple tree view
python tree.py

# Show with colors and file sizes
python tree.py -c -s

# Show everything (including normally ignored directories)
python tree.py --show-all

# Show with file sizes, timestamps, and statistics
python tree.py -c -s -t --stats
```

### Use with node

```bash
# Add script to package.json, append any flags as needed
"scripts": {
  # ...
  # Basic tree view
  "tree": "python scripts/tree.py", 
  # ...
}
```

```bash
# Run with npm
npm run tree
```

### Use with pipenv

```bash
# Add script to Pipfile, append any flags as needed
[scripts]
tree = "python scripts/tree.py"
```

```bash
# Run with pipenv
pipenv run tree
```

### Use with poetry

```bash
# Add script to pyproject.toml, append any flags as needed
[tool.poetry.scripts]
tree = "scripts.tree:main"
```

```bash
# Run with poetry
poetry run tree
```

### Use with `Makefile`

```makefile
# Add a target to your Makefile
tree:
    python scripts/tree.py
```

```bash
# Run with make
make tree
```

### Command Line Options

| Option | Description |
|--------|-------------|
| `-d`, `--max-depth` | Maximum depth to traverse |
| `-s`, `--size` | Show file sizes |
| `-t`, `--time` | Show modification times |
| `-c`, `--color` | Colorize output |
| `--stats` | Show summary statistics |
| `--no-color` | Disable color even if supported |

### Pattern Handling Options

| Option | Description |
|--------|-------------|
| `-i`, `--ignore-pattern` | Additional regex pattern to ignore |
| `-I`, `--ignore-patterns` | File containing patterns to ignore |
| `--no-ignore` | Disable default ignore patterns |
| `--show-all` | Show all files (same as --no-ignore) |

## Default Ignored Patterns

The following patterns are ignored by default (can be disabled with `--no-ignore`):

- `.git` - Git directory
- `.pytest_cache` - Pytest cache
- `.mypy_cache` - MyPy cache
- `__pycache__` - Python cache
- `node_modules` - Node.js modules
- `.vscode` - VSCode settings
- `.idea` - IntelliJ settings
- `.vs` - Visual Studio settings
- `.venv`, `venv`, `env`, `.env` - Virtual environments
- `.tox` - Tox testing
- `.coverage` - Coverage data
- `.sass-cache` - SASS cache
- `.next` - Next.js build
- `dist` - Distribution directories
- `build` - Build directories
- `.*_cache` - Any cache directory

## Color Coding

When using the `-c` option, files are color-coded by type:

- 🔵 Blue - Directories
- 🟢 Green - Executable files (.exe, .sh, .py, etc.)
- 🟡 Yellow - Symlinks
- �cyan Cyan - Media files (images, audio, video)
- 🟣 Magenta - Archives (.zip, .tar, etc.)
- 🔴 Red - Special files (config files, json, etc.)

## Output Example

```powershell
Directory of D:\Project

├───README.md [2.5KB] [2024-01-24 15:30]
├───setup.py [1.2KB]
├───src
│   ├───main.py
│   └───utils
│       ├───helper.py
│       └───config.json
└───tests
    └───test_main.py

Summary:
Directories: 3
Files: 5
Total size: 15.7KB
```

## Output Files

The command generates a `tree.txt` file in the root directory containing the tree structure. When using colors, the console output will be colored while the file output remains plain text for better compatibility.

## Requirements

- Python 3.6 or higher
- No additional dependencies required

## TODOs

### High Priority

- [ ] Rename and publish as a package on PyPI, modify script to be a CLI entry point
- [ ] Add support for custom output formats (JSON, XML, YAML)
- [ ] Add pattern support for file extensions (e.g., show only *.py files)
- [ ] Allow specifying a start directory as command-line argument
- [ ] Add file permission display option (Unix-style)
- [ ] Support for `.treeignore` file in project root (similar to .gitignore)

### Nice to Have

- [ ] Add interactive mode with real-time directory navigation
- [ ] Export to different formats (HTML, Markdown, PDF)
- [ ] Add Git status integration (show modified/untracked files)
- [ ] Support for custom color schemes via config file
- [ ] Add search functionality with glob patterns
- [ ] Add size comparison between different runs
- [ ] Add progress bar for large directories
- [ ] Add option for horizontal tree layout

### Future Considerations

- [ ] Add network share/remote filesystem support
- [ ] Create GUI interface with collapsible tree
- [ ] Add plugin system for custom file type handlers
- [ ] Support for archive inspection (peek into zip/tar files)
- [ ] Add multi-language support for output
- [ ] Create system tray monitoring for directory changes

## License

GPL-3.0 License, see [LICENSE](LICENSE.txt) for details.

## Credits

This project was inspired by the standard `tree` command and aims to provide a more feature-rich alternative for Windows users. Feel free to contribute or suggest new features to enhance the tool further. Pull requests are welcome!

## Contact / Author

For issues, suggestions, or feedback, please contact the author at <https://github.com/soulwax>
