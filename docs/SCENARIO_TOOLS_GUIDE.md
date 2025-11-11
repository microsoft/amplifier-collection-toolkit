---
last_updated: 2025-10-26
status: stable
audience: users, tool-developers
---

# Scenario Tools Guide

## What Are Scenario Tools?

**Scenario tools** are sophisticated CLI applications that orchestrate multiple AI sessions for complex, multi-stage tasks. They differ fundamentally from simple LLM tools (function calling):

| Aspect                | LLM Tools            | Scenario Tools                    |
| --------------------- | -------------------- | --------------------------------- |
| **Invoked by**        | LLM during chat      | Human directly (CLI)              |
| **Complexity**        | Single function call | Multi-stage orchestrated workflow |
| **AI configs**        | Uses current session | Multiple specialized configs      |
| **State**             | Stateless            | Can maintain state across stages  |
| **Human interaction** | Via LLM              | Direct (approval gates, feedback) |
| **Resumability**      | No                   | Yes (checkpoints)                 |

**Example**: Tutorial analyzer is a scenario tool. It orchestrates 6 specialized AI configs through a multi-stage pipeline with human approval gates.

---

## Why Scenario Tools?

### Problem: Single-Config Limitations

A single AI session (one config) can't optimize for different cognitive tasks:

- **Analysis** needs precision (temp=0.3)
- **Creativity** needs exploration (temp=0.7)
- **Evaluation** needs judgment (temp=0.2)

One config compromises all tasks.

### Solution: Metacognitive Recipes

**Metacognitive recipes** are thinking processes encoded as code that orchestrate multiple specialized AI sessions:

```
Analyze (precise) → Simulate (empathetic) → Diagnose (critical) →
→ Plan (strategic) [HUMAN APPROVAL] → Implement (creative) →
→ Evaluate (judgmental) → LOOP or FINISH
```

Each arrow is a specialized AI config optimized for its cognitive role. Code decides which config to use when, manages state across stages, and determines flow based on results.

---

## Scenario Tools in Collections

Collections can package scenario tools in the `scenario-tools/` directory:

```
my-collection/
  scenario-tools/
    my_analyzer/
      main.py                 # CLI entry point
      pyproject.toml          # Package metadata

      analyzer/core.py        # Stage 1: ANALYZER_CONFIG
      synthesizer/core.py     # Stage 2: SYNTHESIZER_CONFIG

      README.md               # User guide
      HOW_TO_BUILD.md         # Builder guide
```

**Installation**: When you install a collection, scenario tools are automatically installed via `uv tool install`:

```bash
# Install collection
amplifier collection add git+https://github.com/user/my-collection

# Tools available immediately
my-analyzer --help

# Or use via uvx
uvx --from my-collection my-analyzer [args]
```

---

## Anatomy of a Scenario Tool

### Directory Structure

```
scenario-tools/tutorial-analyzer/
  # Entry point
  main.py                     # CLI interface, orchestration logic

  # Specialized cognitive modules
  analyzer/core.py            # ANALYZER_CONFIG (analytical, temp=0.3)
  learner_simulator/core.py   # LEARNER_SIMULATOR_CONFIG (empathetic, temp=0.5)
  diagnostician/core.py       # DIAGNOSTICIAN_CONFIG (precise, temp=0.1)
  improver/core.py            # IMPROVER_CONFIG (creative, temp=0.7)
  critic/core.py              # CRITIC_CONFIG (evaluative, temp=0.2)
  synthesizer/core.py         # SYNTHESIZER_CONFIG (analytical, temp=0.3)

  # State management
  state.py                    # Checkpoint/resume logic

  # Packaging
  pyproject.toml              # Package metadata for uv
  README.md                   # User documentation
  HOW_TO_BUILD.md             # Builder documentation
```

### Key Components

**1. Multiple Specialized Configs**

Each cognitive stage has its own config:

