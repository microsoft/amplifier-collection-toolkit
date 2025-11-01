# How Tutorial Analyzer is Built

**Pedagogical Exemplar: Multi-Config Metacognitive Recipe Pattern**

This document explains the internal architecture of tutorial-analyzer as a learning resource for building your own sophisticated scenario tools.

---

## Core Philosophy

**Key Principle**: Code for structure, AI for intelligence

- **Code orchestrates**: Decides which config when, manages state, controls flow
- **Specialized configs think**: Each cognitive task gets optimized AI setup
- **No compromises**: Each stage uses the perfect temperature and model for its role

---

## Architecture Overview

### Six Specialized Configs

Each config is optimized for a specific cognitive role:

| Stage | Role | Temperature | Model | Why |
|-------|------|-------------|-------|-----|
| **Analyzer** | Analytical | 0.3 | Sonnet | Precise structure extraction |
| **Learner Simulator** | Empathetic | 0.5 | Opus | Perspective-taking |
| **Diagnostician** | Diagnostic | 0.1 | Sonnet | Precise issue identification |
| **Improver** | Creative | 0.7 | Opus | Improvement generation |
| **Critic** | Evaluative | 0.2 | Sonnet | Quality scoring |
| **Synthesizer** | Analytical | 0.3 | Sonnet | Results synthesis |

**Why different temps?**
- Analysis needs precision (0.1-0.3)
- Creativity needs exploration (0.6-0.8)
- Evaluation needs judgment (0.1-0.3)

One config at 0.5 would compromise all tasks.

### Directory Structure

```
src/tutorial_analyzer/
  ├── main.py                      # Orchestration logic
  ├── state.py                     # Checkpoint management
  ├── utils.py                     # Shared utilities
  │
  ├── analyzer/
  │   ├── __init__.py
  │   └── core.py                  # ANALYZER_CONFIG
  │
  ├── learner_simulator/
  │   ├── __init__.py
  │   └── core.py                  # LEARNER_SIMULATOR_CONFIG
  │
  ├── diagnostician/
  │   ├── __init__.py
  │   └── core.py                  # DIAGNOSTICIAN_CONFIG
  │
  ├── improver/
  │   ├── __init__.py
  │   └── core.py                  # IMPROVER_CONFIG
  │
  ├── critic/
  │   ├── __init__.py
  │   └── core.py                  # CRITIC_CONFIG
  │
  └── synthesizer/
      ├── __init__.py
      └── core.py                  # SYNTHESIZER_CONFIG
```

**Pattern**: One module per cognitive stage, each exporting a `CONFIG` constant.

---

## Implementation Details

### Config Module Pattern

Each cognitive stage follows the same pattern:

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
            "temperature": 0.3,  # Precise analysis
            "system_prompt": """You are an expert tutorial structure analyzer.

Your task is to analyze tutorial structure and organization.

Output JSON with:
- sections: list of sections found
- clarity_score: 0-1
- issues: list of structural issues
"""
        }
    }],
}
```

**Key elements**:
- Config is a constant (not a function)
- Temperature optimized for cognitive role
- System prompt defines task clearly
- Specifies output format (JSON)

### Orchestration Logic

`main.py` orchestrates the pipeline:

```python
async def analyze_tutorial(tutorial_path: Path) -> dict:
    """Multi-stage metacognitive recipe."""

    content = tutorial_path.read_text()
    state = load_state()

    # Stage 1: Analyze structure (if not already done)
    if "analysis" not in state:
        async with AmplifierSession(config=ANALYZER_CONFIG) as session:
            analysis = await session.execute(f"Analyze: {content}")
        state["analysis"] = analysis
        save_state(state)  # Checkpoint

    # Stage 2: Simulate learner
    if "simulation" not in state:
        async with AmplifierSession(config=LEARNER_SIMULATOR_CONFIG) as session:
            simulation = await session.execute(
                f"Simulate learner experiencing: {content}"
            )
        state["simulation"] = simulation
        save_state(state)  # Checkpoint

    # Stage 3: Diagnose issues
    if "diagnosis" not in state:
        async with AmplifierSession(config=DIAGNOSTICIAN_CONFIG) as session:
            diagnosis = await session.execute(
                f"Diagnose issues from: {state['simulation']}"
            )
        state["diagnosis"] = diagnosis
        save_state(state)  # Checkpoint

    # Code makes routing decision
    if diagnosis["severity"] == "critical":
        return await handle_critical_issues(content, diagnosis)

    # Stage 4: Generate improvements (with human approval)
    print(f"Diagnosis: {diagnosis}")
    if not get_human_approval():
        return {"status": "rejected"}

    if "improvements" not in state:
        async with AmplifierSession(config=IMPROVER_CONFIG) as session:
            improvements = await session.execute(
                f"Generate improvements for: {diagnosis}"
            )
        state["improvements"] = improvements
        save_state(state)  # Checkpoint

    # Stage 5: Evaluate quality
    if "evaluation" not in state:
        async with AmplifierSession(config=CRITIC_CONFIG) as session:
            evaluation = await session.execute(
                f"Evaluate quality: {state['improvements']}"
            )
        state["evaluation"] = evaluation
        save_state(state)  # Checkpoint

    # Quality loop: retry if below threshold
    if evaluation["score"] < 0.8 and state.get("iteration", 0) < 3:
        state["iteration"] = state.get("iteration", 0) + 1
        del state["improvements"]  # Retry improvement generation
        save_state(state)
        return await analyze_tutorial(tutorial_path)  # Recursive retry

    # Stage 6: Synthesize final recommendations
    if "synthesis" not in state:
        async with AmplifierSession(config=SYNTHESIZER_CONFIG) as session:
            synthesis = await session.execute(
                f"Synthesize recommendations: {state}"
            )
        state["synthesis"] = synthesis
        save_state(state)  # Checkpoint

    return state
