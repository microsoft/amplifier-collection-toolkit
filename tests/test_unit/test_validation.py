"""
Unit tests for validation utilities.

Tests input validation, output validation, and data structure validation.
"""

from pathlib import Path

import pytest
from amplifier_collection_toolkit.validation import validate_file_extension
from amplifier_collection_toolkit.validation import validate_input_path
from amplifier_collection_toolkit.validation import validate_json_structure
from amplifier_collection_toolkit.validation import validate_minimum_files
from amplifier_collection_toolkit.validation import validate_not_empty
from amplifier_collection_toolkit.validation import validate_output_path
from amplifier_collection_toolkit.validation import validate_pattern
from amplifier_collection_toolkit.validation import validate_range

# Test validate_input_path


def test_validate_input_path_existing_file(tmp_path):
    """Test validate_input_path with existing file."""
    test_file = tmp_path / "test.txt"
    test_file.write_text("content")

    result = validate_input_path(test_file)

    assert result is True


def test_validate_input_path_existing_directory(tmp_path):
    """Test validate_input_path with existing directory."""
    result = validate_input_path(tmp_path, must_be_dir=True)

    assert result is True


def test_validate_input_path_nonexistent():
    """Test validate_input_path raises error for nonexistent path."""
    with pytest.raises(ValueError, match="does not exist"):
        validate_input_path(Path("/nonexistent"), must_exist=True)


def test_validate_input_path_must_be_dir_but_is_file(tmp_path):
    """Test validate_input_path raises error when directory expected but file found."""
    test_file = tmp_path / "test.txt"
    test_file.write_text("content")

    with pytest.raises(ValueError, match="must be a directory"):
        validate_input_path(test_file, must_be_dir=True)


def test_validate_input_path_empty_directory_warning(tmp_path, caplog):
    """Test validate_input_path warns about empty directory."""
    empty_dir = tmp_path / "empty"
    empty_dir.mkdir()

    validate_input_path(empty_dir)

    assert "empty" in caplog.text.lower()


def test_validate_input_path_nonexistent_allowed(tmp_path):
    """Test validate_input_path allows nonexistent path when must_exist=False."""
    nonexistent = tmp_path / "nonexistent"

    result = validate_input_path(nonexistent, must_exist=False)

    assert result is True


# Test validate_output_path


def test_validate_output_path_new_file(tmp_path):
    """Test validate_output_path with new file in existing directory."""
    output_file = tmp_path / "output.json"

    result = validate_output_path(output_file)

    assert result is True


def test_validate_output_path_existing_file_with_overwrite(tmp_path, caplog):
    """Test validate_output_path allows overwriting existing file."""
    output_file = tmp_path / "output.json"
    output_file.write_text("existing")

    result = validate_output_path(output_file, allow_overwrite=True)

    assert result is True
    assert "overwritten" in caplog.text.lower()


def test_validate_output_path_existing_file_no_overwrite(tmp_path):
    """Test validate_output_path raises error when overwrite not allowed."""
    output_file = tmp_path / "output.json"
    output_file.write_text("existing")

    with pytest.raises(ValueError, match="already exists"):
        validate_output_path(output_file, allow_overwrite=False)


def test_validate_output_path_is_directory(tmp_path):
    """Test validate_output_path raises error when path is directory."""
    with pytest.raises(ValueError, match="is a directory"):
        validate_output_path(tmp_path)


def test_validate_output_path_parent_not_exists(tmp_path):
    """Test validate_output_path raises error when parent directory doesn't exist."""
    output_file = tmp_path / "nonexistent" / "output.json"

    with pytest.raises(ValueError, match="directory does not exist"):
        validate_output_path(output_file)


# Test validate_minimum_files


def test_validate_minimum_files_sufficient():
    """Test validate_minimum_files with sufficient files."""
    files = ["file1.txt", "file2.txt", "file3.txt"]

    result = validate_minimum_files(files, minimum=2)

    assert result is True


def test_validate_minimum_files_exact():
    """Test validate_minimum_files with exact minimum."""
    files = ["file1.txt", "file2.txt"]

    result = validate_minimum_files(files, minimum=2)

    assert result is True


def test_validate_minimum_files_insufficient():
    """Test validate_minimum_files raises error when too few files."""
    files = ["file1.txt"]

    with pytest.raises(ValueError, match="Need at least 2"):
        validate_minimum_files(files, minimum=2)


def test_validate_minimum_files_custom_file_type():
    """Test validate_minimum_files uses custom file_type in error message."""
    files = []

    with pytest.raises(ValueError, match="markdown files"):
        validate_minimum_files(files, minimum=1, file_type="markdown files")


# Test validate_pattern


def test_validate_pattern_valid_recursive():
    """Test validate_pattern with valid recursive pattern."""
    result = validate_pattern("**/*.md")

    assert result is True


def test_validate_pattern_non_recursive_warning(caplog):
    """Test validate_pattern warns about non-recursive pattern."""
    validate_pattern("*.md")

    assert "not recursive" in caplog.text.lower()


