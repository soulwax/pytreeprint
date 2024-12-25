# pytreeprint

A Python-based enhanced tree command that displays directory structures with additional features and customization options.

## Prerequisites

- Python 3.8 or higher
- No additional dependencies required

## Overview

`pytreeprint` is a versatile command-line tool for visualizing directory structures. It provides more features than the standard Windows `tree` command and offers rich customization for project analysis, documentation, and file management.

## Features

- 📂 Detailed directory tree visualization
- 🎨 Colorized output with file type-based coloring
- 📏 Optional file size display
- 🕒 Optional timestamp information
- 🚫 Configurable ignore patterns
- 📊 Summary statistics
- 🌲 Depth control

## Installation **(PENDING PUBLISHING)**

Install directly from PyPI:

```bash
pip install pytreeprint
```

Until it is published, you can clone the repository and run the script directly:

```bash
git clone https://github.com/soulwax/pytreeprint.git
```

Then run the script from the root directory:

```bash
pip install -e . 
```

This installs the package as editable, create a symlink to the script globally while changes are reflected immediately.

Then:

## Usage

### Basic tree view

```shell
pytreeprint
```

### Show with colors and file sizes

```shell
pytreeprint -c -s
```

### Show everything (including normally ignored directories)

```shell
pytreeprint --show-all
```

### Show with file sizes, timestamps, and statistics

```shell
pytreeprint -c -s -t --stats
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
- 💠 Cyan - Media files (images, audio, video)
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

- [x] Rename and publish as a package on PyPI, modify script to be a CLI entry point
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

GPL-3.0 License, see [LICENSE](LICENSE) for details.

## Credits

This project was inspired by the standard `tree` command and aims to provide a more feature-rich alternative for Windows users. Feel free to contribute or suggest new features to enhance the tool further.

## Contact / Author

**For issues, suggestions, or feedback, please contact the author at <https://github.com/soulwax>, or create a new issue on GitHub, or submit a pull request, any feedback is welcome.**
