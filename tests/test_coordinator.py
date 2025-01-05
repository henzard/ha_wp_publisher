# tests/test_coordinator.py

import json
import pytest
from unittest.mock import patch, AsyncMock

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import UpdateFailed

from ha_wp_publisher.coordinator import WordPressPublisherCoordinator
from ha_wp_publisher.const import (
    CONF_WP_URL,
    CONF_WP_USER,
    CONF_WP_PASSWORD,
    CONF_POST_TYPE,
    CONF_CUSTOM_FIELDS,
    CONF_PUBLISH_INTERVAL,
    CONF_ENTITIES
)


@pytest.fixture
def config_data():
    """Sample configuration data for the coordinator."""
    return {
        CONF_WP_URL: "https://example.com",
        CONF_WP_USER: "username",
        CONF_WP_PASSWORD: "password",
        CONF_POST_TYPE: "sensor_data",
        CONF_CUSTOM_FIELDS: json.dumps({"field1": "value1"}),
        CONF_PUBLISH_INTERVAL: 0,  # Real-time publishing
        CONF_ENTITIES: ["sensor.temperature", "sensor.humidity"]
    }


@pytest.fixture
def coordinator(hass: HomeAssistant, config_data):
    """Fixture to create a coordinator instance."""
    return WordPressPublisherCoordinator(hass, config_data)


async def test_coordinator_publish_success(hass: HomeAssistant, coordinator: WordPressPublisherCoordinator):
    """Test successful publishing of sensor data to WordPress."""

    entity_id = "sensor.temperature"
    new_state = "25°C"

    post_data = coordinator._build_post_data(entity_id, new_state)
    endpoint = f"{coordinator.wp_url.strip('/')}/wp-json/wp/v2/{coordinator.post_type.strip('/')}"

    with patch("requests.post") as mock_post:
        mock_response = AsyncMock()
        mock_response.raise_for_status = AsyncMock()
        mock_response.text = '{"id": 123, "title": "Sensor Update: sensor.temperature"}'
        mock_post.return_value = mock_response

        await coordinator.async_publish_state(entity_id, new_state)

        mock_post.assert_called_once_with(
            endpoint,
            json=post_data,
            auth=(coordinator.wp_user, coordinator.wp_password),
            timeout=10
        )

    # Check that last_publish_info is updated correctly
    assert coordinator.last_publish_info["last_published_entity"] == entity_id
    assert coordinator.last_publish_info["last_publish_error"] is None
    assert coordinator.last_publish_info["last_published_time"] is not None


async def test_coordinator_publish_failure(hass: HomeAssistant, coordinator: WordPressPublisherCoordinator):
    """Test failed publishing of sensor data to WordPress."""

    entity_id = "sensor.humidity"
    new_state = "60%"

    with patch("requests.post", side_effect=requests.exceptions.RequestException("Connection error")) as mock_post:
        with pytest.raises(UpdateFailed):
            await coordinator.async_publish_state(entity_id, new_state)

        mock_post.assert_called_once()

    # Check that last_publish_info is updated with error
    assert coordinator.last_publish_info["last_published_entity"] == entity_id
    assert coordinator.last_publish_info["last_publish_error"] == "Connection error"
    assert coordinator.last_publish_info["last_published_time"] is None


async def test_coordinator_scheduled_publish(hass: HomeAssistant):
    """Test scheduled publishing of sensor data to WordPress."""

    config_data = {
        CONF_WP_URL: "https://example.com",
        CONF_WP_USER: "username",
        CONF_WP_PASSWORD: "password",
        CONF_POST_TYPE: "sensor_data",
        CONF_CUSTOM_FIELDS: json.dumps({"field1": "value1"}),
        CONF_PUBLISH_INTERVAL: 60,  # Publish every 60 seconds
        CONF_ENTITIES: ["sensor.temperature", "sensor.humidity"]
    }

    coordinator = WordPressPublisherCoordinator(hass, config_data)

    # Mock the async_publish_state method
    with patch.object(coordinator, 'async_publish_state', new_callable=AsyncMock) as mock_publish:
        # Simulate a scheduled update
        await coordinator.async_refresh()

        # Ensure async_publish_state is called for each entity
        assert mock_publish.call_count == 2
        mock_publish.assert_any_call("sensor.temperature", "25°C")
        mock_publish.assert_any_call("sensor.humidity", "60%")

    # You can add more assertions based on how your coordinator gathers states


async def test_coordinator_handle_invalid_custom_fields(hass: HomeAssistant):
    """Test coordinator handling of invalid custom fields."""

    invalid_config_data = {
        CONF_WP_URL: "https://example.com",
        CONF_WP_USER: "username",
        CONF_WP_PASSWORD: "password",
        CONF_POST_TYPE: "sensor_data",
        CONF_CUSTOM_FIELDS: "invalid_json",  # Invalid JSON
        CONF_PUBLISH_INTERVAL: 0,
        CONF_ENTITIES: ["sensor.temperature"]
    }

    coordinator = WordPressPublisherCoordinator(hass, invalid_config_data)

    assert coordinator.custom_fields == {}  # Should fallback to empty dict

    entity_id = "sensor.temperature"
    new_state = "25°C"

    post_data = coordinator._build_post_data(entity_id, new_state)
    endpoint = f"{coordinator.wp_url.strip('/')}/wp-json/wp/v2/{coordinator.post_type.strip('/')}"

    with patch("requests.post") as mock_post:
        mock_response = AsyncMock()
        mock_response.raise_for_status = AsyncMock()
        mock_response.text = '{"id": 123, "title": "Sensor Update: sensor.temperature"}'
        mock_post.return_value = mock_response

        await coordinator.async_publish_state(entity_id, new_state)

        mock_post.assert_called_once_with(
            endpoint,
            json=post_data,
            auth=(coordinator.wp_user, coordinator.wp_password),
            timeout=10
        )

    # Check that last_publish_info is updated correctly
    assert coordinator.last_publish_info["last_published_entity"] == entity_id
    assert coordinator.last_publish_info["last_publish_error"] is None
    assert coordinator.last_publish_info["last_published_time"] is not None