def test_validate_pattern_empty():
    """Test validate_pattern raises error for empty pattern."""
    with pytest.raises(ValueError, match="cannot be empty"):
        validate_pattern("")


def test_validate_pattern_complex_warning(caplog):
    """Test validate_pattern warns about overly complex patterns."""
    validate_pattern("*****/*.md")

    assert "complex" in caplog.text.lower()


def test_validate_pattern_path_without_recursive_warning(caplog):
    """Test validate_pattern warns about paths without recursive marker."""
    validate_pattern("subdir/*.md")

    assert "includes path" in caplog.text.lower()


# Test validate_file_extension


def test_validate_file_extension_valid():
    """Test validate_file_extension with valid extension."""
    result = validate_file_extension(Path("test.json"), [".json", ".jsonl"])

    assert result is True


def test_validate_file_extension_invalid():
    """Test validate_file_extension raises error for invalid extension."""
    with pytest.raises(ValueError, match="not allowed"):
        validate_file_extension(Path("test.txt"), [".json", ".yaml"])


def test_validate_file_extension_case_insensitive():
    """Test validate_file_extension is case insensitive."""
    result = validate_file_extension(Path("TEST.JSON"), [".json"])

    assert result is True


def test_validate_file_extension_no_restriction():
    """Test validate_file_extension with empty allowed list."""
    result = validate_file_extension(Path("test.xyz"), [])

    assert result is True


# Test validate_json_structure


def test_validate_json_structure_valid():
    """Test validate_json_structure with all required fields."""
    data = {"name": "test", "version": "1.0", "author": "someone"}

    result = validate_json_structure(data, ["name", "version"])

    assert result is True


def test_validate_json_structure_missing_field():
    """Test validate_json_structure raises error for missing field."""
    data = {"name": "test"}

    with pytest.raises(ValueError, match="Missing required fields"):
        validate_json_structure(data, ["name", "version"])


def test_validate_json_structure_multiple_missing():
    """Test validate_json_structure reports all missing fields."""
    data = {"name": "test"}

    with pytest.raises(ValueError, match="version.*author"):
        validate_json_structure(data, ["name", "version", "author"])


def test_validate_json_structure_no_required_fields():
    """Test validate_json_structure with empty required fields list."""
    data = {"anything": "goes"}

    result = validate_json_structure(data, [])

    assert result is True


# Test validate_range


def test_validate_range_within_bounds():
    """Test validate_range with value within bounds."""
    result = validate_range(5, min_value=1, max_value=10)

    assert result is True


def test_validate_range_at_minimum():
    """Test validate_range with value at minimum."""
    result = validate_range(1, min_value=1, max_value=10)

    assert result is True


def test_validate_range_at_maximum():
    """Test validate_range with value at maximum."""
    result = validate_range(10, min_value=1, max_value=10)

    assert result is True


def test_validate_range_below_minimum():
    """Test validate_range raises error when below minimum."""
    with pytest.raises(ValueError, match="must be at least 1"):
        validate_range(0, min_value=1, max_value=10)


def test_validate_range_above_maximum():
    """Test validate_range raises error when above maximum."""
    with pytest.raises(ValueError, match="must be at most 10"):
        validate_range(11, min_value=1, max_value=10)


def test_validate_range_only_minimum():
    """Test validate_range with only minimum constraint."""
    result = validate_range(100, min_value=1)

    assert result is True


def test_validate_range_only_maximum():
    """Test validate_range with only maximum constraint."""
    result = validate_range(5, max_value=10)

    assert result is True


def test_validate_range_custom_name():
    """Test validate_range uses custom name in error message."""
    with pytest.raises(ValueError, match="batch_size"):
        validate_range(0, min_value=1, name="batch_size")


def test_validate_range_float_value():
    """Test validate_range works with float values."""
    result = validate_range(5.5, min_value=1.0, max_value=10.0)

    assert result is True


# Test validate_not_empty


def test_validate_not_empty_non_empty_string():
    """Test validate_not_empty with non-empty string."""
    result = validate_not_empty("hello", "input_text")

    assert result is True


def test_validate_not_empty_non_empty_list():
    """Test validate_not_empty with non-empty list."""
    result = validate_not_empty([1, 2, 3], "results")

    assert result is True


def test_validate_not_empty_non_empty_dict():
    """Test validate_not_empty with non-empty dict."""
    result = validate_not_empty({"key": "value"}, "config")

    assert result is True


def test_validate_not_empty_empty_string():
    """Test validate_not_empty raises error for empty string."""
    with pytest.raises(ValueError, match="cannot be empty"):
        validate_not_empty("", "input_text")


def test_validate_not_empty_empty_list():
    """Test validate_not_empty raises error for empty list."""
    with pytest.raises(ValueError, match="results"):
        validate_not_empty([], "results")


def test_validate_not_empty_empty_dict():
    """Test validate_not_empty raises error for empty dict."""
    with pytest.raises(ValueError, match="config"):
        validate_not_empty({}, "config")
