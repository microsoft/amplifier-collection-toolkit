# Scenario Tool Templates

Templates for building your own scenario tools using the metacognitive recipe pattern.

## Available Templates

### standalone_tool.py

Basic template showing the multi-config pattern structure.

**What it includes**:
- Multiple specialized config definitions
- Orchestration logic structure
- Checkpointing pattern
- Progress reporting
- Input validation

**How to use**:
1. Copy template to your project
2. Rename configs for your cognitive stages
3. Adjust temperatures for each role
4. Implement your orchestration logic
5. Add your specific prompts

**Example**:
```bash
cp templates/standalone_tool.py my_analyzer.py
# Edit to customize for your use case
```

## Learning Path

1. **Study the exemplar**: Read `scenario-tools/tutorial-analyzer/` to see complete implementation
2. **Read the guides**: Check `docs/HOW_TO_CREATE_YOUR_OWN.md` for step-by-step instructions
3. **Copy template**: Use `standalone_tool.py` as starting point
4. **Customize**: Adapt to your specific use case
5. **Test**: Verify with real inputs
6. **Package**: Follow `docs/PACKAGING_GUIDE.md` for distribution

## Key Pattern Elements

Every scenario tool should include:

- **Multiple configs**: One per cognitive role (analytical, creative, evaluative, etc.)
- **Orchestration code**: Decides which config when
- **State management**: Checkpointing for resumability
- **Input validation**: Fail fast with clear errors
- **Progress reporting**: Keep user informed
- **Documentation**: README + HOW_TO_BUILD

## Temperature Guide

Choose temperature based on cognitive role:

- **Analytical** (0.1-0.3): Structure extraction, classification, diagnosis
- **Empathetic** (0.4-0.6): User simulation, perspective-taking
- **Creative** (0.6-0.8): Content generation, ideation
- **Evaluative** (0.1-0.3): Quality scoring, critique
- **Synthesizing** (0.3-0.5): Combining information, summarization

## Related Documentation

- **[../docs/SCENARIO_TOOLS_GUIDE.md](../docs/SCENARIO_TOOLS_GUIDE.md)** - Complete guide to building scenario tools
- **[../docs/HOW_TO_CREATE_YOUR_OWN.md](../docs/HOW_TO_CREATE_YOUR_OWN.md)** - Step-by-step creation guide
- **[../docs/METACOGNITIVE_RECIPES.md](../docs/METACOGNITIVE_RECIPES.md)** - Pattern library
- **[../docs/BEST_PRACTICES.md](../docs/BEST_PRACTICES.md)** - Proven patterns
