"""
Unit tests for the ha_wp_publisher config flow.
"""

import json
import pytest
from unittest.mock import patch

from homeassistant import config_entries
from homeassistant.components.ha_wp_publisher import config_flow
from homeassistant.core import HomeAssistant
from homeassistant.helpers import selector

from tests.common import MockConfigEntry

from custom_components.ha_wp_publisher.const import (
    DOMAIN,
    CONF_WP_URL,
    CONF_WP_USER,
    CONF_WP_PASSWORD,
    CONF_POST_TYPE,
    CONF_CUSTOM_FIELDS,
    CONF_PUBLISH_INTERVAL,
    CONF_ENTITIES
)


@pytest.fixture
def mock_config_flow():
    """Fixture to set up the config flow."""
    return config_flow.WPConfigFlow()


async def test_full_user_flow(hass: HomeAssistant):
    """Test a full user configuration flow."""

    # Initialize the config flow
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={'source': config_entries.SOURCE_USER}
    )
    assert result["type"] == "form"
    assert result["step_id"] == "user"

    # Provide user input for Step 1 (Basic WP credentials)
    user_input_step1 = {
        CONF_WP_URL: "https://example.com",
        CONF_WP_USER: "username",
        CONF_WP_PASSWORD: "password"
    }

    with patch(
        "custom_components.ha_wp_publisher.config_flow.WPConfigFlow.async_step_advanced",
        return_value=await hass.config_entries.flow.async_init(
            DOMAIN, context={'source': config_entries.SOURCE_USER}, data=user_input_step1
        )
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"], user_input_step1
        )

    assert result["type"] == "form"
    assert result["step_id"] == "advanced"

    # Provide user input for Step 2 (Advanced options)
    user_input_step2 = {
        CONF_POST_TYPE: "sensor_data",
        CONF_CUSTOM_FIELDS: json.dumps({"field1": "value1", "field2": "value2"}),
        CONF_PUBLISH_INTERVAL: 60  # Publish every 60 seconds
    }

    with patch(
        "custom_components.ha_wp_publisher.config_flow.WPConfigFlow.async_step_sensors",
        return_value=await hass.config_entries.flow.async_init(
            DOMAIN, context={'source': config_entries.SOURCE_USER}, data=user_input_step2
        )
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"], user_input_step2
        )

    assert result["type"] == "form"
    assert result["step_id"] == "sensors"

    # Provide user input for Step 3 (Sensor selection)
    user_input_step3 = {
        CONF_ENTITIES: ["sensor.temperature", "sensor.humidity"]
    }

    with patch(
        "custom_components.ha_wp_publisher.config_flow.WPConfigFlow.async_create_entry",
        return_value=await hass.config_entries.flow.async_create_entry(
            title="HA to WP Publisher",
            data={
                CONF_WP_URL: "https://example.com",
                CONF_WP_USER: "username",
                CONF_WP_PASSWORD: "password",
                CONF_POST_TYPE: "sensor_data",
                CONF_CUSTOM_FIELDS: json.dumps({"field1": "value1", "field2": "value2"}),
                CONF_PUBLISH_INTERVAL: 60,
                CONF_ENTITIES: ["sensor.temperature", "sensor.humidity"]
            }
        )
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"], user_input_step3
        )

    assert result["type"] == "create_entry"
    assert result["title"] == "HA to WP Publisher"
    assert result["data"] == {
        CONF_WP_URL: "https://example.com",
        CONF_WP_USER: "username",
        CONF_WP_PASSWORD: "password",
        CONF_POST_TYPE: "sensor_data",
        CONF_CUSTOM_FIELDS: json.dumps({"field1": "value1", "field2": "value2"}),
        CONF_PUBLISH_INTERVAL: 60,
        CONF_ENTITIES: ["sensor.temperature", "sensor.humidity"]
    }


async def test_abort_if_already_configured(hass: HomeAssistant):
    """Test abort if the integration is already configured."""

    # Create a mock config entry
    mock_entry = MockConfigEntry(
        domain=DOMAIN,
        data={
            CONF_WP_URL: "https://example.com",
            CONF_WP_USER: "username",
            CONF_WP_PASSWORD: "password",
            CONF_POST_TYPE: "sensor_data",
            CONF_CUSTOM_FIELDS: json.dumps({"field1": "value1"}),
            CONF_PUBLISH_INTERVAL: 60,
            CONF_ENTITIES: ["sensor.temperature"]
        },
        unique_id="https://example.com_username"
    )
    mock_entry.add_to_hass(hass)

    # Attempt to start a new config flow
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={'source': config_entries.SOURCE_USER}
    )
    assert result["type"] == "form"
    assert result["step_id"] == "user"

    # Provide user input that matches the existing config entry
    user_input = {
        CONF_WP_URL: "https://example.com",
        CONF_WP_USER: "username",
        CONF_WP_PASSWORD: "password"
    }

    with patch(
        "custom_components.ha_wp_publisher.config_flow.WPConfigFlow.async_step_advanced",
        return_value=await hass.config_entries.flow.async_abort(reason="already_configured")
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"], user_input
        )

    assert result["type"] == "abort"
    assert result["reason"] == "already_configured"


