"""Amplifier Collection Toolkit: Build Sophisticated AI Tools with Metacognitive Recipes.

This package provides structural utilities for building sophisticated CLI tools that use
multi-config metacognitive recipes - where code orchestrates multiple specialized AI sessions.

Key principle: Code for structure, AI for intelligence.

Modules:
- file_ops: File discovery, JSON I/O, path validation
- progress: Progress reporting
- validation: Input validation

Philosophy:
- Use AmplifierSession directly (don't wrap kernel mechanisms)
- Each tool owns its state (no state frameworks)
- Multi-config pattern for sophisticated tools
- Start simple, add complexity only when needed

See docs/TOOLKIT_GUIDE.md for complete guide.
Example: scenario-tools/tutorial-analyzer/ - Complete pedagogical exemplar.
"""

__version__ = "1.0.0"

# Export key utilities for easy access
from .file_ops import append_jsonl
from .file_ops import discover_files
from .file_ops import read_json
from .file_ops import safe_read_text
from .file_ops import safe_write_text
from .file_ops import validate_path_exists
from .file_ops import write_json
from .progress import ProgressReporter
from .validation import validate_input_path
from .validation import validate_minimum_files
from .validation import validate_output_path

# Alias for compatibility with templates/examples
require_minimum_files = validate_minimum_files

__all__ = [
    # File operations
    "discover_files",
    "read_json",
    "write_json",
    "validate_path_exists",
    "safe_read_text",
    "safe_write_text",
    "append_jsonl",
    # Progress reporting
    "ProgressReporter",
    # Validation
    "validate_input_path",
    "validate_output_path",
    "validate_minimum_files",
    "require_minimum_files",  # Alias for validate_minimum_files
]