```

**Key patterns**:
- **Checkpointing**: Save after every expensive operation
- **Resumability**: Check `if "stage" not in state` before running
- **Human gates**: Get approval before expensive creative work
- **Quality loops**: Retry if evaluation score below threshold
- **Code decisions**: Use routing logic based on results
- **Direct AmplifierSession usage**: No wrappers

### State Management

`state.py` provides simple checkpointing:

```python
# state.py
import json
from pathlib import Path

STATE_FILE = ".tutorial_analyzer_state.json"

def save_state(data: dict):
    """Save state after each stage for resumability."""
    Path(STATE_FILE).write_text(json.dumps(data, indent=2))

def load_state() -> dict:
    """Load state to resume from checkpoint."""
    if Path(STATE_FILE).exists():
        return json.loads(Path(STATE_FILE).read_text())
    return {}

def clear_state():
    """Clear state to start fresh."""
    if Path(STATE_FILE).exists():
        Path(STATE_FILE).unlink()
```

**Philosophy**:
- Simple JSON file (no database)
- Tool owns its state (no state framework)
- Explicit save points
- Easy to inspect/debug

---

## Flow Control Patterns

### Pattern 1: Sequential Pipeline

```python
# Stage 1
result1 = await run_with_config(CONFIG_1, input)

# Stage 2 (uses Stage 1 output)
result2 = await run_with_config(CONFIG_2, result1)

# Stage 3 (uses Stage 2 output)
result3 = await run_with_config(CONFIG_3, result2)
```

**When**: Each stage depends on previous output

### Pattern 2: Quality Loop

```python
max_iterations = 3

for iteration in range(max_iterations):
    # Generate
    draft = await run_with_config(GENERATOR_CONFIG, prompt)

    # Evaluate
    score = await run_with_config(EVALUATOR_CONFIG, draft)

    if score >= 0.8:
        return draft  # Good enough

    # Improve prompt for next iteration
    prompt = f"{prompt}\n\nPrevious scored {score}. Improve."

return draft  # Return best attempt
```

**When**: Need to iterate until quality threshold met

### Pattern 3: Human Approval Gate

```python
# Generate plan
plan = await run_with_config(PLANNER_CONFIG, task)

# Human decides
print(f"Proposed Plan:\n{plan}\n")
if not get_human_approval():
    return {"status": "rejected"}

# Implement approved plan
result = await run_with_config(IMPLEMENTER_CONFIG, plan)
```

**When**: Human judgment needed at strategic points

### Pattern 4: Conditional Routing

```python
# Analyze
analysis = await run_with_config(ANALYZER_CONFIG, input)

# Code decides next step based on analysis
if analysis["complexity"] == "high":
    return await deep_analysis_flow(input)
elif analysis["complexity"] == "medium":
    return await standard_flow(input)
else:
    return await quick_flow(input)
```

**When**: Different inputs need different processing

---

## Design Decisions

### Why No Generic State Framework?

**Alternative**: Create `GenericStateManager` class

**Problem**:
- Adds abstraction layer
- More complex than needed
- Each tool has different state needs

**Solution**: Each tool owns its state
- Simple JSON file
- Explicit save/load
- Easy to understand and debug

### Why Direct AmplifierSession Usage?

**Alternative**: Create `ToolSession` wrapper

**Problem**:
- Hides kernel mechanisms
- Adds unnecessary abstraction
- Makes debugging harder

**Solution**: Use AmplifierSession directly
- Clear what's happening
- No hidden behavior
- Easy to customize per stage

### Why Separate Module Per Stage?

**Alternative**: All configs in `main.py`

**Problem**:
- `main.py` becomes huge
- Configs not reusable
- Hard to understand each stage

**Solution**: One module per stage
- Self-contained
- Clear purpose
- Easy to modify individual stages

### Why Checkpoint After Every Stage?

**Alternative**: Save only at end

**Problem**:
- Lose all work if interrupted
- Can't debug intermediate stages
- Must re-run everything on failure

**Solution**: Save after each expensive operation
- Resume from where left off
- Debug specific stages
- Preserve expensive LLM calls

---

## Testing Strategy

### Unit Tests

Test configs are valid:

```python
# tests/test_configs.py
def test_analyzer_config():
    """Verify analyzer config structure."""
    assert "session" in ANALYZER_CONFIG
    assert "providers" in ANALYZER_CONFIG
    assert ANALYZER_CONFIG["providers"][0]["config"]["temperature"] == 0.3
