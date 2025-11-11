# Toolkit Shared Context: Multi-Config Metacognitive Recipes

**Constitutional knowledge for building sophisticated scenario tools using multi-config patterns**

---

## What Are Metacognitive Recipes?

**Metacognitive recipes** are structured thinking processes where **code orchestrates multiple specialized AI sessions**, each optimized for a specific cognitive role.

### The Core Problem

One AI configuration cannot optimize for all thinking modes:
- **Analytical tasks** need precision (temp=0.3)
- **Creative tasks** need exploration (temp=0.7)
- **Evaluative tasks** need consistency (temp=0.2)

Single-config approaches compromise quality across all tasks.

### The Multi-Config Solution

Each cognitive subtask gets its own optimized configuration:

```
Code orchestrates: Analyze (temp=0.3) → Create (temp=0.7) → Evaluate (temp=0.2)
```

**Benefits**:
- Each config optimized for its cognitive role
- Fresh context per stage (no pollution)
- Isolated failures (one stage doesn't kill others)
- Code controls flow (deterministic, debuggable)

---

## Core Principles

### 1. Mechanism vs Policy

- **AmplifierSession** = MECHANISM (kernel provides capability)
- **Config dicts** = POLICY (tools decide temperature, model, prompts, orchestration)
- **Code orchestration** = POLICY (tools decide flow, loops, routing)

The kernel doesn't care what configs you use. It just executes. **This is correct.**

### 2. Code Orchestrates, AI Executes Thinking

**Code decides**:
- Which config to use when
- Flow control (loops, conditionals, jumps)
- State management across stages
- When to involve humans

**AI executes**:
- Analytical thinking (with analytical config)
- Creative thinking (with creative config)
- Evaluative thinking (with evaluative config)

### 3. Ruthless Simplicity Through Composition

- Each config: Simple dict with optimized values
- Each stage: One focused task
- Code orchestration: Clear flow logic
- **Sophistication emerges from composition of simple pieces**

### 4. AmplifierSession Direct Use (NEVER Wrap)

```python
# RIGHT: Use directly with specialized configs
async with AmplifierSession(config=ANALYZER_CONFIG) as session:
    result = await session.execute(prompt)

# WRONG: Wrapping the mechanism
class LLMHelper:
    def __init__(self):
        self.session = AmplifierSession(...)  # Don't do this!
```

**Why**: Violates "use mechanisms directly" - adds unnecessary abstraction.

### 5. Tool-Owned State (No Frameworks)

```python
# Each tool owns its simple state
STATE_FILE = ".my_tool_state.json"

def save_state(state: dict):
    Path(STATE_FILE).write_text(json.dumps(state, indent=2))

def load_state() -> dict:
    return json.loads(Path(STATE_FILE).read_text()) if Path(STATE_FILE).exists() else {}
```

**Why**: State management is tool-specific policy, not toolkit mechanism.

---

## The Canonical Exemplar

**@toolkit:scenario-tools/blog-writer/** is THE standard all scenario tools MUST follow:

- **5 specialized configs** (style_analyzer, draft_writer, source_reviewer, style_reviewer, feedback_incorporator)
- **Quality loops** (source accuracy, style consistency)
- **Interactive UX** (pause/edit/continue)
- **Documentation structure** (README.md + HOW_TO_BUILD.md)
- **Code organization** (pipeline.py + stage modules + state.py + cli.py)

When building tools: Study blog-writer, model after blog-writer, reference blog-writer.

---

## Anti-Patterns (What NOT to Do)

### #1 CRITICAL: Wrapping AmplifierSession
❌ Creating LLMHelper classes or session managers
✅ Use AmplifierSession directly with specialized configs

### #2 CRITICAL: Single-Config for Multi-Stage
❌ One config trying to handle analytical AND creative AND evaluative tasks
✅ Specialized config per cognitive role

### #3 CRITICAL: Generic State Frameworks
❌ Creating reusable state management classes
✅ Simple dict to JSON per tool

### #4: No Checkpointing
❌ Save state only at end
✅ `save_state()` after every expensive stage

### #5: AI Decides Flow
❌ Asking AI "if quality low, regenerate, else continue"
✅ Code checks quality, decides to iterate: `if score < threshold: regenerate()`

### #6: Not Following Blog-Writer Standard
❌ Creating own documentation structure
✅ Match blog-writer's README and HOW_TO_BUILD exactly

### #7: Toolkit for LLM Operations
❌ Using toolkit helpers for LLM calls
✅ AmplifierSession directly, toolkit for file/progress/validation only

---

## Decision Framework: When to Use Multi-Config

```
Does task involve multiple distinct cognitive roles?
├─ NO → Single config may suffice
└─ YES ↓

Do different stages need different temperatures?
├─ NO → Single config may suffice
└─ YES ↓

Is this a multi-stage workflow?
├─ NO → Consider simpler approach
└─ YES ↓

Would single-config compromise quality?
├─ NO → Single config acceptable
└─ YES → ✓ USE MULTI-CONFIG PATTERN
```

---

## Toolkit Resources

### Essential Documentation
- `@toolkit:docs/TOOLKIT_GUIDE.md` - Complete multi-config pattern reference
- `@toolkit:docs/METACOGNITIVE_RECIPES.md` - Advanced patterns and flow control
- `@toolkit:docs/HOW_TO_CREATE_YOUR_OWN.md` - Step-by-step creation guide
- `@toolkit:docs/BEST_PRACTICES.md` - Strategic guidance
- `@toolkit:docs/PHILOSOPHY.md` - Mechanism vs policy alignment

### Exemplars
- `@toolkit:scenario-tools/blog-writer/` - **THE canonical standard** (5 configs, quality loops, interactive UX)
- `@toolkit:scenario-tools/tutorial-analyzer/` - Complex example (6 configs, human-in-loop, nested loops)
- `@toolkit:templates/standalone_tool.py` - Basic starting template

### Toolkit Utilities (Structural Only)
- `discover_files(path, "**/*.md")` - Recursive file discovery
- `ProgressReporter(count, desc)` - Progress display
- `validate_input_path()`, `require_minimum_files()` - Input validation

**NOT for LLM operations** - Use AmplifierSession directly for all AI tasks.

---

## Philosophy Alignment

### Policy at Edges
Standalone tools ARE the edges. They make ALL policy decisions:
- Which models (haiku, sonnet, opus)
- What temperatures (0.3, 0.5, 0.7)
- Which orchestrators (basic, streaming)
- When to use which config
- How to combine results

### Small, Stable, Boring (Kernel)
- Kernel unchanged by toolkit patterns
- No new APIs needed
- Just executing configs with prompts
- The center stays still so the edges can move fast

### Code for Structure, AI for Intelligence
- **Code**: Orchestrates flow, manages state, decides routing
- **AI**: Executes thinking with specialized configs
- Each does what it does best

---

**This is the constitutional foundation. For detailed implementation patterns, see agent and profile-specific instructions.**