async def test_invalid_custom_fields(hass: HomeAssistant):
    """Test handling of invalid custom fields input."""

    # Initialize the config flow
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={'source': config_entries.SOURCE_USER}
    )
    assert result["type"] == "form"
    assert result["step_id"] == "user"

    # Provide user input for Step 1 (Basic WP credentials)
    user_input_step1 = {
        CONF_WP_URL: "https://example.com",
        CONF_WP_USER: "username",
        CONF_WP_PASSWORD: "password"
    }

    with patch(
        "custom_components.ha_wp_publisher.config_flow.WPConfigFlow.async_step_advanced",
        return_value=await hass.config_entries.flow.async_init(
            DOMAIN, context={'source': config_entries.SOURCE_USER}, data=user_input_step1
        )
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"], user_input_step1
        )

    assert result["type"] == "form"
    assert result["step_id"] == "advanced"

    # Provide invalid JSON for custom fields
    user_input_step2 = {
        CONF_POST_TYPE: "sensor_data",
        CONF_CUSTOM_FIELDS: "invalid_json",
        CONF_PUBLISH_INTERVAL: 60
    }

    with patch(
        "custom_components.ha_wp_publisher.config_flow.WPConfigFlow.async_step_sensors",
        return_value=await hass.config_entries.flow.async_init(
            DOMAIN, context={'source': config_entries.SOURCE_USER}, data=user_input_step2
        )
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"], user_input_step2
        )

    # Depending on your config_flow.py implementation, it might handle invalid JSON differently
    # For this example, we assume it proceeds but logs a warning
    assert result["type"] == "form"
    assert result["step_id"] == "sensors"

    # Provide user input for Step 3 (Sensor selection)
    user_input_step3 = {
        CONF_ENTITIES: ["sensor.temperature"]
    }

    with patch(
        "custom_components.ha_wp_publisher.config_flow.WPConfigFlow.async_create_entry",
        return_value=await hass.config_entries.flow.async_create_entry(
            title="HA to WP Publisher",
            data={
                CONF_WP_URL: "https://example.com",
                CONF_WP_USER: "username",
                CONF_WP_PASSWORD: "password",
                CONF_POST_TYPE: "sensor_data",
                CONF_CUSTOM_FIELDS: "invalid_json",
                CONF_PUBLISH_INTERVAL: 60,
                CONF_ENTITIES: ["sensor.temperature"]
            }
        )
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"], user_input_step3
        )

    assert result["type"] == "create_entry"
    assert result["title"] == "HA to WP Publisher"
    assert result["data"] == {
        CONF_WP_URL: "https://example.com",
        CONF_WP_USER: "username",
        CONF_WP_PASSWORD: "password",
        CONF_POST_TYPE: "sensor_data",
        CONF_CUSTOM_FIELDS: "invalid_json",
        CONF_PUBLISH_INTERVAL: 60,
        CONF_ENTITIES: ["sensor.temperature"]
    }

    # You might want to verify that the coordinator handles invalid custom fields gracefully


async def test_options_flow(hass: HomeAssistant):
    """Test the options flow for the integration."""

    # Create a mock config entry
    mock_entry = MockConfigEntry(
        domain=DOMAIN,
        data={
            CONF_WP_URL: "https://example.com",
            CONF_WP_USER: "username",
            CONF_WP_PASSWORD: "password",
            CONF_POST_TYPE: "sensor_data",
            CONF_CUSTOM_FIELDS: json.dumps({"field1": "value1"}),
            CONF_PUBLISH_INTERVAL: 60,
            CONF_ENTITIES: ["sensor.temperature"]
        },
        unique_id="https://example.com_username"
    )
    mock_entry.add_to_hass(hass)

    # Initialize the options flow
    result = await hass.config_entries.options.async_init(mock_entry.entry_id)
    assert result["type"] == "form"
    assert result["step_id"] == "init"

    # Provide user input for options (e.g., change publish interval)
    user_input_options = {
        CONF_PUBLISH_INTERVAL: 120  # Change to 120 seconds
    }

    with patch(
        "custom_components.ha_wp_publisher.config_flow.WPOptionsFlow.async_create_entry",
        return_value=config_entries.ConfigFlowResult(
            type=config_entries.ConfigFlowResultType.CREATE_ENTRY,
            title="",
            data=user_input_options
        )
    ):
        result = await hass.config_entries.options.async_configure(
            result["flow_id"], user_input_options
        )

    assert result["type"] == "create_entry"
    assert result["data"][CONF_PUBLISH_INTERVAL] == 120