```

### Integration Tests

Test orchestration logic:

```python
# tests/test_orchestration.py
@pytest.mark.asyncio
async def test_analyze_tutorial(tmp_path):
    """Test full pipeline."""
    test_file = tmp_path / "test.md"
    test_file.write_text("# Test Tutorial\n\nContent.")

    result = await analyze_tutorial(test_file)

    assert "analysis" in result
    assert "diagnosis" in result
    assert "synthesis" in result
```

### Manual Testing

Test with real tutorials:

```bash
tutorial-analyzer docs/examples/sample_tutorial.md
```

---

## Common Pitfalls to Avoid

### ❌ One Config for Everything

```python
# BAD: Generic config
GENERIC_CONFIG = {"temperature": 0.5, ...}

# Analysis compromised (needs 0.3)
# Creativity compromised (needs 0.7)
# Evaluation compromised (needs 0.2)
```

### ❌ Forgetting Checkpoints

```python
# BAD: No checkpoints
result1 = await stage1()
result2 = await stage2()  # Crash here = lose stage1 work
result3 = await stage3()
```

### ❌ Silent Processing

```python
# BAD: No progress visibility
for item in items:
    process(item)  # User has no idea what's happening
```

### ❌ No Input Validation

```python
# BAD: Fail late
async def analyze(path):
    content = path.read_text()  # Crash if path invalid
    # 10 minutes of processing...
    # Then discover content invalid
```

---

## Extending the Tool

### Adding a New Stage

1. Create new module:
   ```bash
   mkdir src/tutorial_analyzer/new_stage
   touch src/tutorial_analyzer/new_stage/__init__.py
   touch src/tutorial_analyzer/new_stage/core.py
   ```

2. Define config in `core.py`:
   ```python
   NEW_STAGE_CONFIG = {
       "session": {...},
       "providers": [{
           "config": {
               "temperature": 0.X,  # Choose appropriately
               "system_prompt": "..."
           }
       }]
   }
   ```

3. Add to pipeline in `main.py`:
   ```python
   if "new_stage" not in state:
       async with AmplifierSession(config=NEW_STAGE_CONFIG) as session:
           result = await session.execute(...)
       state["new_stage"] = result
       save_state(state)
   ```

### Modifying Temperature

**Analyze impact first**:
- Lower temp (0.1-0.3): More deterministic, less creative
- Mid temp (0.4-0.6): Balanced
- Higher temp (0.7-0.9): More creative, less deterministic

**Test thoroughly**: Temperature changes affect output quality

### Adding Quality Checks

```python
# After any stage
if not validate_output(state["stage_name"]):
    logger.warning("Stage output failed validation, retrying...")
    del state["stage_name"]
    return await analyze_tutorial(tutorial_path)
```

---

## Key Learnings

### 1. Multi-Config is Essential

One config can't optimize for different cognitive tasks. Each stage needs its own temperature and prompt.

### 2. Code Orchestrates, AI Thinks

Code decides flow control, routing, retries. AI focuses on cognitive tasks. Clear separation.

### 3. Checkpointing is Critical

LLM calls are expensive. Save after every stage. Enables resumability and debugging.

### 4. State Simplicity Wins

JSON file beats complex state frameworks. Easy to inspect, debug, and understand.

### 5. Direct Session Usage

Don't wrap `AmplifierSession`. Use it directly. Clearer what's happening.

---

## Related Patterns

See **[../../docs/METACOGNITIVE_RECIPES.md](../../docs/METACOGNITIVE_RECIPES.md)** for more patterns:

- Parallel analysis with convergence
- Nested quality loops
- Dynamic config selection
- Partial failure handling
- Human-in-loop variations

---

## Building Your Own Tool

**Start here**:
1. Read **[../../docs/HOW_TO_CREATE_YOUR_OWN.md](../../docs/HOW_TO_CREATE_YOUR_OWN.md)**
2. Copy **[../../templates/standalone_tool.py](../../templates/standalone_tool.py)**
3. Study this tutorial-analyzer implementation
4. Define your cognitive stages
5. Create configs (one per stage)
6. Implement orchestration
7. Add checkpointing
8. Test thoroughly

**Remember**: Start simple (2-3 stages), add complexity as needed.

---

**This tool is a pedagogical exemplar**. Study it, modify it, use it as a template. The pattern scales from simple tools (2 configs) to complex pipelines (10+ configs).

The code is the teaching material.
