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

ui:
  show_thinking_stream: true
  show_tool_lines: 5

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
  - module: hooks-streaming-ui
    source: git+https://github.com/microsoft/amplifier-module-hooks-streaming-ui@main
  - module: hooks-logging
    source: git+https://github.com/microsoft/amplifier-module-hooks-logging@main
    config:
      log_file: .toolkit_dev.log
      log_level: DEBUG

agents:
  dirs:
    - ./agents
---

@foundation:context/shared/common-agent-base.md
