"""Tests for the pytreeprint package."""
import sys
from pathlib import Path
import pytest

from pytreeprint.tree import (
    TreeStats,
    generate_tree,
    compile_ignore_pattern,
    DEFAULT_IGNORE_PATTERNS,
)

# Add project root to Python path for test imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


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

    stats = TreeStats()
    tree_output = generate_tree(
        directory=mock_directory,
        max_depth=1,
        stats=stats,
    )

    # Verify depth limitation
    assert not any("level2" in line for line in tree_output)
    assert any("level1" in line for line in tree_output)
