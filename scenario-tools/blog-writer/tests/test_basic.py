"""Basic tests for blog writer."""

from blog_writer.state import StateManager


def test_state_manager(tmp_path):
    """Test StateManager with session directory."""
    session_dir = tmp_path / "test_session"

    # Create state manager
    manager = StateManager(session_dir)

    # Check initial state
    assert manager.state.stage == "initialized"
    assert manager.state.iteration == 0
    assert session_dir.exists()
    assert (session_dir / "state.json").exists()

    # Update draft
    manager.update_draft("# Test Draft\n\nContent here")
    assert manager.state.current_draft == "# Test Draft\n\nContent here"
    assert (session_dir / "draft_iter_0.md").exists()

    # Add iteration history
    manager.add_iteration_history({"type": "test_operation", "data": "test"})
    assert len(manager.state.iteration_history) > 0
    assert manager.state.iteration_history[-1]["type"] == "test_operation"

    # Add user feedback
    manager.add_user_feedback(
        [{"comment": "test feedback", "line_number": 5, "context_before": [], "context_after": []}]
    )
    assert len(manager.state.user_feedback) == 1

    # Increment iteration
    manager.increment_iteration()
    assert manager.state.iteration == 1

    # Save and reload
    manager.save()
    manager2 = StateManager(session_dir)
    assert manager2.state.iteration == 1
    assert manager2.state.current_draft == "# Test Draft\n\nContent here"
