"""Test configuration for ha_wp_publisher."""
import os
import sys
from pathlib import Path

import pytest
from homeassistant.setup import async_setup_component
from homeassistant.core import HomeAssistant

# Get the root directory of the project
ROOT_DIR = Path(__file__).parent.parent.absolute()

# Add the root directory to Python path
sys.path.insert(0, str(ROOT_DIR))

@pytest.fixture
async def hass() -> HomeAssistant:
    """Create a Home Assistant instance for testing."""
    hass = HomeAssistant()
    await async_setup_component(hass, "homeassistant", {})
    return hass

# Create pytest fixtures that can be used across all tests
@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(monkeypatch):
    """Enable custom integrations in Home Assistant."""
    monkeypatch.setenv("PYTEST_ENABLE_CUSTOM_INTEGRATIONS", "1")

@pytest.fixture
def hass_storage():
    """Fixture to mock storage."""
    return {} 