```python
# analyzer/core.py
ANALYZER_CONFIG = {
    "session": {"orchestrator": "loop-basic", "context": "context-simple"},
    "providers": [{
        "module": "provider-anthropic",
        "source": "git+https://github.com/microsoft/amplifier-module-provider-anthropic@main",
        "config": {
            "model": "claude-sonnet-4-5",
            "temperature": 0.3,  # Precise analysis
            "system_prompt": "You are an expert content analyzer..."
        }
    }],
}

# improver/core.py
IMPROVER_CONFIG = {
    "session": {"orchestrator": "loop-streaming", "context": "context-simple"},
    "providers": [{
        "module": "provider-anthropic",
        "source": "git+https://github.com/microsoft/amplifier-module-provider-anthropic@main",
        "config": {
            "model": "claude-opus-4-1",
            "temperature": 0.7,  # Creative generation
            "system_prompt": "You are a creative improvement generator..."
        }
    }],
}
```

**2. Code Orchestration**

Main logic orchestrates which config to use when:

```python
# main.py
async def evolve_tutorial(tutorial_path: Path) -> dict:
    """Multi-stage metacognitive recipe."""

    content = tutorial_path.read_text()

    # Stage 1: Analytical subtask
    async with AmplifierSession(config=ANALYZER_CONFIG) as session:
        analysis = await session.execute(f"Analyze: {content}")

    # Stage 2: Empathetic subtask
    async with AmplifierSession(config=LEARNER_SIMULATOR_CONFIG) as session:
        learner_exp = await session.execute(f"Simulate learner: {content}")

    # Stage 3: Critical subtask
    async with AmplifierSession(config=DIAGNOSTICIAN_CONFIG) as session:
        diagnosis = await session.execute(f"Diagnose: {learner_exp}")

    # Code makes routing decision
    if diagnosis["severity"] == "critical":
        # Jump to different flow
        return await handle_critical_issues(content, diagnosis)

    # Stage 4: Creative subtask (with human approval)
    print(f"Diagnosis: {diagnosis}")
    if not get_human_approval():
        return {"status": "rejected"}

    async with AmplifierSession(config=IMPROVER_CONFIG) as session:
        improvements = await session.execute(f"Improve: {diagnosis}")

    return improvements
```

**3. State Management**

Scenario tools manage state across stages:

```python
# state.py
STATE_FILE = ".tutorial_analyzer_state.json"

def save_state(data: dict):
    """Save state after each stage for resumability."""
    Path(STATE_FILE).write_text(json.dumps(data, indent=2))

def load_state() -> dict:
    """Load state to resume from checkpoint."""
    if Path(STATE_FILE).exists():
        return json.loads(Path(STATE_FILE).read_text())
    return {}

# Usage in main.py
async def resume_or_start(tutorial_path: Path):
    """Resume from checkpoint or start fresh."""
    state = load_state()

    # Stage 1: Analyze (skip if already done)
    if "analysis" not in state:
        async with AmplifierSession(config=ANALYZER_CONFIG) as session:
            state["analysis"] = await session.execute(...)
        save_state(state)  # Checkpoint

    # Stage 2: Simulate (skip if already done)
    if "simulation" not in state:
        async with AmplifierSession(config=SIMULATOR_CONFIG) as session:
            state["simulation"] = await session.execute(...)
        save_state(state)  # Checkpoint

    # Continue from where we left off...
```

---

## Building Your Own Scenario Tool

### Step 1: Design the Metacognitive Recipe

**Identify cognitive stages**:

- What different kinds of thinking does this task need?
- Which stages need precision? Creativity? Judgment?
- Where does human input add value?

**Example - Document analyzer**:

1. **Analyze structure** (precise, temp=0.3)
2. **Extract insights** (analytical, temp=0.4)
3. **Generate summary** (creative, temp=0.6)
4. **Score quality** (evaluative, temp=0.2)
5. **Refine if needed** (loop)

### Step 2: Create Config Modules

One module per cognitive stage:

```
my_analyzer/
  analyzer/core.py          # Stage 1 config
  extractor/core.py         # Stage 2 config
  synthesizer/core.py       # Stage 3 config
  evaluator/core.py         # Stage 4 config
```

Each module exports a `CONFIG` constant:

```python
# analyzer/core.py
from amplifier_core import AmplifierSession

ANALYZER_CONFIG = {
    "session": {
        "orchestrator": "loop-basic",
        "context": "context-simple"
    },
    "providers": [{
        "module": "provider-anthropic",
        "source": "git+https://github.com/microsoft/amplifier-module-provider-anthropic@main",
        "config": {
            "model": "claude-sonnet-4-5",
            "temperature": 0.3,
            "system_prompt": """You are an expert document structure analyzer.

Your task is to analyze document structure and organization.

Output JSON with:
- sections: list of sections found
- clarity_score: 0-1
- issues: list of structural issues
"""
        }
    }],
}
```

### Step 3: Implement Orchestration

```python
# main.py
import asyncio
import click
from pathlib import Path
from amplifier_core import AmplifierSession

from analyzer.core import ANALYZER_CONFIG
from synthesizer.core import SYNTHESIZER_CONFIG
from state import save_state, load_state


@click.command()
@click.argument("input_dir", type=click.Path(exists=True))
@click.option("--resume", is_flag=True, help="Resume from checkpoint")
def main(input_dir: str, resume: bool):
    """Analyze documents with multi-stage AI pipeline."""

    input_path = Path(input_dir)

    if resume:
        state = load_state()
    else:
        state = {"stage": "ANALYZE", "results": {}}

    asyncio.run(run_pipeline(input_path, state))


async def run_pipeline(input_path: Path, state: dict):
    """Execute multi-stage pipeline."""

    # Stage 1: Analyze (if not already done)
    if "analysis" not in state["results"]:
        click.echo("Stage 1: Analyzing structure...")

        async with AmplifierSession(config=ANALYZER_CONFIG) as session:
            analysis = await session.execute(f"Analyze: {input_path}")

        state["results"]["analysis"] = analysis
        save_state(state)  # Checkpoint

    # Stage 2: Synthesize
    if "synthesis" not in state["results"]:
        click.echo("Stage 2: Synthesizing insights...")

        async with AmplifierSession(config=SYNTHESIZER_CONFIG) as session:
            synthesis = await session.execute(
                f"Synthesize: {state['results']['analysis']}"
            )

        state["results"]["synthesis"] = synthesis
        save_state(state)  # Checkpoint

    # Output results
    click.echo(f"\nResults: {state['results']['synthesis']}")


if __name__ == "__main__":
    main()
```

### Step 4: Add Package Metadata

```toml
# pyproject.toml
[project]
name = "my-analyzer"
version = "1.0.0"
description = "Multi-stage document analyzer"

dependencies = [
    "click>=8.1.0",
]

[project.scripts]
my-analyzer = "my_analyzer.main:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

### Step 5: Document for Users and Builders

**README.md** (user-facing):

```markdown
# My Analyzer

Multi-stage document analyzer using specialized AI configs.

## Installation

uv tool install my-analyzer

# Or: uvx --from my-analyzer my-analyzer [args]

## Usage

# Analyze directory

my-analyzer docs/

# Resume from checkpoint

my-analyzer docs/ --resume

## What It Does

1. Analyzes structure (precise AI)
2. Extracts insights (analytical AI)
3. Synthesizes findings (creative AI)
4. Outputs results
```

**HOW_TO_BUILD.md** (contributor-facing):

```markdown
# How to Build My Analyzer

## Metacognitive Recipe

Stage 1: ANALYZER (temp=0.3, analytical)
↓
Stage 2: SYNTHESIZER (temp=0.6, creative)
↓
Output

## Configs

- analyzer/core.py: Structure analysis
- synthesizer/core.py: Insight synthesis

## Flow Control

Coded in main.py:

- Sequential execution
- Checkpointing after each stage
- Resume capability via --resume flag

## Testing

pytest tests/
uv run my-analyzer test_data/
```

### Step 6: Test and Iterate

```bash
# Local testing
cd scenario-tools/my_analyzer
uv run python main.py test_input/

# Install locally
uv tool install .

# Test installed version
my-analyzer test_input/

