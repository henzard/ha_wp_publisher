"""
Config flow for ha_wp_publisher integration.
"""
import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.selector import (
    EntitySelector,
    EntitySelectorConfig,
    Selector
)

DOMAIN = "ha_wp_publisher"

CONF_WP_URL = "wp_url"
CONF_WP_USER = "wp_user"
CONF_WP_PASSWORD = "wp_password"

CONF_POST_TYPE = "post_type"
CONF_CUSTOM_FIELDS = "custom_fields"
CONF_PUBLISH_INTERVAL = "publish_interval"

CONF_ENTITIES = "entities"

_LOGGER = logging.getLogger(__name__)

# Step 1 schema: Basic WP credentials
STEP_USER_DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_WP_URL, default=""): str,
    vol.Required(CONF_WP_USER, default=""): str,
    vol.Required(CONF_WP_PASSWORD, default=""): str,
})

# Step 2 schema: Advanced options (could be optional or required)
STEP_ADVANCED_DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_POST_TYPE, default="posts"): str,
    vol.Optional(CONF_CUSTOM_FIELDS, default=""): str,
    vol.Optional(CONF_PUBLISH_INTERVAL, default=0): vol.Coerce(int),
    # 0 or negative means "no scheduled interval" (real-time)
})

# Step 3 schema: Sensor selection
# This example uses a single multi-entity selector for demonstration.
STEP_SENSOR_DATA_SCHEMA = vol.Schema({
    vol.Optional(CONF_ENTITIES): Selector(
        EntitySelector(
            EntitySelectorConfig(
                domain=["sensor"],  # Only sensors
                multiple=True       # Let user pick multiple sensors
            )
        )
    )
})


class WPConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for the ha_wp_publisher integration."""
    VERSION = 2

    def __init__(self):
        """Initialize the flow."""
        self._data = {}

    async def async_step_user(self, user_input=None):
        """
        Step 1: Collect basic WordPress credentials (URL, user, password).
        """
        if user_input is not None:
            # Store data from this step
            self._data.update(user_input)
            # Proceed to the advanced config step
            return await self.async_step_advanced()

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
        )

    async def async_step_advanced(self, user_input=None):
        """
        Step 2: Advanced options like post type, custom fields, publish interval.
        """
        if user_input is not None:
            self._data.update(user_input)
            # Proceed to sensor selection
            return await self.async_step_sensors()

        return self.async_show_form(
            step_id="advanced",
            data_schema=STEP_ADVANCED_DATA_SCHEMA,
        )

    async def async_step_sensors(self, user_input=None):
        """
        Step 3: Let the user select which sensor entities to track.
        """
        errors = {}
        if user_input is not None:
            self._data.update(user_input)

            # Create the config entry with all stored data
            return self.async_create_entry(
                title="HA to WP Publisher",
                data=self._data
            )

        return self.async_show_form(
            step_id="sensors",
            data_schema=STEP_SENSOR_DATA_SCHEMA,
            errors=errors
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """
        If you want to allow editing the config after creation,
        you can return an instance of an OptionsFlow here.
        """
        return WPOptionsFlow(config_entry)


class WPOptionsFlow(config_entries.OptionsFlow):
    """
    Optional: Let users edit some settings later from the UI
    (e.g., changing intervals, custom fields, or sensor selection).
    """
    def __init__(self, config_entry):
        self.config_entry = config_entry
        self._options = dict(config_entry.options)

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            self._options.update(user_input)
            return self.async_create_entry(title="", data=self._options)

        # Example: Let user edit the publish interval in options
        options_schema = vol.Schema({
            vol.Optional(
                CONF_PUBLISH_INTERVAL,
                default=self._options.get(CONF_PUBLISH_INTERVAL, 0)
            ): vol.Coerce(int)
        })

        return self.async_show_form(
            step_id="init",
            data_schema=options_schema
        )
