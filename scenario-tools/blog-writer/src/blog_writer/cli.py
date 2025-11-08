"""CLI interface for blog-writer tool.

Handles:
- Command-line argument parsing
- File I/O (reading sources, writing outputs)
- Progress display (click.echo)
- Session directory and state management
- Interactive user feedback with context capture

Philosophy:
- Ruthless simplicity: Minimal CLI layer
- Present-moment focus: Solves CLI use case, no abstractions
- Rich state tracking: Complete session history for debugging
"""

import asyncio
import re
from pathlib import Path

import click
from amplifier_collection_toolkit import discover_files
from amplifier_collection_toolkit import require_minimum_files
from amplifier_collection_toolkit import validate_input_path
from amplifier_collection_toolkit import validate_output_path

from .pipeline import run_blog_writing_pipeline
from .state import StateManager
from .state import create_session_directory
from .state import find_latest_session


def extract_feedback_with_context(draft_text: str, context_lines: int = 4) -> list[dict]:
    """Extract feedback comments with surrounding context.

    Args:
        draft_text: Draft with [bracketed comments]
        context_lines: Number of lines before/after to capture

    Returns:
        List of feedback items with:
            - comment: The feedback text
            - line_number: Line number where comment appears
            - line_with_feedback: The actual line containing the feedback (comment removed)
            - context_before: Lines before the comment
            - context_after: Lines after the comment
    """
    lines = draft_text.split("\n")
    feedback_items = []
    feedback_pattern = r"\[([^\]]+)\]"

    for line_num, line in enumerate(lines):
        matches = re.findall(feedback_pattern, line)
        for match in matches:
            # Capture surrounding context
            start_idx = max(0, line_num - context_lines)
            end_idx = min(len(lines), line_num + context_lines + 1)

            context_before = lines[start_idx:line_num]
            context_after = lines[line_num + 1 : end_idx]

            # Extract the line with feedback, removing the comment brackets
            line_with_feedback = re.sub(r"\[[^\]]+\]", "", line).strip()

            feedback_items.append(
                {
                    "comment": match,
                    "line_number": line_num + 1,
                    "line_with_feedback": line_with_feedback,
                    "context_before": context_before,
                    "context_after": context_after,
                }
            )

    return feedback_items


