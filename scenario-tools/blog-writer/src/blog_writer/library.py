"""Library interface for programmatic blog writing.

This is a STUD (interface):
- Thin wrapper around pipeline.py for backward compatibility
- For new code, use run_blog_writing_pipeline() directly with StateManager
- This interface maintains backward compatibility with dict-based state

Philosophy:
- Ruthless simplicity: No abstractions, just thin wrapper
- Present-moment focus: Maintains compatibility while encouraging StateManager use
- Modular design: Clear interface, caller controls policy

Note: This is a compatibility layer. For new code, use:
    from blog_writer.state import StateManager
    from blog_writer.pipeline import run_blog_writing_pipeline

    state_manager = StateManager(session_dir)
    result = await run_blog_writing_pipeline(..., state_manager=state_manager)
"""

from collections.abc import Callable
from pathlib import Path
from tempfile import mkdtemp

from .pipeline import run_blog_writing_pipeline
from .state import StateManager


async def write_blog_post(
    source_content: str,
    style_samples: list[dict],
    user_feedback: str | None = None,
    state: dict | None = None,
    on_save_state: Callable[[dict], None] | None = None,
    on_progress: Callable[[str], None] | None = None,
) -> dict:
    """Write blog post from brain dump matching writing style.

    DEPRECATED: This is a compatibility wrapper. For new code, use StateManager directly.

    Args:
        source_content: Source material (brain dump/notes)
        style_samples: List of dicts with {"file": name, "content": text}
        user_feedback: Optional draft with [bracket comments] for revision
        state: IGNORED - maintained for compatibility
        on_save_state: IGNORED - maintained for compatibility
        on_progress: Progress update callback (default: no-op)

    Returns:
        Dict with:
            - draft: Final blog post draft
            - quality_metrics: Dict with review counts and iterations
            - state: Complete state dict (for compatibility)
    """

    # Create temporary session directory
    temp_dir = Path(mkdtemp(prefix="blog_writer_"))
    state_manager = StateManager(temp_dir)

    # Run pipeline with StateManager
    result = await run_blog_writing_pipeline(
        source_content=source_content,
        style_samples=style_samples,
        user_feedback=user_feedback,
        state_manager=state_manager,
        on_progress=on_progress,
    )

    # Package results for backward compatibility
    return {
        "draft": result["draft"],
        "quality_metrics": result["quality_metrics"],
        "state": {
            "style_profile": state_manager.state.style_profile,
            "draft": result["draft"],
            "source_reviews_completed": result["quality_metrics"]["source_reviews_completed"],
            "style_reviews_completed": result["quality_metrics"]["style_reviews_completed"],
        },
    }