# Uninstall
uv tool uninstall my-analyzer
```

---

## Multi-Config Patterns and Temperature Selection

For multi-config pattern reference and temperature selection guidance, see [TOOLKIT_GUIDE.md - The Multi-Config Pattern](TOOLKIT_GUIDE.md#the-multi-config-pattern).

---

## State Management and Progress Tracking

For checkpointing patterns and progress reporting, see [BEST_PRACTICES.md - State Management](BEST_PRACTICES.md).

---

## Error Handling

For error handling patterns (graceful degradation, clear messages, validation), see [BEST_PRACTICES.md - Error Handling](BEST_PRACTICES.md).

---

## Packaging for Collections

For packaging scenario tools in collections, see [PACKAGING_GUIDE.md - Scenario Tools](PACKAGING_GUIDE.md).

---

## Toolkit Utilities

For toolkit utility reference (file operations, progress reporting, validation), see [TOOLKIT_GUIDE.md - Utilities Package](TOOLKIT_GUIDE.md#1-utilities-package-amplifier_collection_toolkit).

---

## Best Practices for Scenario Tools

For comprehensive best practices, see [BEST_PRACTICES.md](BEST_PRACTICES.md).

---

## Example: Tutorial Analyzer

The `tutorial_analyzer` in the toolkit is the pedagogical exemplar. Study it to understand:

**Six specialized configs**:

1. **Analyzer** (temp=0.3) - Structure analysis
2. **Learner Simulator** (temp=0.5) - User perspective
3. **Diagnostician** (temp=0.1) - Issue identification
4. **Improver** (temp=0.7) - Improvement generation
5. **Critic** (temp=0.2) - Quality scoring
6. **Synthesizer** (temp=0.3) - Results synthesis

**Complex flow control**:

- Multi-stage pipeline
- Quality loops (improve until score > threshold)
- Human approval gates
- Nested evaluations
- State checkpointing

**Complete documentation**:

- README.md - User guide
- HOW_TO_BUILD.md - Builder guide
- Inline comments explaining recipe

See: `scenario-tools/tutorial-analyzer/`

---

## Advanced Flow Control

For advanced patterns (nested loops, conditional jumps, dynamic config selection, partial failure handling), see [METACOGNITIVE_RECIPES.md](METACOGNITIVE_RECIPES.md).

---

## Testing Scenario Tools

### Unit Testing Configs

```python
# tests/test_configs.py
import pytest
from analyzer.core import ANALYZER_CONFIG

def test_analyzer_config():
    """Verify analyzer config structure."""

    assert "session" in ANALYZER_CONFIG
    assert "providers" in ANALYZER_CONFIG

    provider = ANALYZER_CONFIG["providers"][0]
    assert provider["config"]["temperature"] == 0.3  # Analytical
    assert "claude-sonnet" in provider["config"]["model"]
```

### Integration Testing

```python
# tests/test_pipeline.py
import pytest
from pathlib import Path
from main import run_pipeline

@pytest.mark.asyncio
async def test_complete_pipeline(tmp_path):
    """Test full pipeline on sample input."""

    # Create test input
    test_file = tmp_path / "test.md"
    test_file.write_text("# Test Document\n\nSample content.")

    # Run pipeline
    state = {"stage": "ANALYZE", "results": {}}
    result = await run_pipeline(tmp_path, state)

    # Verify results
    assert "analysis" in result["results"]
    assert "synthesis" in result["results"]
```

### Manual Testing

```bash
# Test with real input
uv run python main.py test_data/

# Test resumability
uv run python main.py test_data/ --resume

# Test error handling
uv run python main.py empty_dir/  # Should fail gracefully
```

---

## Learning Path

**1. Study the exemplar**:

- Read: `scenario-tools/tutorial-analyzer/README.md`
- Understand: Multi-config pattern, state management, flow control
- Run: Test with sample tutorials

**2. Read advanced guides**:

- [TOOLKIT_GUIDE.md](TOOLKIT_GUIDE.md) - Complete toolkit reference
- `METACOGNITIVE_RECIPES.md` - Advanced patterns
- `HOW_TO_CREATE_YOUR_OWN.md` - Step-by-step creation

**3. Build your own**:

- Start simple (2-3 stages)
- Add complexity as needed
- Test thoroughly
- Document the recipe

---

## Related Documentation

- [TOOLKIT_GUIDE.md](TOOLKIT_GUIDE.md) - Toolkit utilities and multi-config patterns

---

**Document Version**: 1.0
**Last Updated**: 2025-10-26
