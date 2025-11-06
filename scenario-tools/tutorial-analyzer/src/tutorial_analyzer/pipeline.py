"""Pure domain logic for tutorial analysis pipeline.

This is the BRICK:
- Self-contained multi-stage metacognitive recipe
- No I/O assumptions (caller handles via callbacks)
- Works with ANY storage (file, Redis, memory, PostgreSQL)
- Works with ANY UI (CLI, web, mobile)
- Regeneratable from this specification

Contract (Stud):
- Input: content (str), state (dict), callbacks
- Output: Complete state dict with all analysis results
- Callbacks: on_save_state, on_progress, on_request_approval

Philosophy:
- Ruthless simplicity: Simple callbacks, no abstractions
- Modular design: Clear interface, internal complexity isolated
- Present-moment focus: Solves current need without hypothetical futures
"""

from collections.abc import Awaitable
from collections.abc import Callable

from .analyzer.core import analyze
from .critic.core import evaluate_improvements
from .diagnostician.core import diagnose_issues
from .improver.core import generate_improvements
from .learner_simulator.core import simulate_learner
from .synthesizer.core import synthesize_recommendations


async def run_analysis_pipeline(
    content: str,
    state: dict,
    on_save_state: Callable[[dict], None],
    on_progress: Callable[[str], None] | None = None,
    on_request_approval: Callable[[dict], Awaitable[dict]] | None = None,
) -> dict:
    """Run multi-stage tutorial analysis pipeline.

    This is the core domain logic - pure function with no I/O side effects.
    All I/O happens via callbacks provided by caller.

    Args:
        content: Tutorial markdown content
        state: Current state (empty dict for fresh run, previous state to resume)
        on_save_state: Called after each stage with updated state (for checkpointing)
        on_progress: Optional callback for progress updates (message: str)
        on_request_approval: Optional callback for human approval requests
                           (context: dict) -> dict with {decision: str, modifications?: str}
                           If not provided, improvements auto-approved

    Returns:
        Complete state dict with all analysis results:
            - analysis: Stage 1 output
            - learner_experience: Stage 2 output
            - diagnosis: Stage 3 output
            - improvements: Stage 4 output
            - human_approval: Approval decision
            - critique: Stage 5 output
            - synthesis: Stage 6 output
            - quality_score: Final quality score
            - iterations: Number of quality improvement loops

    Pipeline:
        Analyze → Simulate Learner → Diagnose Issues →
        → Generate Improvements → [HUMAN APPROVAL] →
        → Evaluate Improvements → Synthesize Recommendations →
        → [QUALITY CHECK] → Loop or Finalize
    """

    # Stage 1: Content analysis (autonomous)
    if "analysis" not in state:
        if on_progress:
            on_progress("Stage 1/7: Analyzing tutorial structure...")
        state["analysis"] = await analyze(content)
        on_save_state(state)
        if on_progress:
            on_progress("✓ Analysis complete")

    # Stage 2: Learner simulation (autonomous)
    if "learner_experience" not in state:
        if on_progress:
            on_progress("Stage 2/7: Simulating learner experience...")
        state["learner_experience"] = await simulate_learner(content, state["analysis"])
        on_save_state(state)
        if on_progress:
            on_progress("✓ Simulation complete")

    # Stage 3: Issue diagnosis (autonomous)
    if "diagnosis" not in state:
        if on_progress:
            on_progress("Stage 3/7: Diagnosing pedagogical issues...")
        state["diagnosis"] = await diagnose_issues(state["learner_experience"], state["analysis"])
        on_save_state(state)
        if on_progress:
            on_progress("✓ Diagnosis complete")

    # Stage 4: Improvement generation (autonomous)
    if "improvements" not in state:
        if on_progress:
            on_progress("Stage 4/7: Generating improvement suggestions...")
        # Extract focus_areas from state if present (set by caller)
        focus_areas = state.get("focus_areas")
        state["improvements"] = await generate_improvements(state["diagnosis"], focus_areas)
        on_save_state(state)
        if on_progress:
            on_progress("✓ Improvements generated")

    # Stage 5: HUMAN-IN-LOOP (strategic decision point)
    if "human_approval" not in state:
        if on_request_approval:
            # Request approval from caller
            approval_response = await on_request_approval(
                {"improvements": state["improvements"], "diagnosis": state["diagnosis"]}
            )

            state["human_approval"] = approval_response.get("decision", "yes")
            if approval_response.get("modifications"):
                state["improvements"]["modifications"] = approval_response["modifications"]

            on_save_state(state)

            # If rejected, return early
            if state["human_approval"] == "no":
                return {"status": "rejected", "reason": "User rejected improvements"}
        else:
            # No approval callback - auto-approve
            state["human_approval"] = "yes"
            on_save_state(state)

    # Stage 6: Evaluate improvements (autonomous)
    if "critique" not in state:
        if on_progress:
            on_progress("Stage 5/7: Evaluating improvement quality...")
        state["critique"] = await evaluate_improvements(state["improvements"], state["diagnosis"])
        on_save_state(state)
        if on_progress:
            on_progress("✓ Evaluation complete")

    # Stage 7: Synthesize final recommendations (autonomous)
    if "synthesis" not in state:
        if on_progress:
            on_progress("Stage 6/7: Synthesizing final recommendations...")
        state["synthesis"] = await synthesize_recommendations(
            state["critique"], state["improvements"], state["diagnosis"]
        )
        on_save_state(state)
        if on_progress:
            on_progress("✓ Synthesis complete")

    # QUALITY CHECK: Decide whether to iterate
    quality_score = float(state["synthesis"].get("quality_score", 0))
    iterations = state.get("iterations", 0)

    if on_progress:
        on_progress(f"Quality Score: {quality_score}")

    if quality_score < 0.8 and iterations < 3:
        if on_progress:
            on_progress(f"Score below threshold. Iterating... (attempt {iterations + 1}/3)")

        state["iterations"] = iterations + 1

        # Clear stages that need regeneration
        del state["improvements"]  # Regenerate with feedback
        del state["human_approval"]  # Ask again
        del state["critique"]  # Re-evaluate new improvements
        del state["synthesis"]  # Re-synthesize with new evaluation

        on_save_state(state)

        # Recurse for another iteration
        return await run_analysis_pipeline(content, state, on_save_state, on_progress, on_request_approval)

    # Success - return final state
    return state
