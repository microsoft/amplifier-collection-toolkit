"""
Unit tests for file operations utilities.

Tests file discovery, JSON operations, retries, and validation.
"""

import json
from pathlib import Path
from unittest.mock import patch

import pytest
from amplifier_collection_toolkit.file_ops import append_jsonl
from amplifier_collection_toolkit.file_ops import discover_files
from amplifier_collection_toolkit.file_ops import read_json
from amplifier_collection_toolkit.file_ops import safe_read_text
from amplifier_collection_toolkit.file_ops import safe_write_text
from amplifier_collection_toolkit.file_ops import validate_path_exists
from amplifier_collection_toolkit.file_ops import write_json

# Test discover_files


def test_discover_files_single_file(tmp_path):
    """Test discover_files with a single file path."""
    test_file = tmp_path / "test.md"
    test_file.write_text("content")

    result = discover_files(test_file)

    assert len(result) == 1
    assert result[0] == test_file


def test_discover_files_directory_recursive(sample_markdown_files):
    """Test discover_files finds files recursively."""
    result = discover_files(sample_markdown_files, "**/*.md")

    assert len(result) == 3
    assert all(f.suffix == ".md" for f in result)


def test_discover_files_with_max_items(sample_markdown_files):
    """Test discover_files respects max_items limit."""
    result = discover_files(sample_markdown_files, "**/*.md", max_items=2)

    assert len(result) == 2


def test_discover_files_sorted_output(sample_markdown_files):
    """Test discover_files returns sorted results."""
    result = discover_files(sample_markdown_files, "**/*.md")

    # Results should be sorted
    assert result == sorted(result)


def test_discover_files_non_recursive_pattern_warning(sample_markdown_files, caplog):
    """Test discover_files warns about non-recursive patterns."""
    discover_files(sample_markdown_files, "*.md")

    assert "not recursive" in caplog.text.lower()


def test_discover_files_accepts_string_path(sample_markdown_files):
    """Test discover_files accepts str path (not just Path)."""
    result = discover_files(str(sample_markdown_files), "**/*.md")

    assert len(result) == 3
    assert all(isinstance(f, Path) for f in result)


def test_discover_files_invalid_path():
    """Test discover_files raises error for invalid path."""
    with pytest.raises(ValueError, match="neither file nor directory"):
        discover_files("/nonexistent/path", "**/*.md")


# Test write_json


def test_write_json_basic(tmp_path):
    """Test basic JSON writing."""
    output_file = tmp_path / "output.json"
    data = {"key": "value", "number": 42}

    write_json(data, output_file)

    assert output_file.exists()
    loaded = json.loads(output_file.read_text())
    assert loaded == data


def test_write_json_creates_parent_directory(tmp_path):
    """Test write_json creates parent directories."""
    output_file = tmp_path / "nested" / "dir" / "output.json"
    data = {"test": "data"}

    write_json(data, output_file)

    assert output_file.exists()
    assert output_file.parent.exists()


def test_write_json_with_indent(tmp_path):
    """Test write_json formats with indentation."""
    output_file = tmp_path / "output.json"
    data = {"key": "value"}

    write_json(data, output_file, indent=4)

    content = output_file.read_text()
    assert "\n" in content  # Formatted with newlines


def test_write_json_ensure_ascii(tmp_path):
    """Test write_json ensure_ascii parameter."""
    output_file = tmp_path / "output.json"
    data = {"text": "Hello 世界"}

    write_json(data, output_file, ensure_ascii=True)

    content = output_file.read_text()
    assert "\\u" in content  # Unicode escaped


def test_write_json_atomic_write(tmp_path):
    """Test write_json uses atomic write (temp file then replace)."""
    output_file = tmp_path / "output.json"
    data = {"test": "data"}

    write_json(data, output_file)

    # Temp file should not exist after successful write
    temp_file = output_file.with_suffix(output_file.suffix + ".tmp")
    assert not temp_file.exists()


def test_write_json_retry_on_io_error(tmp_path, cloud_sync_error, caplog):
    """Test write_json retries on I/O errors."""
    output_file = tmp_path / "output.json"
    data = {"test": "data"}

    # Track call count to control when error occurs
    call_count = [0]
    original_open = open

    def mock_open_with_retry(*args, **kwargs):
        call_count[0] += 1
        if call_count[0] == 1:
            # First call fails
            raise cloud_sync_error
        # Subsequent calls succeed with real open
        return original_open(*args, **kwargs)

    with patch("builtins.open", side_effect=mock_open_with_retry):
        # Should succeed on retry
        write_json(data, output_file, max_retries=2)

        # Should log warning on first failure
        assert "I/O error" in caplog.text

        # Verify file was written
        assert output_file.exists()
        loaded = json.loads(output_file.read_text())
        assert loaded == data


def test_write_json_fails_after_max_retries(tmp_path, cloud_sync_error):
    """Test write_json fails after exhausting retries."""
    output_file = tmp_path / "output.json"
    data = {"test": "data"}

    with patch("builtins.open", side_effect=cloud_sync_error), pytest.raises(OSError):
        write_json(data, output_file, max_retries=2)


# Test read_json


def test_read_json_basic(temp_json_file):
    """Test basic JSON reading."""
    result = read_json(temp_json_file)

    assert isinstance(result, dict)
    assert result["name"] == "test"
    assert result["version"] == "1.0"


