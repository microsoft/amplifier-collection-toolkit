---
name: toolkit-dev
description: Profile optimized for developing scenario tools with metacognitive recipes
extends: foundation
---

# Toolkit Development Profile

Optimized for building sophisticated CLI tools using metacognitive recipes.

## Configuration

This profile extends `foundation` with toolkit-specific optimizations:

### Session Configuration

```yaml
session:
  orchestrator: loop-streaming   # Real-time feedback during development
  context: context-simple        # Lightweight for rapid iteration
```

### Provider Overrides

```yaml
providers:
  - module: provider-anthropic
    source: git+https://github.com/microsoft/amplifier-module-provider-anthropic@main
    config:
      default_model: claude-sonnet-4-5  # Fast, cost-effective for development
      temperature: 0.3                   # Analytical default (adjust per stage)
      max_tokens: 4096
```

### Additional Tools

```yaml
tools:
  - module: tool-filesystem
    source: git+https://github.com/microsoft/amplifier-module-tool-filesystem@main
    config:
      allowed_paths:
        - .
        - ./scenario-tools
        - ./tests

  - module: tool-bash
    source: git+https://github.com/microsoft/amplifier-module-tool-bash@main
    config:
      allowed_commands:
        - pytest
        - uv
        - python
```

### Hooks

```yaml
hooks:
  - module: hooks-logging
    source: git+https://github.com/microsoft/amplifier-module-hooks-logging@main
    config:
      log_file: .toolkit_dev.log
      log_level: DEBUG
```

## Use Cases

Perfect for:
- Building new scenario tools
- Testing multi-config patterns
- Debugging tool orchestration
- Rapid prototyping
- Learning metacognitive recipes

## Usage

```bash
# Activate this profile
amplifier profile use toolkit-dev

# Run with this profile
amplifier run --mode chat

# Build a tool
amplifier run "Help me build a document analyzer using the toolkit pattern"
```

## Philosophy

This profile embodies toolkit principles:
- Fast iteration (streaming, simple context)
- Development-friendly (debug logging, filesystem/bash tools)
- Cost-effective (Sonnet model)
- Practical (sensible defaults)

## Related

- **Collection**: amplifier-collection-toolkit
- **Utilities**: `from amplifier_collection_toolkit import ...`
- **Examples**: scenario-tools/tutorial-analyzer/
- **Docs**: docs/TOOLKIT_GUIDE.md
