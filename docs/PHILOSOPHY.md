# Toolkit Philosophy: Mechanism vs Policy, Multi-Config at Edges

## Core Principle: Standalone Tools ARE the Edges

Standalone tools built with this toolkit are **policy-making edges** in the Amplifier ecosystem. They make all decisions about configuration, flow, and behavior. The kernel (amplifier-core) provides only mechanisms.

**The division of responsibility**:

- **Kernel (amplifier-core)**: Provides `AmplifierSession` - the mechanism to execute with any config
- **Tools (this toolkit)**: Make ALL policy decisions - which configs, when to use them, how to orchestrate

## Why Multi-Config?

### The Single-Config Limitation

One config attempts to serve all cognitive tasks - analysis (needs precision), creation (needs creativity), evaluation (needs consistency).

**Problems**:

- **Temperature compromise**: Can't optimize for precision (temp=0.3) AND creativity (temp=0.7)
- **Attention dilution**: Generic prompt not optimized for any specific task
- **Context pollution**: All tasks share one session, context accumulates
- **Failure cascade**: One mistake affects all subsequent tasks

### The Multi-Config Solution

Each cognitive subtask gets its own optimized configuration:

- **Analytical config** (temp=0.3): Structure extraction, classification
- **Creative config** (temp=0.7): Content generation, ideation
- **Evaluative config** (temp=0.2): Quality assessment, scoring

Code orchestrates which config to use when, managing flow between specialized sessions.

**Benefits**:

- **Optimized temperatures**: Each task gets its ideal temperature
- **Focused attention**: Each session has one clear job
- **Fresh context**: Each stage starts clean
- **Isolated failures**: One stage failing doesn't kill the rest