def test_read_json_file_not_found():
    """Test read_json raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        read_json(Path("/nonexistent/file.json"))


def test_read_json_invalid_json(tmp_path):
    """Test read_json handles invalid JSON."""
    invalid_file = tmp_path / "invalid.json"
    invalid_file.write_text("{invalid json}")

    with pytest.raises(ValueError, match="Invalid JSON"):
        read_json(invalid_file)


def test_read_json_retry_on_io_error(temp_json_file, cloud_sync_error, caplog):
    """Test read_json retries on I/O errors."""
    original_data = json.loads(temp_json_file.read_text())

    with patch("builtins.open", side_effect=[cloud_sync_error, open(temp_json_file)]):
        result = read_json(temp_json_file, max_retries=2)

        assert result == original_data
        assert "I/O error" in caplog.text


# Test validate_path_exists


def test_validate_path_exists_valid_file(tmp_path):
    """Test validate_path_exists with valid file."""
    test_file = tmp_path / "test.txt"
    test_file.write_text("content")

    result = validate_path_exists(test_file, "test file")

    assert result == test_file


def test_validate_path_exists_valid_directory(tmp_path):
    """Test validate_path_exists with valid directory."""
    result = validate_path_exists(tmp_path, "test directory")

    assert result == tmp_path


def test_validate_path_exists_nonexistent():
    """Test validate_path_exists raises error for nonexistent path."""
    with pytest.raises(ValueError, match="does not exist"):
        validate_path_exists(Path("/nonexistent"), "test path")


# Test safe_read_text


def test_safe_read_text_basic(tmp_path):
    """Test safe_read_text reads file content."""
    test_file = tmp_path / "test.txt"
    content = "Hello, world!"
    test_file.write_text(content)

    result = safe_read_text(test_file)

    assert result == content


def test_safe_read_text_with_encoding(tmp_path):
    """Test safe_read_text respects encoding parameter."""
    test_file = tmp_path / "test.txt"
    content = "Hello 世界"
    test_file.write_text(content, encoding="utf-8")

    result = safe_read_text(test_file, encoding="utf-8")

    assert result == content


def test_safe_read_text_file_not_found():
    """Test safe_read_text raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        safe_read_text(Path("/nonexistent/file.txt"))


def test_safe_read_text_retry_on_io_error(tmp_path, cloud_sync_error, caplog):
    """Test safe_read_text retries on I/O errors."""
    test_file = tmp_path / "test.txt"
    test_file.write_text("content")

    with patch.object(Path, "read_text", side_effect=[cloud_sync_error, "content"]):
        result = safe_read_text(test_file, max_retries=2)

        assert result == "content"
        assert "I/O error" in caplog.text


# Test safe_write_text


def test_safe_write_text_basic(tmp_path):
    """Test safe_write_text writes content."""
    test_file = tmp_path / "test.txt"
    content = "Hello, world!"

    safe_write_text(content, test_file)

    assert test_file.read_text() == content


def test_safe_write_text_creates_parent_directory(tmp_path):
    """Test safe_write_text creates parent directories."""
    test_file = tmp_path / "nested" / "test.txt"

    safe_write_text("content", test_file)

    assert test_file.exists()
    assert test_file.parent.exists()


def test_safe_write_text_with_encoding(tmp_path):
    """Test safe_write_text respects encoding parameter."""
    test_file = tmp_path / "test.txt"
    content = "Hello 世界"

    safe_write_text(content, test_file, encoding="utf-8")

    assert test_file.read_text(encoding="utf-8") == content


def test_safe_write_text_retry_on_io_error(tmp_path, cloud_sync_error, caplog):
    """Test safe_write_text retries on I/O errors."""
    test_file = tmp_path / "test.txt"

    with patch.object(Path, "write_text", side_effect=[cloud_sync_error, None]):
        safe_write_text("content", test_file, max_retries=2)

        assert "I/O error" in caplog.text


# Test append_jsonl


def test_append_jsonl_basic(tmp_path):
    """Test append_jsonl appends JSON line."""
    jsonl_file = tmp_path / "output.jsonl"
    record = {"id": 1, "value": "test"}

    append_jsonl(record, jsonl_file)

    assert jsonl_file.exists()
    lines = jsonl_file.read_text().strip().split("\n")
    assert len(lines) == 1
    assert json.loads(lines[0]) == record


def test_append_jsonl_multiple_records(tmp_path):
    """Test append_jsonl appends multiple records."""
    jsonl_file = tmp_path / "output.jsonl"
    records = [{"id": 1, "value": "first"}, {"id": 2, "value": "second"}, {"id": 3, "value": "third"}]

    for record in records:
        append_jsonl(record, jsonl_file)

    lines = jsonl_file.read_text().strip().split("\n")
    assert len(lines) == 3
    assert all(json.loads(line) in records for line in lines)


def test_append_jsonl_creates_parent_directory(tmp_path):
    """Test append_jsonl creates parent directories."""
    jsonl_file = tmp_path / "nested" / "output.jsonl"
    record = {"test": "data"}

    append_jsonl(record, jsonl_file)

    assert jsonl_file.exists()
    assert jsonl_file.parent.exists()


def test_append_jsonl_retry_on_io_error(tmp_path, cloud_sync_error, caplog):
    """Test append_jsonl retries on I/O errors."""
    jsonl_file = tmp_path / "output.jsonl"
    record = {"test": "data"}

    with patch("builtins.open", side_effect=[cloud_sync_error, open(jsonl_file, "a")]):
        append_jsonl(record, jsonl_file, max_retries=2)

        assert "I/O error" in caplog.text


def test_write_json_non_serializable_data(tmp_path):
    """Test write_json handles non-serializable data."""
    output_file = tmp_path / "output.json"

    class NonSerializable:
        """Test class that cannot be JSON serialized."""

    data = {"obj": NonSerializable()}

    with pytest.raises(TypeError):
        write_json(data, output_file)
