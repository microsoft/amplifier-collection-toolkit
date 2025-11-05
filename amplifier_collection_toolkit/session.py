"""Session creation utilities for standalone scenario tools.

Provides helpers for creating AmplifierSessions with proper infrastructure setup.
Enables scenario tools to run independently without pre-installed amplifier CLI.

Philosophy:
- Structural utility (not AI wrapper) - handles infrastructure boilerplate
- Uses standard mechanisms (StandardModuleSourceResolver)
- Minimal setup (no workspace, no settings) for standalone tools
- Aligns with "mechanism not policy" - tools can customize if needed
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from amplifier_core import AmplifierSession


async def create_standalone_session(config: dict) -> "AmplifierSession":
    """Create AmplifierSession with module resolver for standalone tools.

    Enables scenario tools to run independently without pre-installed amplifier CLI.
    Uses StandardModuleSourceResolver with minimal setup (no settings, no workspace).

    Resolution strategy (3 layers):
    - Layer 1 (Environment): AMPLIFIER_MODULE_<ID> env vars (optional override)
    - Layer 4 (Profile hint): Source URLs from config (primary mechanism)
    - Layer 5 (Package): Installed packages (fallback)

    This aligns with AGENTS.md philosophy:
    - "Mechanism, not policy" - Uses standard resolver mechanism
    - "Ruthless simplicity" - Minimal setup, no complex configuration
    - "Truly standalone" - Tool fetches its own dependencies

    Args:
        config: AmplifierSession mount plan with source URLs

    Returns:
        Initialized AmplifierSession ready for use

    Raises:
        RuntimeError: If session initialization fails (e.g., module not found)

    Example:
        >>> from amplifier_collection_toolkit import create_standalone_session
        >>>
        >>> config = {
        ...     "session": {
        ...         "orchestrator": {
        ...             "module": "loop-basic",
        ...             "source": "git+https://github.com/microsoft/amplifier-module-loop-basic@main"
        ...         },
        ...         "context": {
        ...             "module": "context-simple",
        ...             "source": "git+https://github.com/microsoft/amplifier-module-context-simple@main"
        ...         },
        ...     },
        ...     "providers": [{
        ...         "module": "provider-anthropic",
        ...         "source": "git+https://github.com/microsoft/amplifier-module-provider-anthropic@main",
        ...         "config": {"model": "claude-sonnet-4-5", "temperature": 0.3}
        ...     }]
        ... }
        >>>
        >>> async with await create_standalone_session(config) as session:
        ...     result = await session.execute("analyze this")

    Note:
        Requires amplifier-module-resolution in dependencies for StandardModuleSourceResolver.
        All modules in config must include "source" URLs (git+https://...).
    """
    from amplifier_core import AmplifierSession
    from amplifier_module_resolution import StandardModuleSourceResolver

    # Create session
    session = AmplifierSession(config=config)

    # Mount minimal resolver (standalone tool policy)
    # No workspace_dir, no settings_provider → uses only env + profile hints + packages
    resolver = StandardModuleSourceResolver(
        workspace_dir=None,
        settings_provider=None,
    )

    await session.coordinator.mount("module-source-resolver", resolver)
    await session.initialize()

    return session
