"""
End-to-end tests for complete workflows.

Tests complete scenarios from discovery to processing to output.
"""

import json

import pytest
from amplifier_collection_toolkit.file_ops import discover_files
from amplifier_collection_toolkit.file_ops import read_json
from amplifier_collection_toolkit.file_ops import write_json
from amplifier_collection_toolkit.progress import ProgressReporter
from amplifier_collection_toolkit.validation import validate_input_path
from amplifier_collection_toolkit.validation import validate_minimum_files
from amplifier_collection_toolkit.validation import validate_output_path


def test_complete_file_processing_workflow(tmp_path):
    """E2E test: Complete file discovery, validation, and output workflow."""
    # Setup: Create input files
    input_dir = tmp_path / "input"
    input_dir.mkdir()

    for i in range(5):
        (input_dir / f"doc{i}.md").write_text(f"# Document {i}\n\nContent for document {i}")

    output_dir = tmp_path / "output"
    output_dir.mkdir()

    # Step 1: Validate input
    validate_input_path(input_dir, must_be_dir=True)

    # Step 2: Discover files
    files = discover_files(input_dir, "**/*.md")

    # Step 3: Validate minimum files
    validate_minimum_files(files, minimum=3, file_type="markdown files")

    # Step 4: Process files with progress tracking
    results = []
    reporter = ProgressReporter(total=len(files), description="Processing")

    for file_path in files:
        # Simulate processing
        content = file_path.read_text()
        result = {"file": file_path.name, "length": len(content), "lines": len(content.split("\n"))}
        results.append(result)
        reporter.update(item_name=file_path.name)

    reporter.complete()

    # Step 5: Validate and write output
    output_file = output_dir / "results.json"
    validate_output_path(output_file)
    write_json(results, output_file)

    # Step 6: Verify output
    assert output_file.exists()
    loaded_results = read_json(output_file)
    assert len(loaded_results) == 5
    assert all("file" in r and "length" in r for r in loaded_results)


def test_incremental_processing_with_jsonl(tmp_path):
    """E2E test: Incremental processing with JSONL checkpointing."""
    from amplifier_collection_toolkit.file_ops import append_jsonl
    from amplifier_collection_toolkit.file_ops import discover_files

    # Setup: Create input files
    input_dir = tmp_path / "input"
    input_dir.mkdir()

    for i in range(10):
        (input_dir / f"item{i}.txt").write_text(f"Item {i}")

    checkpoint_file = tmp_path / "progress.jsonl"

    # Discover files
    files = discover_files(input_dir, "**/*.txt")

    # Process with checkpointing
    for file_path in files:
        # Simulate processing
        result = {"file": file_path.name, "status": "processed", "timestamp": "2024-01-01T00:00:00"}

        # Checkpoint after each file
        append_jsonl(result, checkpoint_file)

    # Verify checkpoints
    assert checkpoint_file.exists()

    # Read all checkpoints
    checkpoints = []
    with open(checkpoint_file) as f:
        for line in f:
            checkpoints.append(json.loads(line.strip()))

    assert len(checkpoints) == 10
    assert all(c["status"] == "processed" for c in checkpoints)


def test_validation_prevents_invalid_workflow(tmp_path):
    """E2E test: Validation catches errors before expensive processing."""
    from amplifier_collection_toolkit.file_ops import discover_files
    from amplifier_collection_toolkit.validation import validate_input_path
    from amplifier_collection_toolkit.validation import validate_minimum_files
    from amplifier_collection_toolkit.validation import validate_output_path

    # Setup: Empty input directory
    input_dir = tmp_path / "empty_input"
    input_dir.mkdir()

    output_dir = tmp_path / "nonexistent"  # Doesn't exist

    # Step 1: Input validation should warn about empty directory
    validate_input_path(input_dir, must_be_dir=True)

    # Step 2: File discovery returns empty list
    files = discover_files(input_dir, "**/*.md")

    # Step 3: Validation catches insufficient files BEFORE processing
    with pytest.raises(ValueError, match="Need at least"):
        validate_minimum_files(files, minimum=1, file_type="markdown files")

    # Step 4: Output validation catches missing parent directory
    output_file = output_dir / "results.json"
    with pytest.raises(ValueError, match="directory does not exist"):
        validate_output_path(output_file)

    # Workflow stopped early, preventing expensive processing of invalid inputs
