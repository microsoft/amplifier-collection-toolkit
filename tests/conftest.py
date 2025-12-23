"""
Pytest fixtures for toolkit collection tests.

Provides common fixtures for testing utilities, mocking external dependencies,
and creating test data structures.
"""

import pytest
import json
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock


@pytest.fixture
def mock_amplifier_session():
    """Mock AmplifierSession for testing without actual LLM calls."""
    session = AsyncMock()
    session.execute = AsyncMock(return_value="Mock response")
    session.initialize = AsyncMock()
    session.coordinator = MagicMock()
    session.coordinator.mount = AsyncMock()
    return session


@pytest.fixture
def mock_resolver():
    """Mock StandardModuleSourceResolver for testing."""
    resolver = MagicMock()
    resolver.resolve = AsyncMock(return_value="/mock/module/path")
    return resolver


@pytest.fixture
def temp_json_file(tmp_path):
    """Create a temporary JSON file with sample data."""
    json_file = tmp_path / "test_data.json"
    data = {
        "name": "test",
        "version": "1.0",
        "items": [1, 2, 3]
    }
    json_file.write_text(json.dumps(data, indent=2))
    return json_file


@pytest.fixture
def sample_config():
    """Sample AmplifierSession configuration."""
    return {
        "session": {
            "orchestrator": {
                "module": "loop-basic",
                "source": "git+https://github.com/microsoft/amplifier-module-loop-basic@main"
            },
            "context": {
                "module": "context-simple",
                "source": "git+https://github.com/microsoft/amplifier-module-context-simple@main"
            },
        },
        "providers": [{
            "module": "provider-anthropic",
            "source": "git+https://github.com/microsoft/amplifier-module-provider-anthropic@main",
            "config": {
                "model": "claude-sonnet-4-5",
                "temperature": 0.3
            }
        }]
    }


@pytest.fixture
def cloud_sync_error():
    """OSError simulating cloud-synced file I/O error."""
    error = OSError("I/O error")
    error.errno = 5  # I/O error errno
    return error


@pytest.fixture
def sample_markdown_files(tmp_path):
    """Create sample markdown files for testing file discovery."""
    # Create directory structure
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    
    nested_dir = docs_dir / "nested"
    nested_dir.mkdir()
    
    # Create markdown files
    (docs_dir / "file1.md").write_text("# File 1\nContent")
    (docs_dir / "file2.md").write_text("# File 2\nContent")
    (nested_dir / "file3.md").write_text("# File 3\nContent")
    
    # Create non-markdown file
    (docs_dir / "readme.txt").write_text("Text file")
    
    return docs_dir


@pytest.fixture
def sample_agent_yaml():
    """Sample agent YAML content for testing."""
    return """---
meta:
  name: test-agent
  description: "Test agent"

tools:
  - module: tool-filesystem

providers:
  - module: provider-anthropic
    config:
      model: claude-sonnet-4-5
      temperature: 0.3
---

# Test Agent Content
"""


@pytest.fixture
def empty_directory(tmp_path):
    """Create an empty directory for testing."""
    empty_dir = tmp_path / "empty"
    empty_dir.mkdir()
    return empty_dir


@pytest.fixture
def mock_progress_reporter():
    """Mock ProgressReporter for testing."""
    from unittest.mock import MagicMock
    reporter = MagicMock()
    reporter.update = MagicMock()
    reporter.complete = MagicMock()
    reporter.log_summary = MagicMock()
    reporter.estimate_remaining = MagicMock(return_value="5m 30s")
    return reporter
