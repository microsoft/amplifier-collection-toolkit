# Tutorial Analyzer

Analyze tutorials and generate improvement recommendations through multi-stage metacognitive analysis.

Available as **CLI tool** for command-line use or **library** for integration into web applications.

## What It Does

Analyzes tutorials from a learner's perspective and generates a detailed improvement report:

1. **Analyzes** tutorial structure and content
2. **Simulates** learner experiencing the tutorial
3. **Diagnoses** pedagogical issues from learner perspective
4. **Generates** specific, actionable improvement recommendations
5. **Evaluates** recommendation quality
6. **Synthesizes** prioritized action plan
7. **Creates** markdown analysis report

## Installation

### CLI Tool

Via uvx (no install needed):
```bash
uvx tutorial-analyzer tutorial.md
```

Via uv tool (persistent):
```bash
uv tool install tutorial-analyzer
tutorial-analyzer tutorial.md
```

From local wheel:
```bash
uvx --from ./tutorial_analyzer-0.1.0-py3-none-any.whl tutorial-analyzer tutorial.md
```

### Library (for web apps)

```bash
pip install tutorial-analyzer
```

## Usage

### CLI Usage

Basic:
```bash
tutorial-analyzer tutorial.md
```

With focus areas:
```bash
tutorial-analyzer tutorial.md clarity engagement code-examples
```

**Output:** Creates `tutorial_name_analysis.md` with:
- Recommended improvements (prioritized)
- Implementation guidance
- Quality assessment

### Library Usage

Use the library to integrate tutorial analysis into web applications:

```python
from tutorial_analyzer.library import analyze_tutorial

# Analyze with default in-memory state
result = await analyze_tutorial(
    content=tutorial_text,
    on_progress=lambda msg: print(msg),
)

# With custom state storage (e.g., Redis)
result = await analyze_tutorial(
    content=tutorial_text,
    state=existing_state,
    on_save_state=lambda s: redis.set(session_id, json.dumps(s)),
    on_progress=lambda m: websocket.send_json({"msg": m}),
    on_request_approval=get_approval_via_websocket,
)
```

**Web Integration Example (FastAPI + WebSocket)**:

```python
from fastapi import FastAPI, WebSocket
from tutorial_analyzer.library import analyze_tutorial
import redis, json

app = FastAPI()

@app.websocket("/analyze/{session_id}")
async def analyze_endpoint(websocket: WebSocket, session_id: str):
    await websocket.accept()
    data = await websocket.receive_json()

    # Your app handles storage
    redis_client = redis.Redis()
    state = json.loads(redis_client.get(f"session:{session_id}") or "{}")

    # Your app handles WebSocket communication
    async def progress(msg):
        await websocket.send_json({"type": "progress", "msg": msg})

    async def approval(context):
        await websocket.send_json({"type": "approval", "context": context})
        return await websocket.receive_json()

    # Run analysis with your callbacks
    result = await analyze_tutorial(
        content=data["content"],
        state=state,
        on_save_state=lambda s: redis_client.set(f"session:{session_id}", json.dumps(s)),
        on_progress=progress,
        on_request_approval=approval
    )

    await websocket.send_json({"type": "complete", "result": result})
```

**Library API**:

```python
async def analyze_tutorial(
    content: str,                                          # Tutorial markdown content
    state: Optional[dict] = None,                          # Resume from previous state
    on_save_state: Optional[Callable[[dict], None]] = None,  # State persistence
    on_progress: Optional[Callable[[str], None]] = None,   # Progress updates
    on_request_approval: Optional[Callable[[dict], dict]] = None,  # Human-in-loop
) -> dict:
    """
    Analyze tutorial and generate improvement recommendations.

    Returns dict with:
        - report_markdown: Full analysis report
        - quality_score: Overall quality (0.0-1.0)
        - structured_data: Diagnosis, improvements, synthesis
    """
```

## How It Works

### Multi-Config Metacognitive Recipe

Uses 6 specialized configs, each optimized for its cognitive role:

1. **Analyzer** (analytical, temp=0.3) - Extract tutorial structure
2. **Learner Simulator** (empathetic, temp=0.5) - Simulate learner experience
3. **Diagnostician** (precise, temp=0.1) - Identify pedagogical issues
4. **Improver** (creative, temp=0.7) - Generate improvement suggestions
5. **Critic** (evaluative, temp=0.2) - Evaluate improvement quality
6. **Synthesizer** (analytical, temp=0.3) - Create final recommendations

### Pipeline

```
Analyze → Simulate Learner → Diagnose Issues →
→ Generate Improvements → [HUMAN APPROVAL] →
→ Evaluate Improvements → Synthesize Recommendations →
→ [QUALITY CHECK] → Loop or Finalize
```

### Philosophy

- **Code for structure, AI for intelligence**: Code orchestrates, specialized configs think
- **Multiple configs, not one**: Each cognitive task gets optimized setup
- **Human-in-loop**: Strategic approval after improvement generation
- **Quality loops**: Iterate until threshold met
- **Checkpointing**: Resumable if interrupted

## Development

Install for development:
```bash
cd amplifier-app-cli/toolkit/examples/tutorial_analyzer
uv sync --all-extras
```

Run tests:
```bash
uv run pytest
```

Build:
```bash
uv build
```

Test locally:
```bash
uvx ./dist/tutorial_analyzer-*.whl tests/fixtures/sample_tutorial.md
```

## Architecture

The tutorial analyzer follows a clean separation between domain logic and interfaces:

**Core Pipeline** (reusable):
- `src/tutorial_analyzer/pipeline.py` - Pure domain logic, no I/O assumptions

**Interfaces**:
- `src/tutorial_analyzer/cli.py` - CLI wrapper (console I/O, local file state)
- `src/tutorial_analyzer/library.py` - Library interface (programmatic access)

**Analysis Stages** (6 specialized configs):
- `src/tutorial_analyzer/analyzer/` - Stage 1: Content analysis
- `src/tutorial_analyzer/learner_simulator/` - Stage 2: Learner simulation
- `src/tutorial_analyzer/diagnostician/` - Stage 3: Issue diagnosis
- `src/tutorial_analyzer/improver/` - Stage 4: Improvement generation
- `src/tutorial_analyzer/critic/` - Stage 5: Quality evaluation
- `src/tutorial_analyzer/synthesizer/` - Stage 6: Final recommendations

**Philosophy**:
- **Brick**: `pipeline.py` contains pure domain logic
- **Studs**: `cli.py` and `library.py` provide stable interfaces
- **Regeneratable**: Any part can be regenerated from specification

Each stage is self-contained with its own specialized config.

## License

MIT
