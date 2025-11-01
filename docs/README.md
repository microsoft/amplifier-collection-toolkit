# Amplifier Collection Toolkit Documentation

Complete guides for building sophisticated CLI tools using metacognitive recipes.

---

## Quick Navigation

### Getting Started
- **[TOOLKIT_GUIDE.md](TOOLKIT_GUIDE.md)** - Comprehensive reference and overview
- **[SCENARIO_TOOLS_GUIDE.md](SCENARIO_TOOLS_GUIDE.md)** - How to build scenario tools

### Philosophy & Principles
- **[PHILOSOPHY.md](PHILOSOPHY.md)** - Design philosophy and core principles
- **[BEST_PRACTICES.md](BEST_PRACTICES.md)** - Proven patterns and conventions

### Building Tools
- **[HOW_TO_CREATE_YOUR_OWN.md](HOW_TO_CREATE_YOUR_OWN.md)** - Step-by-step creation guide
- **[METACOGNITIVE_RECIPES.md](METACOGNITIVE_RECIPES.md)** - Pattern library and advanced techniques
- **[PACKAGING_GUIDE.md](PACKAGING_GUIDE.md)** - Distribution and installation

---

## What Are Metacognitive Recipes?

**Metacognitive recipes** are thinking processes encoded as code that orchestrate multiple specialized AI sessions:

```
Analyze (precise) → Simulate (empathetic) → Diagnose (critical) →
→ Plan (strategic) [HUMAN APPROVAL] → Implement (creative) →
→ Evaluate (judgmental) → LOOP or FINISH
```

**Key Principle**: Code for structure, AI for intelligence.

---

## Documentation Organization

### For Users (Using the Toolkit)
1. Start with **TOOLKIT_GUIDE.md** - Overview and utilities reference
2. Read **SCENARIO_TOOLS_GUIDE.md** - Understanding scenario tools
3. Study **../scenario-tools/tutorial-analyzer/** - Complete example

### For Builders (Creating Tools)
1. Read **PHILOSOPHY.md** - Understand core principles
2. Follow **HOW_TO_CREATE_YOUR_OWN.md** - Step-by-step guide
3. Study **METACOGNITIVE_RECIPES.md** - Pattern library
4. Apply **BEST_PRACTICES.md** - Quality guidelines
5. Use **PACKAGING_GUIDE.md** - Distribution

---

## Learning Path

**Beginner**: New to scenario tools
→ SCENARIO_TOOLS_GUIDE.md → tutorial-analyzer example → templates/standalone_tool.py

**Intermediate**: Ready to build
→ HOW_TO_CREATE_YOUR_OWN.md → BEST_PRACTICES.md → Build your tool

**Advanced**: Complex patterns
→ METACOGNITIVE_RECIPES.md → PHILOSOPHY.md → Advanced implementations

---

## Quick Reference

### Utilities (`amplifier_collection_toolkit`)

```python
from amplifier_collection_toolkit import (
    discover_files,          # Recursive file discovery
    ProgressReporter,        # Progress display
    validate_input_path,     # Path validation
    read_json, write_json,   # JSON I/O
)
```

### Temperature Guide

| Role | Temperature | Use For |
|------|-------------|---------|
| Analytical | 0.1-0.3 | Structure extraction, classification |
| Empathetic | 0.4-0.6 | User simulation, perspective-taking |
| Creative | 0.6-0.8 | Content generation, ideation |
| Evaluative | 0.1-0.3 | Quality scoring, critique |
| Synthesizing | 0.3-0.5 | Combining information, summarization |

### Config Pattern

```python
from amplifier_core import AmplifierSession

CONFIG = {
    "session": {"orchestrator": "loop-basic"},
    "providers": [{
        "module": "provider-anthropic",
        "source": "git+https://github.com/...",
        "config": {
            "temperature": 0.3,  # Choose based on role
            "system_prompt": "..."
        }
    }]
}

# Use directly
async with AmplifierSession(config=CONFIG) as session:
    result = await session.execute(prompt)
```

---

## Examples in This Collection

**Tutorial Analyzer** (`../scenario-tools/tutorial-analyzer/`)
- 6 specialized configs
- Multi-stage pipeline
- Quality loops
- Human approval gates
- Complete pedagogical exemplar

**See also**: `../templates/standalone_tool.py` for basic template

---

## Philosophy Highlights

From **PHILOSOPHY.md**:

- **Multi-config patterns** (not single-config)
- **Structural utilities only** (no session wrappers)
- **Direct AmplifierSession usage**
- **Each tool owns its state**
- **Ruthless simplicity**

---

## Support

- **Issues**: [GitHub Issues](https://github.com/microsoft/amplifier-collection-toolkit/issues)
- **Discussions**: [GitHub Discussions](https://github.com/microsoft/amplifier-collection-toolkit/discussions)
- **Collection**: [amplifier-collection-toolkit](https://github.com/microsoft/amplifier-collection-toolkit)

---

**Ready to build? Start with [HOW_TO_CREATE_YOUR_OWN.md](HOW_TO_CREATE_YOUR_OWN.md)**