For implementation examples, see [TOOLKIT_GUIDE.md - The Multi-Config Pattern](TOOLKIT_GUIDE.md#the-multi-config-pattern).

## Alignment with Kernel Philosophy

### Mechanism Not Policy

**Kernel provides mechanism**: `AmplifierSession` executes with any config provided.

**Tool makes policy decisions**:
- Which model (haiku, sonnet, opus)
- What temperature (0.1, 0.5, 0.8)
- Which orchestrator (basic, streaming)
- What system prompt
- When to use which config
- How to combine results
- When to loop or iterate

The kernel doesn't care. It just executes. **This is correct.**

### Policy at Edges

Standalone tools **ARE** the edges. They make all policy decisions about their behavior:
- Define multiple specialized configs (analytical, creative, evaluative)
- Decide flow based on results (if needs research → use research config, else → use creator config)
- Manage their own state and checkpointing
- Determine when to involve humans

No one else decides for you. **This is correct.**

### Ruthless Simplicity

**Each piece stays simple**:

- Each config: Simple dict with a few optimized values
- Each stage: One focused task with one config
- Code orchestration: Clear flow logic
- State management: Simple dict to JSON

**Sophistication emerges from composition**:

- Multiple simple configs
- Clear orchestration logic
- Well-defined stages

**No unnecessary abstraction**:

- No session wrappers (use AmplifierSession directly)
- No state frameworks (simple dict per tool)
- No config builders (just dict literals)

### Small, Stable, Boring (Kernel)

**Kernel stays unchanged**:

- `AmplifierSession` interface same
- Load modules, execute prompts
- No new APIs needed

**Tools innovate at edges**:

- New metacognitive recipes
- New config combinations
- New orchestration patterns
- New flow control strategies

The center stays still so the edges can move fast. **This is correct.**

## Build-Time vs Runtime Configuration

### Standalone Tools Make Build-Time Decisions

**CLI applications** (like `amplifier`) allow users to choose behavior at runtime through profiles and flags.

**Standalone tools** make policy decisions at **build time** - the tool author decides which models, temperatures, and orchestration patterns to use. Users invoke the tool but don't configure its internal choices.

### Standalone Tools Are Opinionated

Each standalone tool is a **specific solution** to a **specific problem** with **specific choices baked in**:

- Which models (sonnet vs opus vs haiku)
- Which temperatures (0.1 vs 0.5 vs 0.8)
- How many configs (2 vs 6 vs 10)
- Which cognitive stages (simulate learner? skip simulation?)
- When humans approve (autonomous vs gated)

These are **policy decisions made by tool author**, not runtime choices for users.

Users who want different behavior create **different tools**. No dynamic configuration needed.

### Module Loading Works Directly

Standalone tools install amplifier modules as dependencies:

```toml
# pyproject.toml
[project]
dependencies = [
    "amplifier-core",
]

[project.optional-dependencies]
amplifier = [
    "amplifier-module-provider-anthropic @ git+https://github.com/...",
    "amplifier-module-loop-streaming @ git+https://github.com/...",
]
```

Modules discovered automatically via entry points. No profile loading or dynamic resolution needed.

## Configuration Sophistication Spectrum

Standalone tools can use three levels of configuration sophistication:

### Level 1: Fixed Configs (90% of tools)

**Policy decision at build time**:

```python
# Tool author decides these values when building tool
ANALYZER_CONFIG = {
    "session": {"orchestrator": "loop-basic"},
    "providers": [{
        "module": "provider-anthropic",
        "source": "git+https://github.com/...",
        "config": {
            "model": "claude-sonnet-4-5",
            "temperature": 0.3,
            "system_prompt": "You are an expert analyzer."
        }
    }]
}

# Same config every time tool runs - predictable, safe
```

**Philosophy alignment**: ✅ Perfect

- Mechanism not policy: Kernel unchanged, tool makes policy once
- Policy at edges: Tool decides, kernel executes
- Ruthless simplicity: Define once, use everywhere
- Small, stable, boring: No dynamic behavior

### Level 2: Code-Modified Configs (8% of tools)

**Policy decision at runtime, bounded by code**:

```python
# Base template with policy boundaries
BASE_CONFIG = {
    "session": {"orchestrator": "loop-streaming"},
    "providers": [{"module": "provider-anthropic", "config": {}}],
    "tools": []  # Code decides which tools
}

def create_config(task_type: str) -> dict:
    """Code makes bounded policy decisions."""
    config = copy.deepcopy(BASE_CONFIG)

    # Deterministic decisions within predefined options
    if task_type == "deep_research":
        config["providers"][0]["config"] = {"model": "claude-opus-4-1", "temperature": 0.3}
        config["tools"].append(WEB_SEARCH_TOOL)
    else:
        config["providers"][0]["config"] = {"model": "claude-sonnet-4-5", "temperature": 0.5}

    return config
```

**Philosophy alignment**: ✅ Good

- Mechanism not policy: Kernel still unchanged
- Policy at edges: Tool's code makes runtime decisions
- Ruthless simplicity: Bounded options, deterministic logic
- Some complexity: Justified by need for adaptability

### Level 3: AI-Generated Configs (2% of tools, EXPLORATORY)

**Policy decision delegated to AI** (low-stakes exploration only):

```python
async def generate_config_for_exploration(topic: str) -> dict:
    """AI creates config for exploration."""

    # AI generates entire config
    async with AmplifierSession(config=META_PLANNER_CONFIG) as session:
        config_json = await session.execute(f"Generate config for exploring: {topic}")

    # CRITICAL: Code validates before using
    generated_config = parse_json(config_json)
    validate_schema(generated_config)
    validate_module_whitelist(generated_config)
    validate_no_dangerous_tools(generated_config)

    # Use for LOW-STAKES exploration only
    async with AmplifierSession(config=generated_config) as session:
        result = await session.execute(f"Explore: {topic}")

    return result
```

**Philosophy alignment**: ⚠️ CAUTION

- Mechanism not policy: ✅ Kernel still unchanged
- Policy at edges: ⚠️ AI controls policy (with code validation)
- Ruthless simplicity: ⚠️ Complex if overused
- Small, stable, boring: ⚠️ Unpredictable behavior

**Use ONLY for**:

- Exploratory research (low stakes)
- Unknown domains (learning)
- Prototyping (not production)

**NEVER for**:

- Production tools
- Security-sensitive tasks
- Well-understood domains

## When to Use Toolkit Utilities

### Use Toolkit For

**Structural operations**:

- File discovery: `discover_files(path, "**/*.md")`
- Progress reporting: `ProgressReporter(count, description)`
- Input validation: `validate_input_path(path, must_be_dir=True)`

**Why**: These are mechanism utilities. They don't make policy decisions. They just provide capabilities your code uses.

### Don't Use Toolkit For

**LLM operations** - Use amplifier-core directly:

- ❌ Don't wrap `AmplifierSession`
- ❌ Don't create LLM helper classes
- ❌ Don't parse LLM responses (amplifier-core handles it)
- ❌ Don't retry LLM calls (orchestrator handles it)

**State management** - Each tool owns its state:

- ❌ Don't create state manager classes
- ❌ Don't generalize state structure
- ✅ Each tool has its own simple state dict

**Why**: These are policy decisions. Each tool decides its own policies. Toolkit doesn't impose them.

## What NOT to Wrap from Amplifier-Core

### Never Wrap These

**AmplifierSession**:

```python
# WRONG: Wrapping the mechanism
class Helper:
    def __init__(self):
        self.session = AmplifierSession(...)

# RIGHT: Use directly
async with AmplifierSession(config=MY_CONFIG) as session:
    result = await session.execute(...)
```

**Providers**:

```python
# WRONG: Direct provider access
from amplifier_module_provider_anthropic import AnthropicProvider
provider = AnthropicProvider()

# RIGHT: Via AmplifierSession
async with AmplifierSession(config=config_with_provider) as session:
    result = await session.execute(...)
```

**Orchestrators**:

```python
# WRONG: Direct orchestrator use
from amplifier_module_loop_streaming import StreamingOrchestrator
orchestrator = StreamingOrchestrator()

# RIGHT: Specify in config, let kernel load
config = {"session": {"orchestrator": "loop-streaming"}}
async with AmplifierSession(config=config) as session:
    # Kernel loaded and wired orchestrator
    result = await session.execute(...)
```

### Why Not Wrap?

**Wrapping creates indirection**:

- Adds complexity without value
- Hides the kernel interface
- Makes debugging harder
- Violates "use mechanisms directly"

**Kernel interfaces are designed for direct use**:

- `AmplifierSession` is the public API
- It's already simple and usable
- Wrapping it makes it more complex, not simpler

## Multi-Config and Kernel Philosophy

### How Multi-Config Aligns

**Mechanism not policy** ✅:

- Kernel: `AmplifierSession.execute(config, prompt)` - pure mechanism
- Tools: Multiple CONFIG dicts - pure policy decisions
- Clean separation

**Policy at edges** ✅:

- Tools ARE the edges
- Tools decide all configs (which model, what temperature, which orchestrator)
- Multiple configs = multiple policy decisions at edges
- Kernel just executes

**Ruthless simplicity** ✅:

- Each config is simple (just a dict with a few values)
- Each stage is simple (one config, one task)
- Code orchestration is simple (clear flow logic)
- Sophistication emerges from composition

**Small, stable, boring (kernel)** ✅:

- Kernel unchanged
- No new APIs needed
- Just executing configs with prompts
- Boring is good

### How Multi-Config Enables Innovation

**Tools can innovate**:

- Try new config combinations
- Experiment with temperatures
- Test different models
- Explore new flow patterns

**Kernel stays stable**:

- Same `AmplifierSession` interface
- Same module loading
- Same event system
- No changes needed

**The center stays still so the edges can move fast.** Multi-config pattern exemplifies this.

## When to Use Multiple Configs

### Indicators You Need Multi-Config

Ask these questions:

**1. Do you have distinct cognitive tasks?**

- Analysis (precise) AND creation (creative)? → Multiple configs
- Evaluation (consistent) AND generation (diverse)? → Multiple configs

**2. Do tasks need different temperatures?**

- Some need precision (temp=0.1-0.3)? → Multiple configs
- Some need creativity (temp=0.6-0.8)? → Multiple configs

**3. Do you have multiple stages?**

- Extract → Synthesize → Evaluate? → Multiple configs
- Analyze → Plan → Implement → Review? → Multiple configs

**4. Do you need different models?**

- Fast analysis (Haiku) and deep creation (Opus)? → Multiple configs

### When Single Config Is Fine

**Indicators you're overthinking**:

- Tool does ONE thing → Single config probably fine
- All tasks similar (all analytical or all creative) → Single config probably fine
- No multi-stage pipeline → Single config probably fine
- No quality loops → Single config probably fine

**Example of appropriate single-config tool**:

```python
# Simple code formatter - one analytical task
FORMATTER_CONFIG = {"temperature": 0.2}

async def format_code(code: str):
    async with AmplifierSession(config=FORMATTER_CONFIG) as session:
        formatted = await session.execute(f"Format this code:\n\n{code}")
    return formatted
```

**No need for multi-config** - it's one focused analytical task.

## The Spectrum: When to Use Which Level

### Decision Framework

```
┌─────────────────────────────────────────────────────────────┐
│ Are task requirements known and unchanging?                  │
│   YES → Level 1 (Fixed configs)                             │
│   NO  → Continue...                                          │
└─────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────┐
│ Does task vary at runtime within bounded options?           │
│   YES → Level 2 (Code-modified configs)                     │
│   NO  → Continue...                                          │
└─────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────┐
│ Is this low-stakes exploration in unknown domain?           │
│   YES → Level 3 (AI-generated, with safeguards)             │
│   NO  → Back to Level 1 (prefer predictability)             │
└─────────────────────────────────────────────────────────────┘
```

**Default**: Level 1 (Fixed configs) - 90% of tools stay here forever

### Philosophy Alignment by Level

**Level 1: Fixed Configs**

- Mechanism not policy: ✅ Perfect
- Policy at edges: ✅ Tool decides once
- Ruthless simplicity: ✅ Maximum
- Boring: ✅ Predictable

**Level 2: Code-Modified**

- Mechanism not policy: ✅ Good
- Policy at edges: ✅ Code at edge decides
- Ruthless simplicity: ⚠️ Some complexity
- Boring: ⚠️ Some dynamism

**Level 3: AI-Generated**

- Mechanism not policy: ✅ Kernel still unchanged
- Policy at edges: ⚠️ AI controls policy
- Ruthless simplicity: ⚠️ Complex if overused
- Boring: ❌ Unpredictable

**Recommendation**: Start Level 1. Stay Level 1 unless you have a specific need for adaptability.

## Common Misconceptions

### Misconception 1: "More configs = more complex"

**Reality**: More configs can mean LESS complexity

**Single config attempting everything**:

```python
# Complex: One config trying to handle all cases
prompt = """You will receive different types of tasks.
For analytical tasks, be precise.
For creative tasks, be diverse.
For evaluative tasks, be consistent.

Task: {task}
Type: {task_type}
"""

# Complexity in prompt engineering to handle all cases
```

**Multiple configs, each simple**:

```python
# Simple: Each config focused on one thing
ANALYZER_CONFIG = {"temperature": 0.3}
CREATOR_CONFIG = {"temperature": 0.7}
EVALUATOR_CONFIG = {"temperature": 0.2}

# Complexity in orchestration (which is code, which is easier)
```

### Misconception 2: "I need complex loading for multiple configs"

**Reality**: Multiple configs are just multiple dicts

```python
# Define all configs directly
CONFIGS = {
    "analyzer": {
        "session": {"orchestrator": "loop-basic"},
        "providers": [{"module": "provider-anthropic", "source": "git+...", "config": {"temperature": 0.3}}]
    },
    "creator": {
        "session": {"orchestrator": "loop-basic"},
        "providers": [{"module": "provider-anthropic", "source": "git+...", "config": {"temperature": 0.7}}]
    },
}

# Code decides which config when
config = CONFIGS["analyzer"]  # or CONFIGS["creator"], etc.
async with AmplifierSession(config=config) as session:
    result = await session.execute(...)
```

CLI apps use profiles for dynamic user choice. Standalone tools make build-time choices.

### Misconception 3: "Multi-config violates simplicity"

**Reality**: Multi-config ENABLES simplicity

**Each config stays simple** (focused, optimized)
**Each stage stays simple** (one task, one config)
**Code orchestration stays simple** (clear flow logic)

**Sophistication emerges from composition of simple pieces**

This is the essence of ruthless simplicity: simple pieces, clear composition.

## Summary

**Toolkit philosophy**:

1. **Standalone tools are policy-making edges** - They decide all configs
2. **Multi-config pattern** - Each cognitive subtask gets optimized config
3. **Code orchestrates thinking** - Flow, state, decisions in code
4. **Use kernel directly** - AmplifierSession without wrappers
5. **Start simple** - Level 1 (fixed configs) for 90% of tools
6. **Add complexity only when needed** - Level 2/3 when justified

**Alignment with kernel philosophy**:

- ✅ Mechanism not policy (kernel provides capability, tools decide configs)
- ✅ Policy at edges (tools ARE edges, make ALL decisions)
- ✅ Ruthless simplicity (each piece simple, composition sophisticated)
- ✅ Small, stable, boring (kernel unchanged, tools innovate)

**Key insight**: The most sophisticated AI tools are built from the simplest pieces - specialized configs and clear orchestration logic. Start simple, compose thoughtfully.

**Next steps**:

1. Study `scenario-tools/tutorial-analyzer/` - See multi-config in action
2. Read `METACOGNITIVE_RECIPES.md` - Understand pattern deeply
3. Read `HOW_TO_CREATE_YOUR_OWN.md` - Build your own tool
4. Start with Level 1 - Don't over-engineer!
