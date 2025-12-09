"""
Unit tests for session creation utilities.

Tests the create_standalone_session function and session configuration.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch


@pytest.mark.asyncio
async def test_create_standalone_session_basic(sample_config):
    """Test basic session creation with valid config."""
    with patch('amplifier_collection_toolkit.session.AmplifierSession') as MockSession, \
         patch('amplifier_collection_toolkit.session.StandardModuleSourceResolver') as MockResolver:
        
        # Setup mocks
        mock_session_instance = MagicMock()
        mock_session_instance.coordinator = MagicMock()
        mock_session_instance.coordinator.mount = AsyncMock()
        mock_session_instance.initialize = AsyncMock()
        MockSession.return_value = mock_session_instance
        
        mock_resolver_instance = MagicMock()
        MockResolver.return_value = mock_resolver_instance
        
        # Import and test
        from amplifier_collection_toolkit.session import create_standalone_session
        
        session = await create_standalone_session(sample_config)
        
        # Verify session was created with config
        MockSession.assert_called_once_with(config=sample_config)
        
        # Verify resolver was created with no workspace/settings
        MockResolver.assert_called_once_with(
            workspace_dir=None,
            settings_provider=None
        )
        
        # Verify resolver was mounted
        mock_session_instance.coordinator.mount.assert_called_once_with(
            "module-source-resolver", 
            mock_resolver_instance
        )
        
        # Verify session was initialized
        mock_session_instance.initialize.assert_called_once()
        
        # Verify correct session returned
        assert session == mock_session_instance


@pytest.mark.asyncio
async def test_create_standalone_session_with_source_urls(sample_config):
    """Test session creation uses source URLs from config."""
    with patch('amplifier_collection_toolkit.session.AmplifierSession') as MockSession, \
         patch('amplifier_collection_toolkit.session.StandardModuleSourceResolver'):
        
        mock_session_instance = MagicMock()
        mock_session_instance.coordinator = MagicMock()
        mock_session_instance.coordinator.mount = AsyncMock()
        mock_session_instance.initialize = AsyncMock()
        MockSession.return_value = mock_session_instance
        
        from amplifier_collection_toolkit.session import create_standalone_session
        
        # Config has source URLs
        assert "source" in sample_config["session"]["orchestrator"]
        assert "source" in sample_config["providers"][0]
        
        session = await create_standalone_session(sample_config)
        
        # Verify session received full config with sources
        call_args = MockSession.call_args
        passed_config = call_args.kwargs['config']
        assert passed_config == sample_config


@pytest.mark.asyncio
async def test_create_standalone_session_initialization_failure():
    """Test session creation handles initialization failure."""
    with patch('amplifier_collection_toolkit.session.AmplifierSession') as MockSession, \
         patch('amplifier_collection_toolkit.session.StandardModuleSourceResolver'):
        
        mock_session_instance = MagicMock()
        mock_session_instance.coordinator = MagicMock()
        mock_session_instance.coordinator.mount = AsyncMock()
        mock_session_instance.initialize = AsyncMock(side_effect=RuntimeError("Module not found"))
        MockSession.return_value = mock_session_instance
        
        from amplifier_collection_toolkit.session import create_standalone_session
        
        # Should propagate the error
        with pytest.raises(RuntimeError, match="Module not found"):
            await create_standalone_session({"session": {}, "providers": []})


@pytest.mark.asyncio
async def test_create_standalone_session_resolver_configuration(sample_config):
    """Test that resolver is configured for standalone operation."""
    with patch('amplifier_collection_toolkit.session.AmplifierSession') as MockSession, \
         patch('amplifier_collection_toolkit.session.StandardModuleSourceResolver') as MockResolver:
        
        mock_session_instance = MagicMock()
        mock_session_instance.coordinator = MagicMock()
        mock_session_instance.coordinator.mount = AsyncMock()
        mock_session_instance.initialize = AsyncMock()
        MockSession.return_value = mock_session_instance
        
        from amplifier_collection_toolkit.session import create_standalone_session
        
        await create_standalone_session(sample_config)
        
        # Verify resolver was created with standalone configuration
        call_args = MockResolver.call_args
        assert call_args.kwargs['workspace_dir'] is None
        assert call_args.kwargs['settings_provider'] is None


@pytest.mark.asyncio
async def test_create_standalone_session_mount_sequence(sample_config):
    """Test that session mount and initialization happen in correct order."""
    with patch('amplifier_collection_toolkit.session.AmplifierSession') as MockSession, \
         patch('amplifier_collection_toolkit.session.StandardModuleSourceResolver'):
        
        call_sequence = []
        
        mock_session_instance = MagicMock()
        mock_session_instance.coordinator = MagicMock()
        
        async def mock_mount(*args, **kwargs):
            call_sequence.append('mount')
        
        async def mock_initialize():
            call_sequence.append('initialize')
        
        mock_session_instance.coordinator.mount = mock_mount
        mock_session_instance.initialize = mock_initialize
        MockSession.return_value = mock_session_instance
        
        from amplifier_collection_toolkit.session import create_standalone_session
        
        await create_standalone_session(sample_config)
        
        # Verify mount happens before initialize
        assert call_sequence == ['mount', 'initialize']


@pytest.mark.asyncio
async def test_create_standalone_session_minimal_config():
    """Test session creation with minimal configuration."""
    with patch('amplifier_collection_toolkit.session.AmplifierSession') as MockSession, \
         patch('amplifier_collection_toolkit.session.StandardModuleSourceResolver'):
        
        mock_session_instance = MagicMock()
        mock_session_instance.coordinator = MagicMock()
        mock_session_instance.coordinator.mount = AsyncMock()
        mock_session_instance.initialize = AsyncMock()
        MockSession.return_value = mock_session_instance
        
        from amplifier_collection_toolkit.session import create_standalone_session
        
        minimal_config = {
            "session": {},
            "providers": []
        }
        
        session = await create_standalone_session(minimal_config)
        
        # Should still work with minimal config
        assert session == mock_session_instance
        MockSession.assert_called_once_with(config=minimal_config)
