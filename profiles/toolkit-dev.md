---
profile:
  name: toolkit-dev
  version: 1.0.0
  description: Toolkit development configuration with metacognitive recipe helpers
  extends: foundation

session:
  orchestrator:
    module: loop-streaming
    source: git+https://github.com/microsoft/amplifier-module-loop-streaming@main
    config:
      extended_thinking: true
  context:
    module: context-simple

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
  - module: tool-task
    source: git+https://github.com/microsoft/amplifier-module-tool-task@main

hooks:
  - module: hooks-logging
    source: git+https://github.com/microsoft/amplifier-module-hooks-logging@main
    config:
      log_file: .toolkit_dev.log
      log_level: DEBUG

agents:
  dirs:
    - ./agents
---

# Toolkit Development Profile

Optimized for building sophisticated CLI tools using metacognitive recipes.

Use this profile when you want fast iteration with streaming feedback, direct filesystem access, and tooling tuned for multi-config recipe development.

## Usage

```bash
# Activate this profile
amplifier profile use toolkit-dev

# Run with this profile
amplifier run --mode chat

# Build a tool
amplifier run "Help me build a document analyzer using the toolkit pattern"
```

## Included Capabilities

- Streaming orchestration with lightweight context for rapid iteration
- Filesystem + bash tooling constrained to the project workspace
- Task delegation via the Toolkit `tool-builder` agent
- Debug logging configured for development loops

## Related

- **Collection**: toolkit
- **Utilities**: `from amplifier_collection_toolkit import ...`
- **Examples**: scenario-tools/tutorial-analyzer/
- **Docs**: docs/TOOLKIT_GUIDE.md
