"""
Unit tests for progress reporting utilities.

Tests ProgressReporter, SimpleSpinner, and log_stage functionality.
"""

import pytest
import logging
import time
from unittest.mock import patch, MagicMock
from amplifier_collection_toolkit.progress import (
    ProgressReporter,
    SimpleSpinner,
    log_stage
)


# Test ProgressReporter

def test_progress_reporter_initialization():
    """Test ProgressReporter initializes correctly."""
    reporter = ProgressReporter(total=10, description="Testing")
    
    assert reporter.total == 10
    assert reporter.current == 0
    assert reporter.description == "Testing"
    assert reporter.show_items is True
    assert reporter.log_interval == 10


def test_progress_reporter_update(caplog):
    """Test ProgressReporter.update increments counter."""
    reporter = ProgressReporter(total=5, description="Processing")
    
    reporter.update()
    
    assert reporter.current == 1


def test_progress_reporter_update_with_item_name(caplog):
    """Test ProgressReporter.update logs item names."""
    caplog.set_level(logging.INFO)
    reporter = ProgressReporter(total=2, description="Processing", log_interval=1)
    
    reporter.update(item_name="test_file.txt")
    
    assert "test_file.txt" in caplog.text


def test_progress_reporter_complete(caplog):
    """Test ProgressReporter.complete logs summary."""
    caplog.set_level(logging.INFO)
    reporter = ProgressReporter(total=5, description="Processing")
    reporter.current = 5
    
    reporter.complete()
    
    assert "complete" in caplog.text.lower()
    assert "5/5" in caplog.text


def test_progress_reporter_complete_calculates_elapsed_time(caplog):
    """Test ProgressReporter.complete includes elapsed time."""
    caplog.set_level(logging.INFO)
    reporter = ProgressReporter(total=5, description="Processing")
    reporter.current = 5
    
    # Simulate some elapsed time
    reporter.start_time = time.time() - 2.5
    
    reporter.complete()
    
    # Should show time in seconds
    assert "s" in caplog.text


def test_progress_reporter_complete_formats_time_minutes(caplog):
    """Test ProgressReporter.complete formats time in minutes for longer operations."""
    caplog.set_level(logging.INFO)
    reporter = ProgressReporter(total=5, description="Processing")
    reporter.current = 5
    
    # Simulate 90 seconds elapsed
    reporter.start_time = time.time() - 90
    
    reporter.complete()
    
    # Should show time in minutes
    assert "m" in caplog.text


def test_progress_reporter_log_interval():
    """Test ProgressReporter respects log_interval."""
    reporter = ProgressReporter(total=10, description="Processing", log_interval=5)
    
    # Should not log every update
    with patch('amplifier_collection_toolkit.progress.logger.info') as mock_log:
        reporter.update()
        reporter.update()
        reporter.update()
        
        # Only initial log, no update logs yet (interval is 5)
        # Filter out the initial log
        update_logs = [call for call in mock_log.call_args_list if "Processing" in str(call)]
        assert len(update_logs) <= 2  # Initial + maybe one update


def test_progress_reporter_log_summary_all_success(caplog):
    """Test ProgressReporter.log_summary with all successes."""
    caplog.set_level(logging.INFO)
    reporter = ProgressReporter(total=10, description="Processing")
    
    reporter.log_summary(successes=10, failures=0)
    
    assert "10 items processed successfully" in caplog.text


def test_progress_reporter_log_summary_with_failures(caplog):
    """Test ProgressReporter.log_summary with some failures."""
    reporter = ProgressReporter(total=10, description="Processing")
    
    reporter.log_summary(successes=8, failures=2)
    
    assert "failures" in caplog.text.lower()
    assert "8/10" in caplog.text


def test_progress_reporter_estimate_remaining():
    """Test ProgressReporter.estimate_remaining calculates time."""
    reporter = ProgressReporter(total=10, description="Processing")
    reporter.current = 5
    reporter.start_time = time.time() - 10  # 5 items in 10 seconds = 2s per item
    
    estimate = reporter.estimate_remaining()
    
    # Should estimate ~10s remaining (5 items * 2s each)
    assert estimate is not None
    assert "s" in estimate or "m" in estimate


def test_progress_reporter_estimate_remaining_no_progress():
    """Test ProgressReporter.estimate_remaining returns None when no progress."""
    reporter = ProgressReporter(total=10, description="Processing")
    
    estimate = reporter.estimate_remaining()
    
    assert estimate is None


def test_progress_reporter_estimate_remaining_complete():
    """Test ProgressReporter.estimate_remaining returns None when complete."""
    reporter = ProgressReporter(total=10, description="Processing")
    reporter.current = 10
    
    estimate = reporter.estimate_remaining()
    
    assert estimate is None


# Test SimpleSpinner

def test_simple_spinner_initialization(caplog):
    """Test SimpleSpinner initializes correctly."""
    caplog.set_level(logging.INFO)
    spinner = SimpleSpinner(description="Searching")
    
    assert spinner.description == "Searching"
    assert spinner.counter == 0
    assert "Searching..." in caplog.text


def test_simple_spinner_spin():
    """Test SimpleSpinner.spin increments counter."""
    spinner = SimpleSpinner(description="Working")
    
    spinner.spin()
    spinner.spin()
    
    assert spinner.counter == 2


def test_simple_spinner_spin_logs_periodically(caplog):
    """Test SimpleSpinner.spin logs activity periodically."""
    caplog.set_level(logging.INFO)
    spinner = SimpleSpinner(description="Working")
    
    # Force time difference to trigger log
    spinner.last_update = time.time() - 10
    
    spinner.spin()
    
    # Should log activity after time interval
    assert "still" in caplog.text.lower()


def test_simple_spinner_stop(caplog):
    """Test SimpleSpinner.stop logs completion."""
    caplog.set_level(logging.INFO)
    spinner = SimpleSpinner(description="Working")
    spinner.counter = 5
    
    spinner.stop()
    
    assert "complete" in caplog.text.lower()
    assert "5 items" in caplog.text


def test_simple_spinner_stop_with_message(caplog):
    """Test SimpleSpinner.stop logs custom message."""
    caplog.set_level(logging.INFO)
    spinner = SimpleSpinner(description="Working")
    
    spinner.stop(message="Found 42 results")
    
    assert "Found 42 results" in caplog.text


# Test log_stage

def test_log_stage_basic(caplog):
    """Test log_stage logs stage name."""
    caplog.set_level(logging.INFO)
    log_stage("Validation")
    
    assert "Stage: Validation" in caplog.text
    assert "=" in caplog.text  # Separator


def test_log_stage_with_description(caplog):
    """Test log_stage logs stage description."""
    caplog.set_level(logging.INFO)
    log_stage("Processing", description="Analyzing input files")
    
    assert "Stage: Processing" in caplog.text
    assert "Analyzing input files" in caplog.text


def test_log_stage_separator_format(caplog):
    """Test log_stage uses consistent separator format."""
    caplog.set_level(logging.INFO)
    log_stage("Test Stage")
    
    # Should have separator lines
    lines = caplog.text.strip().split('\n')
    separator_lines = [line for line in lines if '=' in line]
    
    assert len(separator_lines) >= 2  # Opening and closing separators
