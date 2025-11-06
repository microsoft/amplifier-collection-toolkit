"""Library interface for programmatic tutorial analysis.

This is a STUD (interface):
- Thin wrapper around pipeline.py for discoverability
- Caller handles state storage (Redis, PostgreSQL, memory, whatever)
- Caller handles I/O (WebSocket, SSE, polling, whatever)
- Caller handles approval flow (web UI, API, auto-approve, whatever)

Philosophy:
- Ruthless simplicity: No abstractions, just thin wrapper
- Present-moment focus: Solves immediate need (web integration)
- Modular design: Clear interface, caller controls policy

Usage Example (FastAPI + WebSocket + Redis):

    from tutorial_analyzer.library import analyze_tutorial
    import redis, json

    @app.websocket("/analyze/{session_id}")
    async def analyze_endpoint(websocket: WebSocket, session_id: str):
        redis_client = redis.Redis()

        # Your app handles storage
        state = json.loads(redis_client.get(f"session:{session_id}") or "{}")

        # Your app handles WebSocket
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
"""

from collections.abc import Awaitable
from collections.abc import Callable

from .pipeline import run_analysis_pipeline


def _generate_report_markdown(state: dict, tutorial_identifier: str = "tutorial") -> str:
    """Generate markdown analysis report as string.

    Args:
        state: Complete analysis state
        tutorial_identifier: Name/ID for the tutorial (used in report header)

    Returns:
        Markdown report as string
    """
    lines = []
    lines.append("# Tutorial Analysis Report\n")
    lines.append(f"**Tutorial:** `{tutorial_identifier}`\n")
    lines.append(f"**Quality Score:** {state.get('synthesis', {}).get('quality_score', 'N/A')}\n")
    lines.append("\n---\n\n")

    # Diagnosis Summary
    if "diagnosis" in state:
        lines.append("## Diagnosis Summary\n\n")
        diagnosis = state["diagnosis"]
        if "summary" in diagnosis:
            summary = diagnosis["summary"]
            lines.append(f"**Primary Issue:** {summary.get('primary_pedagogical_failure', 'N/A')}\n\n")
            lines.append(
                f"**Issues Found:** {summary.get('critical_issues', 0)} critical, "
                f"{summary.get('major_issues', 0)} major, {summary.get('minor_issues', 0)} minor\n\n"
            )

        # Detailed issues
        if "issues" in diagnosis and isinstance(diagnosis["issues"], list):
            lines.append("### Identified Issues\n\n")
            for issue in diagnosis["issues"]:
                if isinstance(issue, dict):
                    severity = issue.get("severity", "unknown").upper()
                    lines.append(f"- **[{severity}]** {issue.get('issue', 'Unknown issue')}\n")
            lines.append("\n")

    # Learner Experience
    if "learner_experience" in state:
        lines.append("## From Learner Perspective\n\n")
        exp = state["learner_experience"]
        if isinstance(exp, dict):
            if "issue" in exp:
                lines.append(f"**Confusion Point:** {exp['issue']}\n\n")
            if "location" in exp:
                lines.append(f"**Location:** {exp['location']}\n\n")
        lines.append("\n")

    # Improvements
    if "improvements" in state:
        lines.append("## Recommended Improvements\n\n")
        improvements_data = state["improvements"]

        # Handle single improvement object
        if "title" in improvements_data and "description" in improvements_data:
            suggestions = [improvements_data]
        else:
            suggestions = improvements_data.get("suggestions") or improvements_data.get("improvements", [])

        if isinstance(suggestions, list):
            for i, suggestion in enumerate(suggestions, 1):
                if isinstance(suggestion, dict):
                    lines.append(f"### {i}. {suggestion.get('title', 'Untitled')}\n\n")
                    lines.append(f"{suggestion.get('description', 'No description')}\n\n")
                    if "location" in suggestion:
                        lines.append(f"**Location:** {suggestion.get('location')}\n\n")
                else:
                    lines.append(f"### {i}. {suggestion}\n\n")

    # Implementation Priority
    if "synthesis" in state:
        lines.append("## Implementation Priority\n\n")
        synthesis = state["synthesis"]
        recommendations = synthesis.get("recommendations", [])
        if isinstance(recommendations, list):
            for i, rec in enumerate(recommendations, 1):
                lines.append(f"{i}. {rec}\n")
        lines.append("\n")

    lines.append("---\n\n")
    lines.append("*Generated by tutorial-analyzer using Multi-Config Metacognitive Recipe Pattern*\n")

    return "".join(lines)


async def analyze_tutorial(
    content: str,
    state: dict | None = None,
    on_save_state: Callable[[dict], None] | None = None,
    on_progress: Callable[[str], None] | None = None,
    on_request_approval: Callable[[dict], Awaitable[dict]] | None = None,
    focus_areas: list[str] | None = None,
    tutorial_identifier: str = "tutorial",
) -> dict:
    """Analyze tutorial and generate improvement recommendations.

    Library interface for web applications. Caller handles all I/O via callbacks.

    Args:
        content: Tutorial markdown content
        state: Resume from previous state (default: empty dict for fresh run)
        on_save_state: State persistence callback (default: no-op)
        on_progress: Progress update callback (default: no-op)
        on_request_approval: Approval request callback (default: auto-approve)
        focus_areas: Optional areas to focus on (e.g., ["clarity", "examples"])
        tutorial_identifier: Name/ID for tutorial (used in report)

    Returns:
        Dict with:
            - report_markdown: Full analysis report as string
            - quality_score: Overall quality (0.0-1.0)
            - structured_data: Complete state (diagnosis, improvements, synthesis, etc.)
            - status: "complete" or "rejected"

    Example (web integration with WebSocket + Redis):

        result = await analyze_tutorial(
            content=uploaded_text,
            state=json.loads(redis.get(session_id) or "{}"),
            on_save_state=lambda s: redis.set(session_id, json.dumps(s)),
            on_progress=lambda m: websocket.send_json({"msg": m}),
            on_request_approval=get_user_approval_via_websocket,
            focus_areas=["clarity", "examples"]
        )

        if result["status"] == "complete":
            await websocket.send_json({
                "type": "complete",
                "report": result["report_markdown"],
                "score": result["quality_score"]
            })
    """

    # Defaults
    if state is None:
        state = {}

    # Add focus_areas to state if provided
    if focus_areas:
        state["focus_areas"] = focus_areas

    # Create save callback - no-op if not provided
    def save_callback(s: dict) -> None:
        if on_save_state is not None:
            on_save_state(s)
        # Else: no-op (caller doesn't need checkpointing)

    # Run pipeline
    result_state = await run_analysis_pipeline(
        content=content,
        state=state,
        on_save_state=save_callback,
        on_progress=on_progress,
        on_request_approval=on_request_approval,
    )

    # Check if rejected
    if result_state.get("status") == "rejected":
        return {
            "status": "rejected",
            "reason": result_state.get("reason", "Unknown"),
            "report_markdown": "",
            "quality_score": 0.0,
            "structured_data": result_state,
        }

    # Success - package results
    return {
        "status": "complete",
        "report_markdown": _generate_report_markdown(result_state, tutorial_identifier),
        "quality_score": float(result_state["synthesis"].get("quality_score", 0.0)),
        "structured_data": result_state,
    }
