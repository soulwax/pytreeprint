"""Tests for the pytreeprint package."""
import pytest
from pathlib import Path

from pytreeprint.types import TreeStats
from pytreeprint.tree import (
    generate_tree,
    compile_ignore_pattern,
    DEFAULT_IGNORE_PATTERNS
)


@pytest.fixture
def mock_directory(tmp_path):
    """Create a mock directory structure for testing."""
    # Create test directories
    dir1 = tmp_path / "dir1"
    dir2 = tmp_path / "dir2"
    dir1.mkdir()
    dir2.mkdir()

    # Create test files
    (dir1 / "file1.txt").write_text("content")
    (dir2 / "file2.py").write_text("print('hello')")

    return tmp_path


def test_tree_generation(mock_directory):
    """Test basic tree generation functionality."""
    stats = TreeStats()
    tree_output = generate_tree(
        directory=mock_directory,
        stats=stats,
        show_size=True,
        show_date=True,
    )

    # Verify statistics
    assert stats.directories == 2
    assert stats.files == 2

    # Verify tree structure
    assert len(tree_output) > 0
    assert any("dir1" in line for line in tree_output)
    assert any("dir2" in line for line in tree_output)
    assert any("file1.txt" in line for line in tree_output)
    assert any("file2.py" in line for line in tree_output)


def test_ignore_patterns(mock_directory):
    """Test pattern-based file/directory ignoring."""
    # Create an ignored directory
    pycache_dir = mock_directory / "__pycache__"
    pycache_dir.mkdir()
    (pycache_dir / "module.cpython-39.pyc").write_text("")

    stats = TreeStats()
    pattern = compile_ignore_pattern(DEFAULT_IGNORE_PATTERNS)
    tree_output = generate_tree(
        directory=mock_directory,
        stats=stats,
        exclude_pattern=pattern,
    )

    # Verify ignored items
    assert not any("__pycache__" in line for line in tree_output)
    assert stats.directories == 2  # Should only count dir1 and dir2


def test_empty_directory(tmp_path):
    """Test tree generation with empty directory."""
    stats = TreeStats()
    tree_output = generate_tree(directory=tmp_path, stats=stats)

    assert stats.directories == 0
    assert stats.files == 0
    assert not tree_output  # Should be empty list


def test_max_depth(mock_directory):
    """Test max depth limitation."""
    # Create nested directories
    nested = mock_directory / "level1" / "level2" / "level3"
    nested.mkdir(parents=True)
    (nested / "deep_file.txt").write_text("deep")

    # Create a file in level1 to ensure depth check works correctly
    (mock_directory / "level1" / "shallow_file.txt").write_text("shallow")

    stats = TreeStats()
    tree_output = generate_tree(
        directory=mock_directory,
        max_depth=1,
        stats=stats,
    )

    # Verify depth limitation
    assert any("level1" in line for line in tree_output)
    assert any("shallow_file.txt" in line for line in tree_output)
    assert not any("level2" in line for line in tree_output)
    assert not any("level3" in line for line in tree_output)
    assert not any("deep_file.txt" in line for line in tree_output)
