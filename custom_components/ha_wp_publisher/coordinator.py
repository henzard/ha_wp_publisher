import logging
import requests

from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

_LOGGER = logging.getLogger(__name__)

class WordPressPublisherCoordinator(DataUpdateCoordinator):
    """Coordinator to publish data to WordPress."""

    def __init__(self, hass: HomeAssistant, wp_url, wp_user, wp_password, entities):
        """Initialize."""
        super().__init__(
            hass,
            _LOGGER,
            name="WordPress Publisher",
            update_interval=None,  # We might publish on state change, not a timed poll
        )
        self.wp_url = wp_url
        self.wp_user = wp_user
        self.wp_password = wp_password
        self.entities = entities

    async def async_publish_state(self, entity_id: str, new_state):
        """Publish the state of an entity to WordPress."""
        # Example of using the WP REST API to do something—like create a post or update data
        try:
            # This is a generic example endpoint; adjust for your actual WP plugin endpoint or the built-in WP REST API
            endpoint = f"{self.wp_url}/wp-json/wp/v2/posts"

            # This could create a new post with sensor info. Or call a custom endpoint you’ve created.
            post_data = {
                "title": f"Sensor State: {entity_id}",
                "content": f"The new state is: {new_state}",
                "status": "publish"
            }

            response = requests.post(
                endpoint,
                json=post_data,
                auth=(self.wp_user, self.wp_password),
                timeout=10
            )
            response.raise_for_status()

            _LOGGER.debug("Published entity %s state to WP: %s", entity_id, response.text)
        except Exception as err:
            _LOGGER.error("Error publishing to WP: %s", err)
            raise UpdateFailed from err
