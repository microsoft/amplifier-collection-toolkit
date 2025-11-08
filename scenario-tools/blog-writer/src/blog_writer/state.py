"""Rich state management for blog writer with complete session tracking.

Following the pattern from scenarios/blog_writer/state.py:
- Complete state structure with iteration history
- Session directory management
- Rich metadata and tracking
- Checkpoint after every significant operation

This enables:
- Resume from any point in the pipeline
- Full session visibility for debugging
- Context accumulation across iterations
- Historical tracking of all operations
"""

import json
from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from pathlib import Path
from typing import Any


@dataclass
class BlogWriterState:
    """Complete blog writer state for persistence.

    Tracks everything about a session:
    - Pipeline stage and iteration
    - Outputs from each stage (style, drafts, reviews)
    - Accumulated user feedback with full context
    - Complete iteration history for debugging
    - Metadata for session management
    """

    # Pipeline tracking
    stage: str = "initialized"
    iteration: int = 0
    max_iterations: int = 10

    # Stage outputs
    style_profile: str = ""  # From style_analyzer
    current_draft: str = ""  # Latest draft
    source_reviews: list[dict] = field(default_factory=list)  # ALL source review results
    style_reviews: list[dict] = field(default_factory=list)  # ALL style review results
    user_feedback: list[dict] = field(default_factory=list)  # ALL feedback with context

    # Review iteration counts
    source_reviews_completed: int = 0
    style_reviews_completed: int = 0

    # Iteration history - EVERY operation logged
    iteration_history: list[dict] = field(default_factory=list)

    # Metadata
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())

    # Input parameters (for resume)
    source_path: str | None = None
    style_dir_path: str | None = None
    output_path: str | None = None


class StateManager:
    """Manages rich state with session directory.

    Provides:
    - State persistence in session directory
    - Iteration history tracking
    - Draft versioning
    - User feedback accumulation
    """

    def __init__(self, session_dir: Path):
        """Initialize state manager with session directory.

        Args:
            session_dir: Directory for this session (typically .data/blog_writer_{timestamp})
        """
        self.session_dir = session_dir
        self.session_dir.mkdir(parents=True, exist_ok=True)
        self.state_file = self.session_dir / "state.json"
        self.state = self._load_or_create()

    def _load_or_create(self) -> BlogWriterState:
        """Load existing state or create new."""
        if self.state_file.exists():
            try:
                data = json.loads(self.state_file.read_text())
                return BlogWriterState(**data)
            except Exception:
                # If state is corrupted, create new
                return BlogWriterState()
        return BlogWriterState()

    def save(self) -> None:
        """Save current state with timestamp update."""
        self.state.updated_at = datetime.now().isoformat()
        self.state_file.write_text(json.dumps(asdict(self.state), indent=2))

    def add_iteration_history(self, entry: dict[str, Any]) -> None:
        """Add entry to iteration history for debugging.

        Args:
            entry: Dictionary with operation details (type, data, etc.)
        """
        entry["iteration"] = self.state.iteration
        entry["timestamp"] = datetime.now().isoformat()
        self.state.iteration_history.append(entry)
        self.save()

    def update_draft(self, draft: str, sub_version: str | None = None) -> None:
        """Update current draft and save to disk with optional sub-versioning.

        Args:
            draft: New draft text
            sub_version: Optional sub-version suffix (e.g., "source_rev_1", "style_rev_2")
        """
        self.state.current_draft = draft

        # Save to numbered file with optional sub-version
        if sub_version:
            draft_file = self.session_dir / f"draft_iter_{self.state.iteration}_{sub_version}.md"
        else:
            draft_file = self.session_dir / f"draft_iter_{self.state.iteration}.md"

        draft_file.write_text(draft)

        self.add_iteration_history(
            {"type": "draft_saved", "file": str(draft_file), "sub_version": sub_version, "length": len(draft)}
        )

    def add_source_review(self, review: dict[str, Any]) -> None:
        """Add source review result to history.

        Args:
            review: Source review result dictionary
        """
        review_entry = {"iteration": self.state.iteration, "timestamp": datetime.now().isoformat(), "review": review}

        self.state.source_reviews.append(review_entry)
        self.state.source_reviews_completed = len(self.state.source_reviews)
        self.add_iteration_history({"type": "source_review", "passed": review.get("passed", False)})

    def add_style_review(self, review: dict[str, Any]) -> None:
        """Add style review result to history.

        Args:
            review: Style review result dictionary
        """
        review_entry = {"iteration": self.state.iteration, "timestamp": datetime.now().isoformat(), "review": review}

        self.state.style_reviews.append(review_entry)
        self.state.style_reviews_completed = len(self.state.style_reviews)
        self.add_iteration_history({"type": "style_review", "passed": review.get("passed", False)})

    def add_user_feedback(self, feedback_items: list[dict]) -> None:
        """Add user feedback with full context.

        Args:
            feedback_items: List of feedback items, each with:
                - comment: The feedback text
                - line_number: Where it appears
                - context_before: Lines before (for context)
                - context_after: Lines after (for context)
        """
        feedback_entry = {
            "iteration": self.state.iteration,
            "timestamp": datetime.now().isoformat(),
            "items": feedback_items,  # Each has comment, line, context_before, context_after
        }

        self.state.user_feedback.append(feedback_entry)
        self.add_iteration_history({"type": "user_feedback", "count": len(feedback_items)})

    def increment_iteration(self) -> None:
        """Move to next iteration."""
        self.state.iteration += 1
        self.add_iteration_history({"type": "iteration_start", "iteration": self.state.iteration})

    def update_stage(self, stage: str) -> None:
        """Update current pipeline stage.

        Args:
            stage: New stage name (e.g., "style_analysis", "draft_generation")
        """
        self.state.stage = stage
        self.add_iteration_history({"type": "stage_change", "stage": stage})
        self.save()


def create_session_directory(base_path: Path = Path(".data")) -> Path:
    """Create new session directory with timestamp.

    Args:
        base_path: Base directory for sessions (default: .data/)

    Returns:
        Path to new session directory
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    session_dir = base_path / f"blog_writer_{timestamp}"
    session_dir.mkdir(parents=True, exist_ok=True)
    return session_dir


def find_latest_session(base_path: Path = Path(".data")) -> Path | None:
    """Find most recent session directory.

    Args:
        base_path: Base directory for sessions (default: .data/)

    Returns:
        Path to latest session or None if no sessions exist
    """
    sessions = sorted(base_path.glob("blog_writer_*"), reverse=True)
    return sessions[0] if sessions else None
