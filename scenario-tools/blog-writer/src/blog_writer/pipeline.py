"""Pure domain logic for blog writing pipeline.

This is the BRICK:
- Self-contained multi-stage metacognitive recipe
- No I/O assumptions (caller handles via callbacks)
- Works with ANY storage (file, Redis, memory, PostgreSQL)
- Works with ANY UI (CLI, web, mobile)
- Regeneratable from this specification

Contract (Stud):
- Input: source_content (str), style_samples (list[dict]), user_feedback (str | None), state_manager (StateManager), callbacks
- Output: Complete state dict with {style_profile, draft, reviews, final_draft}
- Callbacks: on_progress

Philosophy:
- Ruthless simplicity: Simple callbacks, no abstractions
- Modular design: Clear interface, internal complexity isolated
- Present-moment focus: Solves current need without hypothetical futures
"""

from collections.abc import Callable
from typing import TYPE_CHECKING

from .draft_writer.core import generate_draft
from .feedback_incorporator.core import interpret_feedback
from .source_reviewer.core import review_source_accuracy
from .style_analyzer.core import analyze_style
from .style_reviewer.core import review_style_consistency

if TYPE_CHECKING:
    from .state import StateManager


async def run_blog_writing_pipeline(
    source_content: str,
    style_samples: list[dict],
    user_feedback: str | None,
    state_manager: "StateManager",
    on_progress: Callable[[str], None] | None = None,
) -> dict:
    """Run multi-stage blog writing pipeline with rich state tracking.

    This is the core domain logic - uses StateManager for comprehensive tracking.

    Args:
        source_content: Source material (brain dump/notes)
        style_samples: List of dicts with {"file": name, "content": text}
        user_feedback: Optional draft with [bracket comments] for revision
        state_manager: StateManager instance for rich state tracking
        on_progress: Optional callback for progress updates (message: str)

    Returns:
        Complete state dict with all pipeline results:
            - style_profile: Stage 1 output
            - draft: Stage 2 output
            - source_reviews_completed: Number of source review iterations
            - style_reviews_completed: Number of style review iterations
            - final_draft: Final polished draft

    Pipeline:
        Style Analysis (cached) → Draft Generation →
        → Source Accuracy Review (loop) → Style Consistency Review (loop) →
        → Finalize or Incorporate Feedback
    """

    state = state_manager.state

    # Stage 1: Style analysis (cached - only run once)
    if not state.style_profile:
        state_manager.update_stage("style_analysis")
        if on_progress:
            on_progress("Analyzing writing style...")

        state.style_profile = await analyze_style(style_samples)
        state_manager.add_iteration_history({"type": "style_analysis", "samples_analyzed": len(style_samples)})

        if on_progress:
            on_progress("✓ Style analysis complete")

    # Check if we're incorporating user feedback
    if user_feedback:
        state_manager.update_stage("feedback_incorporation")
        if on_progress:
            on_progress("Interpreting user feedback...")

        # Stage 5: Interpret feedback
        feedback_interpretation = await interpret_feedback(user_feedback, source_content, state.style_profile)

        # Create revision guidance from feedback
        revision_guidance = f"""User provided {len(feedback_interpretation["feedback_items"])} feedback items:

{feedback_interpretation["overall_guidance"]}

Specific items to address:
"""
        for item in feedback_interpretation["feedback_items"]:
            revision_guidance += f"\n- {item['interpretation']}: {item['action']}"

        # Generate revised draft
        if on_progress:
            on_progress("Generating revised draft...")
        state.current_draft = await generate_draft(source_content, state.style_profile, revision_guidance)
        state_manager.increment_iteration()
        state_manager.update_draft(state.current_draft)

        # Reset review counters to ensure both reviews run again
        state.source_reviews_completed = 0
        state.style_reviews_completed = 0

        if on_progress:
            on_progress("✓ Revised draft generated")

    elif not state.current_draft:
        # Generate initial draft
        state_manager.update_stage("draft_generation")
        if on_progress:
            on_progress("Generating initial draft...")

        state.current_draft = await generate_draft(source_content, state.style_profile)
        state_manager.increment_iteration()
        state_manager.update_draft(state.current_draft)

        if on_progress:
            on_progress("✓ Draft generated")

    # Stage 3: Source accuracy review loop
    state_manager.update_stage("source_review")
    max_source_reviews = 3

    while state.source_reviews_completed < max_source_reviews:
        if on_progress:
            on_progress(
                f"Reviewing source accuracy (attempt {state.source_reviews_completed + 1}/{max_source_reviews})..."
            )

        source_review = await review_source_accuracy(source_content, state.current_draft)
        state_manager.add_source_review(source_review)

        if source_review["passed"] or source_review["severity"] in ["none", "minor"]:
            if on_progress:
                on_progress("✓ Source accuracy verified")
            break

        # Generate revision guidance
        revision_guidance = f"""The source accuracy review found issues:

Severity: {source_review["severity"]}

Issues:
"""
        for issue in source_review["issues"]:
            revision_guidance += f"\n- {issue}"

        if source_review.get("missing_concepts"):
            revision_guidance += "\n\nMissing concepts from source:"
            for concept in source_review["missing_concepts"]:
                revision_guidance += f"\n- {concept}"

        if source_review.get("incorrect_representations"):
            revision_guidance += "\n\nIncorrect representations:"
            for incorrect in source_review["incorrect_representations"]:
                revision_guidance += f"\n- {incorrect}"

        # Revise draft with sub-version tracking
        if on_progress:
            on_progress(
                f"Revising draft (source accuracy, attempt {state.source_reviews_completed}/{max_source_reviews})"
            )
        state.current_draft = await generate_draft(source_content, state.style_profile, revision_guidance)
        sub_version = f"source_rev_{state.source_reviews_completed + 1}"
        state_manager.update_draft(state.current_draft, sub_version=sub_version)

    # Stage 4: Style consistency review loop
    state_manager.update_stage("style_review")
    max_style_reviews = 3

    while state.style_reviews_completed < max_style_reviews:
        if on_progress:
            on_progress(
                f"Reviewing style consistency (attempt {state.style_reviews_completed + 1}/{max_style_reviews})..."
            )

        style_review = await review_style_consistency(state.style_profile, style_samples, state.current_draft)
        state_manager.add_style_review(style_review)

        if style_review["passed"] or style_review["severity"] in ["none", "minor"]:
            if on_progress:
                on_progress("✓ Style consistency verified")
            break

        # Generate revision guidance
        revision_guidance = f"""The style consistency review found issues:

Severity: {style_review["severity"]}

Issues:
"""
        for issue in style_review["issues"]:
            revision_guidance += f"\n- {issue}"

        if style_review.get("voice_issues"):
            revision_guidance += "\n\nVoice issues:"
            for issue in style_review["voice_issues"]:
                revision_guidance += f"\n- {issue}"

        if style_review.get("tone_issues"):
            revision_guidance += "\n\nTone issues:"
            for issue in style_review["tone_issues"]:
                revision_guidance += f"\n- {issue}"

        # Revise draft with sub-version tracking
        if on_progress:
            on_progress(
                f"Revising draft (style consistency, attempt {state.style_reviews_completed}/{max_style_reviews})"
            )
        state.current_draft = await generate_draft(source_content, state.style_profile, revision_guidance)
        sub_version = f"style_rev_{state.style_reviews_completed + 1}"
        state_manager.update_draft(state.current_draft, sub_version=sub_version)

    # Mark completion
    state_manager.update_stage("completed")

    # Return dict for backward compatibility
    return {
        "draft": state.current_draft,
        "style_profile": state.style_profile,
        "quality_metrics": {
            "source_reviews_completed": state.source_reviews_completed,
            "style_reviews_completed": state.style_reviews_completed,
        },
        "final_draft": state.current_draft,
    }
