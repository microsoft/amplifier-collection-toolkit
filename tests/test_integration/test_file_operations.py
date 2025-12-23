"""
Integration tests for file operations.

Tests file operations working together in realistic scenarios.
"""

import json

from amplifier_collection_toolkit.file_ops import append_jsonl
from amplifier_collection_toolkit.file_ops import discover_files
from amplifier_collection_toolkit.file_ops import read_json
from amplifier_collection_toolkit.file_ops import safe_read_text
from amplifier_collection_toolkit.file_ops import safe_write_text
from amplifier_collection_toolkit.file_ops import write_json


def test_discover_and_process_files(sample_markdown_files):
    """Integration test: Discover files and process them."""
    # Discover markdown files
    files = discover_files(sample_markdown_files, "**/*.md")

    assert len(files) == 3

    # Read and process each file
    for file_path in files:
        content = safe_read_text(file_path)
        assert len(content) > 0
        assert "File" in content


def test_write_read_json_roundtrip(tmp_path):
    """Integration test: Write and read JSON maintains data integrity."""
    output_file = tmp_path / "data.json"

    # Write complex data structure
    original_data = {
        "string": "test",
        "number": 42,
        "float": 3.14,
        "boolean": True,
        "null": None,
        "array": [1, 2, 3],
        "nested": {"key": "value", "list": ["a", "b", "c"]},
    }

    write_json(original_data, output_file)

    # Read it back
    loaded_data = read_json(output_file)

    # Verify data integrity
    assert loaded_data == original_data


def test_jsonl_append_and_read_workflow(tmp_path):
    """Integration test: Append multiple JSONL records and read them back."""
    jsonl_file = tmp_path / "output.jsonl"

    # Append multiple records
    records = [
        {"id": 1, "type": "event", "value": "start"},
        {"id": 2, "type": "event", "value": "process"},
        {"id": 3, "type": "event", "value": "end"},
    ]

    for record in records:
        append_jsonl(record, jsonl_file)

    # Read all records back
    loaded_records = []
    with open(jsonl_file) as f:
        for line in f:
            loaded_records.append(json.loads(line.strip()))

    assert len(loaded_records) == 3
    assert loaded_records == records


def test_file_discovery_with_validation(tmp_path):
    """Integration test: Discover files and validate them."""
    from amplifier_collection_toolkit.validation import validate_input_path
    from amplifier_collection_toolkit.validation import validate_minimum_files

    # Create test files
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()

    for i in range(5):
        (docs_dir / f"file{i}.md").write_text(f"# File {i}")

    # Validate input path
    validate_input_path(docs_dir, must_be_dir=True)

    # Discover files
    files = discover_files(docs_dir, "**/*.md")

    # Validate minimum files
    validate_minimum_files(files, minimum=3, file_type="markdown files")

    assert len(files) == 5


def test_nested_directory_file_operations(tmp_path):
    """Integration test: File operations in nested directory structure."""
    # Create nested structure
    nested_path = tmp_path / "level1" / "level2" / "level3"

    # Write file (should create all parent directories)
    output_file = nested_path / "data.json"
    data = {"nested": "data"}

    write_json(data, output_file)

    # Verify file exists
    assert output_file.exists()
    assert nested_path.exists()

    # Read it back
    loaded_data = read_json(output_file)
    assert loaded_data == data

    # Write text file in same structure
    text_file = nested_path / "notes.txt"
    safe_write_text("Some notes", text_file)

    # Read text back
    text_content = safe_read_text(text_file)
    assert text_content == "Some notes"
