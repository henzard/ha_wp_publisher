import logging
import aiohttp
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

# If you have these in your const.py, import them:
# from .const import (
#     DOMAIN, CONF_WP_URL, CONF_WP_USER, CONF_WP_PASSWORD,
#     CONF_POST_TYPE, CONF_CUSTOM_FIELDS, CONF_PUBLISH_INTERVAL,
#     CONF_ENTITIES
# )

DOMAIN = "ha_wp_publisher"

CONF_WP_URL = "wp_url"
CONF_WP_USER = "wp_user"
CONF_WP_PASSWORD = "wp_password"

CONF_POST_TYPE = "post_type"
CONF_CUSTOM_FIELDS = "custom_fields"
CONF_PUBLISH_INTERVAL = "publish_interval"
CONF_ENTITIES = "entities"

_LOGGER = logging.getLogger(__name__)


class WordPressPublisherCoordinator(DataUpdateCoordinator):
    """
    Coordinates publishing sensor data to WordPress, either on a schedule
    or in real time (if update_interval is None or zero).
    """

    def __init__(
        self,
        hass: HomeAssistant,
        config_data: dict,
    ):
        """
        :param hass: HomeAssistant instance.
        :param config_data: Dictionary containing user config from config_flow.
        """
        # Determine update interval (scheduled publishing) vs. real-time (None or 0)
        interval_seconds = config_data.get(CONF_PUBLISH_INTERVAL, 0)
        update_interval = None
        if interval_seconds > 0:
            update_interval = timedelta(seconds=interval_seconds)

        super().__init__(
            hass,
            _LOGGER,
            name="WordPress Publisher Coordinator",
            update_interval=update_interval
        )

        # Store WP config
        self.wp_url = config_data.get(CONF_WP_URL)
        self.wp_user = config_data.get(CONF_WP_USER)
        self.wp_password = config_data.get(CONF_WP_PASSWORD)

        # Advanced WP settings
        self.post_type = config_data.get(CONF_POST_TYPE, "posts")
        self.custom_fields_str = config_data.get(CONF_CUSTOM_FIELDS, "")

        # Entities to track
        self.entities = config_data.get(CONF_ENTITIES, [])

        # We can parse custom_fields from a JSON string or comma-delimited pairs if we want
        # Here, assume user can provide them in JSON form. Example: {"field1": "val1", "field2": "val2"}
        try:
            import json
            self.custom_fields = json.loads(self.custom_fields_str) if self.custom_fields_str else {}
        except Exception:
            _LOGGER.warning("Failed to parse custom_fields as JSON. Using empty dict.")
            self.custom_fields = {}

        # For storing latest publish status info if you want to reference it in a sensor, etc.
        self.last_publish_info = {
            "last_published_entity": None,
            "last_published_time": None,
            "last_publish_error": None,
        }

        _LOGGER.debug(
            "Coordinator initialized with WP URL: %s, post_type: %s, update_interval: %s",
            self.wp_url, self.post_type, str(self.update_interval)
        )

    async def _async_update_data(self):
        """
        If update_interval is set, this method is called automatically on schedule.
        Otherwise, if update_interval is None, we rely on real-time triggers (like state_changed).
        This function can do a 'batch publish' or simply gather data for each entity.
        """
        _LOGGER.debug("Scheduled publishing triggered.")
        # Real-time approach: you might not do anything here if you handle immediate state changes elsewhere.
        # For a scheduled approach, gather states and publish them in bulk or one by one.

        data_to_publish = {}
        for entity_id in self.entities:
            state_obj = self.hass.states.get(entity_id)
            if state_obj is not None:
                data_to_publish[entity_id] = state_obj.state
            else:
                _LOGGER.warning("Entity %s not found in HA states.", entity_id)

        # Attempt to publish each sensor’s state
        for entity_id, state_val in data_to_publish.items():
            await self.async_publish_state(entity_id, state_val)

        # Return data_to_publish so HA knows the result of this update
        return data_to_publish

    async def async_publish_state(self, entity_id: str, new_state):
        """
        Publish the state of a specific entity to WordPress.
        Called manually on real-time triggers or within _async_update_data for scheduled updates.

        :param entity_id: The Home Assistant entity ID.
        :param new_state: The new state value to be published.
        """
        _LOGGER.debug("Publishing %s to WP as post_type '%s'.", entity_id, self.post_type)
        try:
            post_data = self._build_post_data(entity_id, new_state)
            endpoint = f"{self.wp_url.strip('/')}/wp-json/wp/v2/{self.post_type.strip('/')}"
            _LOGGER.debug("POST endpoint: %s", endpoint)

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    endpoint,
                    json=post_data,
                    auth=aiohttp.BasicAuth(self.wp_user, self.wp_password),
                    timeout=10
                ) as response:
                    response.raise_for_status()
                    _LOGGER.info("Successfully published %s state to WP. Response: %s", entity_id, await response.text())

                    # Update last publish info
                    self.last_publish_info["last_published_entity"] = entity_id
                    self.last_publish_info["last_published_time"] = self.hass.helpers.event.dt_util.now()
                    self.last_publish_info["last_publish_error"] = None

        except Exception as err:
            _LOGGER.error("Error publishing %s to WP: %s", entity_id, err)
            self.last_publish_info["last_publish_error"] = str(err)
            raise UpdateFailed from err

    def _build_post_data(self, entity_id: str, new_state):
        """
        Helper to create the JSON payload for WordPress.

        :param entity_id: The sensor entity_id.
        :param new_state: The new state value.
        :return: Dict used by the WP REST API.
        """
        # Basic example with 'title' and 'content'
        post_data = {
            "title": f"Sensor Update: {entity_id}",
            "content": f"New state: {new_state}",
            "status": "publish"
        }

        # Merge custom fields or meta if provided
        # Note: Depending on WP setup (ACF or otherwise) the field syntax can vary
        if self.custom_fields:
            # Example of adding them under 'meta' or 'fields'
            # Adjust to your environment
            post_data["meta"] = []
            for key, val in self.custom_fields.items():
                post_data["meta"].append({"key": key, "value": val})

        return post_data
