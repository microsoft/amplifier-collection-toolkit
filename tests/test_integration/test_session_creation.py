"""
Integration tests for session creation.

Tests the full session creation flow with mocked external dependencies.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch


@pytest.mark.asyncio
async def test_session_creation_full_flow(sample_config):
    """Integration test: Full session creation with all components."""
    with patch('amplifier_collection_toolkit.session.AmplifierSession') as MockSession, \
         patch('amplifier_collection_toolkit.session.StandardModuleSourceResolver') as MockResolver:
        
        # Setup realistic mocks
        mock_session = MagicMock()
        mock_session.coordinator = MagicMock()
        mock_session.coordinator.mount = AsyncMock()
        mock_session.initialize = AsyncMock()
        MockSession.return_value = mock_session
        
        mock_resolver = MagicMock()
        MockResolver.return_value = mock_resolver
        
        from amplifier_collection_toolkit.session import create_standalone_session
        
        # Create session
        session = await create_standalone_session(sample_config)
        
        # Verify complete flow
        assert MockSession.called
        assert MockResolver.called
        assert mock_session.coordinator.mount.called
        assert mock_session.initialize.called
        assert session == mock_session


@pytest.mark.asyncio
async def test_session_creation_with_multiple_providers(sample_config):
    """Integration test: Session creation with multiple providers."""
    with patch('amplifier_collection_toolkit.session.AmplifierSession') as MockSession, \
         patch('amplifier_collection_toolkit.session.StandardModuleSourceResolver'):
        
        mock_session = MagicMock()
        mock_session.coordinator = MagicMock()
        mock_session.coordinator.mount = AsyncMock()
        mock_session.initialize = AsyncMock()
        MockSession.return_value = mock_session
        
        # Config with multiple providers
        multi_provider_config = {
            "session": sample_config["session"],
            "providers": [
                sample_config["providers"][0],
                {
                    "module": "provider-openai",
                    "source": "git+https://github.com/microsoft/amplifier-module-provider-openai@main",
                    "config": {"model": "gpt-4", "temperature": 0.5}
                }
            ]
        }
        
        from amplifier_collection_toolkit.session import create_standalone_session
        
        session = await create_standalone_session(multi_provider_config)
        
        # Verify config passed through correctly
        call_args = MockSession.call_args
        passed_config = call_args.kwargs['config']
        assert len(passed_config['providers']) == 2


@pytest.mark.asyncio
async def test_session_creation_resolver_configuration(sample_config):
    """Integration test: Verify resolver is configured correctly for standalone use."""
    with patch('amplifier_collection_toolkit.session.AmplifierSession') as MockSession, \
         patch('amplifier_collection_toolkit.session.StandardModuleSourceResolver') as MockResolver:
        
        mock_session = MagicMock()
        mock_session.coordinator = MagicMock()
        mock_session.coordinator.mount = AsyncMock()
        mock_session.initialize = AsyncMock()
        MockSession.return_value = mock_session
        
        from amplifier_collection_toolkit.session import create_standalone_session
        
        await create_standalone_session(sample_config)
        
        # Verify resolver configuration for standalone operation
        resolver_call = MockResolver.call_args
        assert resolver_call.kwargs['workspace_dir'] is None
        assert resolver_call.kwargs['settings_provider'] is None


@pytest.mark.asyncio
async def test_session_creation_error_handling(sample_config):
    """Integration test: Session creation handles errors gracefully."""
    with patch('amplifier_collection_toolkit.session.AmplifierSession') as MockSession, \
         patch('amplifier_collection_toolkit.session.StandardModuleSourceResolver'):
        
        mock_session = MagicMock()
        mock_session.coordinator = MagicMock()
        mock_session.coordinator.mount = AsyncMock()
        mock_session.initialize = AsyncMock(side_effect=RuntimeError("Module resolution failed"))
        MockSession.return_value = mock_session
        
        from amplifier_collection_toolkit.session import create_standalone_session
        
        # Should propagate initialization errors
        with pytest.raises(RuntimeError, match="Module resolution failed"):
            await create_standalone_session(sample_config)
