"""Test configuration for ha_wp_publisher."""
import os
import sys
from pathlib import Path

import pytest

# Get the root directory of the project
ROOT_DIR = Path(__file__).parent.parent.absolute()

# Add the custom_components directory to Python path
CUSTOM_COMPONENTS_DIR = ROOT_DIR / "custom_components"
sys.path.insert(0, str(CUSTOM_COMPONENTS_DIR))

# Create pytest fixtures that can be used across all tests
@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(monkeypatch):
    """Enable custom integrations in Home Assistant."""
    monkeypatch.setenv("PYTEST_ENABLE_CUSTOM_INTEGRATIONS", "1")

@pytest.fixture
def hass_storage():
    """Fixture to mock storage."""
    return {} 