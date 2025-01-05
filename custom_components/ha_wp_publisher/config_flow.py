import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.selector import (
    EntitySelector,
    EntitySelectorConfig,
    Selector
)

from .const import DOMAIN, CONF_WP_URL, CONF_WP_USER, CONF_WP_PASSWORD, CONF_ENTITIES

_LOGGER = logging.getLogger(__name__)

class WPConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """WordPress Publisher config flow."""

    VERSION = 1

    def __init__(self):
        self._wp_url = None
        self._wp_user = None
        self._wp_password = None
        self._entities = []

    async def async_step_user(self, user_input=None):
        """Initial step where the user sets WP credentials and selects sensors."""
        errors = {}

        if user_input is not None:
            self._wp_url = user_input[CONF_WP_URL]
            self._wp_user = user_input[CONF_WP_USER]
            self._wp_password = user_input[CONF_WP_PASSWORD]
            self._entities = user_input[CONF_ENTITIES]

            # Optionally, you could validate the WP credentials here
            # For brevity, we skip validation
            return self.async_create_entry(
                title="HA to WP Publisher",
                data={
                    CONF_WP_URL: self._wp_url,
                    CONF_WP_USER: self._wp_user,
                    CONF_WP_PASSWORD: self._wp_password,
                    CONF_ENTITIES: self._entities,
                }
            )

        entity_selector = EntitySelector(EntitySelectorConfig(domain=["sensor"]))
        data_schema = {
            vol.Required(CONF_WP_URL): str,
            vol.Required(CONF_WP_USER): str,
            vol.Required(CONF_WP_PASSWORD): str,
            vol.Optional(CONF_ENTITIES): Selector(entity_selector),
        }

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(data_schema),
            errors=errors
        )
