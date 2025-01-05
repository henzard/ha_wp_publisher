"""
sensor.py for ha_wp_publisher
Defines a sensor entity that shows the current publish status and details.
"""

import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

SENSOR_NAME = "WP Publisher Status"


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """
    Set up the WP Publisher sensor from a config entry.
    """
    coordinator = hass.data[DOMAIN][entry.entry_id]

    # Create and add the status sensor
    status_sensor = WordPressPublisherStatusSensor(coordinator, entry)
    async_add_entities([status_sensor], update_before_add=False)


class WordPressPublisherStatusSensor(CoordinatorEntity, SensorEntity):
    """
    A sensor to track the last publish status and related info:
    - Sensor state: "idle", "ok", or "error"
    - Attributes:
        * last_published_entity
        * last_published_time
        * last_publish_error
    """

    _attr_has_entity_name = True  # Use this if you want HA to group it by integration name

    def __init__(self, coordinator, entry: ConfigEntry):
        """
        Initialize the status sensor.
        """
        super().__init__(coordinator)
        self._entry = entry
        self._attr_name = SENSOR_NAME
        # Unique ID helps HA track this entity distinctly
        self._attr_unique_id = f"{entry.entry_id}_wp_publisher_status"

    @property
    def state(self):
        """
        Return the main state of the sensor.
        Could be "idle", "ok", or "error", based on the last publish attempt.
        """
        info = self.coordinator.last_publish_info
        if not info["last_published_entity"]:
            return "idle"  # Nothing published yet

        if info["last_publish_error"]:
            return "error"

        return "ok"

    @property
    def extra_state_attributes(self):
        """
        Return additional details about the last publish attempt.
        """
        info = self.coordinator.last_publish_info
        return {
            "last_published_entity": info.get("last_published_entity"),
            "last_published_time": str(info.get("last_published_time")) 
                                   if info.get("last_published_time") else None,
            "last_publish_error": info.get("last_publish_error"),
        }

    @callback
    def _handle_coordinator_update(self) -> None:
        """
        Called by the CoordinatorEntity base class when data is updated.
        We just need to tell HA our state changed.
        """
        self.async_write_ha_state()

    @property
    def icon(self):
        """
        Optional: Return an icon based on the sensor state.
        """
        state = self.state
        if state == "ok":
            return "mdi:check-circle"
        elif state == "error":
            return "mdi:alert-circle"
        return "mdi:information"

    @property
    def device_info(self):
        """
        Optional: Provide device info to group the sensor under a device in HA.
        """
        return {
            "identifiers": {(DOMAIN, self._entry.entry_id)},
            "name": "WP Publisher Integration",
            "manufacturer": "ha_wp_publisher",
        }
