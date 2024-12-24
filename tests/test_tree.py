import os
import sys
from pathlib import Path

# Add the project root directory to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pytest
from pytreeprint.tree import TreeStats, generate_tree

@pytest.fixture
def temp_directory(tmp_path):
    # Create a test directory structure
    (tmp_path / "dir1").mkdir()
    (tmp_path / "dir1" / "file1.txt").write_text("content")
    (tmp_path / "dir2").mkdir()
    (tmp_path / "dir2" / "file2.py").write_text("print('hello')")
    return tmp_path

def test_tree_generation(temp_directory):
    stats = TreeStats()
    tree_output = generate_tree(temp_directory, stats=stats)
    
    # Check if all directories and files are counted
    assert stats.directories == 2
    assert stats.files == 2
    
    # Check if tree structure is correct
    assert len(tree_output) > 0
    assert any("dir1" in line for line in tree_output)
    assert any("dir2" in line for line in tree_output)
    assert any("file1.txt" in line for line in tree_output)
    assert any("file2.py" in line for line in tree_output)

def test_ignore_patterns(temp_directory):
    # Create a file that should be ignored
    (temp_directory / "__pycache__").mkdir()
    (temp_directory / "__pycache__" / "cache.pyc").write_text("")
    
    stats = TreeStats()
    from pytreeprint.tree import compile_ignore_pattern, DEFAULT_IGNORE_PATTERNS
    
    pattern = compile_ignore_pattern(DEFAULT_IGNORE_PATTERNS)
    tree_output = generate_tree(temp_directory, stats=stats, exclude_pattern=pattern)
    
    # Check if pycache is ignored
    assert not any("__pycache__" in line for line in tree_output)
    assert stats.directories == 2  # Only dir1 and dir2