@click.command()
@click.option(
    "--source", "-s", type=click.Path(exists=True, path_type=Path), required=True, help="Source file (brain dump/notes)"
)
@click.option(
    "--style-dir",
    "-d",
    type=click.Path(exists=True, path_type=Path),
    required=True,
    help="Directory of your writing samples",
)
@click.option(
    "--output", "-o", type=click.Path(path_type=Path), required=True, help="Output file for generated blog post"
)
@click.option(
    "--draft",
    type=click.Path(exists=True, path_type=Path),
    required=False,
    help="Existing draft with feedback comments",
)
@click.option("--resume", is_flag=True, help="Resume from last checkpoint")
@click.option("--interactive/--no-interactive", default=True, help="Enable interactive feedback mode (default: True)")
def cli(source: Path, style_dir: Path, output: Path, draft: Path | None, resume: bool, interactive: bool):
    """
    Blog Writer - Transform brain dumps into polished blog posts in your style.

    This tool uses 5 specialized AI configs in a metacognitive recipe:
    1. Style Analyzer (analytical) - Learns your writing patterns
    2. Draft Writer (creative) - Generates initial content
    3. Source Reviewer (critical) - Verifies accuracy
    4. Style Reviewer (critical) - Checks consistency
    5. Feedback Incorporator (balanced) - Applies your guidance

    Example:
        blog-writer --source ideas.md --style-dir ~/blog/ --output draft.md
    """
    click.echo("🚀 Blog Writer - Multi-Config Metacognitive Recipe")

    # Validate inputs
    validate_input_path(source, must_exist=True, must_be_dir=False)
    validate_input_path(style_dir, must_exist=True, must_be_dir=True)
    validate_output_path(output)

    # Create or find session directory
    if resume and not draft:
        session_dir = find_latest_session()
        if session_dir:
            click.echo(f"♻️  Resuming session: {session_dir.name}")
        else:
            click.echo("⚠️  No previous session found, creating new session")
            session_dir = create_session_directory()
    else:
        session_dir = create_session_directory()

    # Initialize state manager
    state_manager = StateManager(session_dir)
    state = state_manager.state

    # Store input parameters for reference
    if not state.source_path:
        state.source_path = str(source)
        state.style_dir_path = str(style_dir)
        state.output_path = str(output)
        state_manager.save()

    # Display resume info if applicable
    if resume and state.iteration > 0:
        click.echo("\n📊 Resume Status:")
        click.echo(f"   - Iteration: {state.iteration}")
        click.echo(f"   - Stage: {state.stage}")
        click.echo(f"   - Style analysis: {'✓' if state.style_profile else '✗'}")
        click.echo(f"   - Current draft: {'✓' if state.current_draft else '✗'}")
        click.echo(f"   - Source reviews: {state.source_reviews_completed}")
        click.echo(f"   - Style reviews: {state.style_reviews_completed}")

    # Read source file
    source_content = source.read_text()

    # Discover and read style samples
    style_files = discover_files(style_dir, "**/*.md")
    require_minimum_files(style_files, minimum=2, file_type="style sample files")

    click.echo(f"   Found {len(style_files)} writing samples")

    style_samples = []
    for file in style_files[:10]:  # Limit to 10 samples
        style_samples.append({"file": file.name, "content": file.read_text()})

    # Read draft with feedback if provided
    user_feedback = draft.read_text() if draft else None
    if user_feedback:
        click.echo(f"\n📝 Loading draft with feedback from {draft}")

    # Track feedback rounds
    feedback_rounds = 0

    # Run pipeline with StateManager
    result = asyncio.run(
        run_blog_writing_pipeline(
            source_content=source_content,
            style_samples=style_samples,
            user_feedback=user_feedback,
            state_manager=state_manager,
            on_progress=lambda msg: click.echo(msg),
        )
    )

    # Draft is already saved by state_manager.update_draft()
    iteration_file = session_dir / f"draft_iter_{state.iteration}.md"
    click.echo(f"\n💾 Draft saved: {iteration_file.name}")

    # Show quality metrics from initial generation
    metrics = result["quality_metrics"]
    source_reviews = metrics["source_reviews_completed"]
    style_reviews = metrics["style_reviews_completed"]

    # Interactive feedback loop (if enabled and not providing draft)
    if interactive and not draft:
        while state.iteration < 10:  # Max 10 iterations
            # Display review issues if any
            if result.get("review_issues"):
                click.echo("\n⚠️  Issues found during review:")
                for issue in result["review_issues"][:3]:
                    click.echo(f"   • {issue}")
                if len(result["review_issues"]) > 3:
                    click.echo(f"   ... and {len(result['review_issues']) - 3} more")

            # INTERACTIVE PAUSE
            click.echo("\n" + "=" * 60)
            click.echo(f"ITERATION {state.iteration} - BLOG DRAFT REVIEW")
            click.echo("=" * 60)
            click.echo(f"\nDraft saved to: {iteration_file}")
            click.echo("\n📝 INSTRUCTIONS:")
            click.echo("  1. Open the draft file in your editor")
            click.echo("  2. Add [bracketed comments] inline where you want changes")
            click.echo("  3. Save the file")
            click.echo("  4. Come back here and:")
            click.echo("     • Type 'done' when you've added comments")
            click.echo("     • Type 'approve' to accept without changes")
            click.echo("     • Type 'quit' to exit")
            click.echo("-" * 60)

            user_choice = click.prompt("Your choice", type=str).strip().lower()

            if user_choice in ["approve", "approved"]:
                # Save as final and exit
                output.write_text(result["draft"])
                click.echo(f"\n✨ Blog post approved and saved to: {output}")
                break

            if user_choice == "quit":
                click.echo(f"\n💾 Draft saved to: {iteration_file}")
                click.echo("   Resume with: blog-writer --resume")
                return

            if user_choice in ["done", "d", ""]:
                # Read feedback from edited file
                draft_with_feedback = iteration_file.read_text()

                # Extract bracketed comments WITH CONTEXT
                feedback_items_with_context = extract_feedback_with_context(draft_with_feedback)

                if feedback_items_with_context:
                    click.echo(f"\n📋 Found {len(feedback_items_with_context)} feedback items:")
                    for i, item in enumerate(feedback_items_with_context[:5], 1):
                        click.echo(f"  {i}. [{item['comment']}] (line {item['line_number']})")
                    if len(feedback_items_with_context) > 5:
                        click.echo(f"  ... and {len(feedback_items_with_context) - 5} more")

                    # Save feedback with context to state
                    state_manager.add_user_feedback(feedback_items_with_context)
                    feedback_rounds += 1

                    # Run revision
                    click.echo(f"\n🔄 Applying feedback (iteration {state.iteration + 1})...")
                    result = asyncio.run(
                        run_blog_writing_pipeline(
                            source_content=source_content,
                            style_samples=style_samples,
                            user_feedback=draft_with_feedback,
                            state_manager=state_manager,
                            on_progress=lambda msg: click.echo(msg),
                        )
                    )

                    # Draft already saved by state_manager
                    iteration_file = session_dir / f"draft_iter_{state.iteration}.md"
                    click.echo(f"💾 Revision saved: {iteration_file.name}")

                    # Update metrics
                    metrics = result["quality_metrics"]
                    source_reviews = metrics["source_reviews_completed"]
                    style_reviews = metrics["style_reviews_completed"]
                else:
                    click.echo("\n⚠️  No feedback found. Use [brackets] to add comments.")
                    continue
            else:
                click.echo(f"\n❓ Unknown choice: {user_choice}")
                continue
    else:
        # Non-interactive mode - save final output
        output.write_text(result["draft"])
        click.echo(f"\n✅ Blog post saved to {output}")

    # Enhanced completion message
    click.echo("\n" + "=" * 60)
    click.echo("✨ BLOG POST GENERATION COMPLETE!")
    click.echo("=" * 60)
    click.echo(f"\n📄 Final post: {output}")
    click.echo(f"📁 Session data: {session_dir}")
    click.echo(f"🔄 Total iterations: {state.iteration}")
    click.echo("📊 Quality metrics:")
    click.echo(f"   - Source reviews: {source_reviews}")
    click.echo(f"   - Style reviews: {style_reviews}")
    click.echo(f"   - User feedback rounds: {feedback_rounds}")
    click.echo(f"\n💾 State file: {session_dir / 'state.json'}")
    click.echo("✅ Ready to publish!")


if __name__ == "__main__":
    cli()
