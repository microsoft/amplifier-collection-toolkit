# amplifier-collection-toolkit

**Build sophisticated CLI tools using metacognitive recipes with Amplifier**

This collection provides utilities, templates, examples, and guidance for building sophisticated CLI tools using the **metacognitive recipe pattern** - where code orchestrates multiple specialized AI configs to accomplish complex, multi-stage tasks.

---

## What This Collection Provides

### 1. Utilities Package (`amplifier_collection_toolkit`)

Structural helpers for building robust CLI tools:

- **File Operations**: Recursive discovery, JSON I/O, path validation
- **Progress Reporting**: User-friendly progress display
- **Input Validation**: Early validation with clear error messages

```python
from amplifier_collection_toolkit import (
    discover_files,
    ProgressReporter,
    validate_input_path
)
```

### 2. Scenario Tool: Tutorial Analyzer

A complete pedagogical exemplar demonstrating the metacognitive recipe pattern:

- 6 specialized AI configs (analyzer, simulator, diagnostician, improver, critic, synthesizer)
- Multi-stage pipeline with quality loops
- State checkpointing for resumability
- Human approval gates

Automatically installed as `tutorial-analyzer` CLI tool.

### 3. Templates

Starting point for building your own scenario tools:

- `standalone_tool.py` - Basic tool template
- Shows multi-config pattern structure
- Includes best practices

### 4. Comprehensive Documentation

- **TOOLKIT_GUIDE.md** - Complete reference
- **SCENARIO_TOOLS_GUIDE.md** - How to build scenario tools
- **PHILOSOPHY.md** - Design principles
- **BEST_PRACTICES.md** - Proven patterns
- **METACOGNITIVE_RECIPES.md** - Advanced patterns
- **HOW_TO_CREATE_YOUR_OWN.md** - Step-by-step guide
- **PACKAGING_GUIDE.md** - Distribution guide

### 5. Example Profile

**toolkit-dev**: Profile optimized for tool development workflow

- Extends the `foundation` profile and inherits whichever provider you have active (no Anthropic requirement)
- Auto-discovers agents shipped in this collection so `tool-builder` is available immediately

### 6. Example Agent

**tool-builder**: Agent that helps create new scenario tools

---

## Installation

```bash
# Install collection
amplifier collection add git+https://github.com/microsoft/amplifier-collection-toolkit@main

# Verify installation
amplifier collection list
amplifier collection show toolkit

# Tutorial analyzer automatically available
tutorial-analyzer --help

# Utilities importable
python -c "from amplifier_collection_toolkit import discover_files; print('OK')"
```

---

## Quick Start

### Using Utilities

```python
from amplifier_collection_toolkit import (
    discover_files,
    ProgressReporter,
    validate_input_path
)
from pathlib import Path

# Discover files recursively
input_dir = Path("./documents")
validate_input_path(input_dir, must_be_dir=True)

files = discover_files(input_dir, "**/*.md")
print(f"Found {len(files)} markdown files")

# Process with progress
progress = ProgressReporter(len(files), "Processing")
for file in files:
    # Your processing logic
    progress.update()
progress.finish()
```

### Using Tutorial Analyzer

```bash
# Analyze a tutorial
tutorial-analyzer path/to/tutorial.md

# Resume from checkpoint
tutorial-analyzer path/to/tutorial.md --resume
```

### Creating Your Own Tool

```bash
# Copy template
cp templates/standalone_tool.py my_tool.py

# Follow guides in docs/
# - HOW_TO_CREATE_YOUR_OWN.md for step-by-step
# - METACOGNITIVE_RECIPES.md for patterns
# - BEST_PRACTICES.md for quality
```

---

## What are Metacognitive Recipes?

**Metacognitive recipes** are thinking processes encoded as code that orchestrate multiple specialized AI sessions:

```
Analyze (precise) → Simulate (empathetic) → Diagnose (critical) →
→ Plan (strategic) [HUMAN APPROVAL] → Implement (creative) →
→ Evaluate (judgmental) → LOOP or FINISH
```

Each arrow represents a specialized AI config optimized for its cognitive role. Code decides which config to use when, manages state across stages, and determines flow based on results.

**Key Principle**: Code for structure, AI for intelligence.

**Why?** A single AI session can't optimize for different cognitive tasks:
- **Analysis** needs precision (temp=0.3)
- **Creativity** needs exploration (temp=0.7)
- **Evaluation** needs judgment (temp=0.2)

Multi-config patterns allow each stage to use the optimal configuration.

---

## Philosophy

Core principles:

- **Multi-config patterns**: Specialized configs for different cognitive tasks (not one compromise config)
- **Structural utilities only**: File operations, progress, validation (NOT AmplifierSession wrappers)
- **Tool-owned state**: Each tool manages its own checkpointing (no state frameworks)
- **Ruthless simplicity**: Start minimal, YAGNI, code for structure/AI for intelligence

See [docs/PHILOSOPHY.md](docs/PHILOSOPHY.md) for complete philosophical rationale.

---

## Collection Capabilities

Declared in `pyproject.toml`:

- `scenario-tool-development` - Build sophisticated CLI tools
- `multi-config-patterns` - Metacognitive recipe examples
- `utilities` - File ops, progress, validation helpers
- `metacognitive-recipes` - Pattern library

---

## Documentation

Complete guides in `docs/`:

- **[TOOLKIT_GUIDE.md](docs/TOOLKIT_GUIDE.md)** - Comprehensive reference
- **[SCENARIO_TOOLS_GUIDE.md](docs/SCENARIO_TOOLS_GUIDE.md)** - Build scenario tools
- **[PHILOSOPHY.md](docs/PHILOSOPHY.md)** - Design principles
- **[BEST_PRACTICES.md](docs/BEST_PRACTICES.md)** - Proven patterns
- **[METACOGNITIVE_RECIPES.md](docs/METACOGNITIVE_RECIPES.md)** - Advanced patterns
- **[HOW_TO_CREATE_YOUR_OWN.md](docs/HOW_TO_CREATE_YOUR_OWN.md)** - Step-by-step guide
- **[PACKAGING_GUIDE.md](docs/PACKAGING_GUIDE.md)** - Distribution

---

## Examples

### Tutorial Analyzer

Located in `scenario-tools/tutorial-analyzer/`:

- Complete multi-stage tool with 6 specialized configs
- Demonstrates quality loops, checkpointing, human gates
- Fully documented (README + HOW_TO_BUILD)
- Installable as standalone CLI tool

Study this as the pedagogical exemplar for building your own tools.

---

## Requirements

- Python >=3.11
- Amplifier core system
- click (for CLI utilities)

---

## Contributing

This project welcomes contributions and suggestions. Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

---

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft
trademarks or logos is subject to and must follow
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.

---

**Collection Version**: 1.0.0
**Last Updated**: 2025-10-31
