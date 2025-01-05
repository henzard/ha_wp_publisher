import pytest
from unittest.mock import patch
from homeassistant import config_entries, data_entry_flow
from custom_components.ha_wp_publisher.config_flow import WPConfigFlow
from custom_components.ha_wp_publisher.const import DOMAIN

@pytest.mark.asyncio
async def test_user_step(hass):
    """Test we can configure the integration via the user step."""
    flow = WPConfigFlow()
    flow.hass = hass

    # Start the config flow
    result = await flow.async_step_user(
        user_input={
            "wp_url": "https://example.com",
            "wp_user": "username",
            "wp_password": "password",
            "entities": "sensor.my_sensor"
        }
    )
    # We expect the flow to create an entry
    assert result["type"] == data_entry_flow.FlowResultType.CREATE_ENTRY
    assert result["title"] == "HA to WP Publisher"
    assert result["data"]["wp_url"] == "https://example.com"
    assert result["data"]["wp_user"] == "username"
    assert result["data"]["wp_password"] == "password"
    assert result["data"]["entities"] == "sensor.my_sensor"
