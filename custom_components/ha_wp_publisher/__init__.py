"""
Init file for the ha_wp_publisher integration.
Sets up config entries, coordinator, and optional real-time state listeners.
"""

import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.const import EVENT_STATE_CHANGED

from .const import DOMAIN, CONF_PUBLISH_INTERVAL
from .coordinator import WordPressPublisherCoordinator

# If you have a sensor platform to display publish status, add "sensor" here.
PLATFORMS = ["sensor"]

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """
    Set up the ha_wp_publisher integration from a config entry.
    """
    _LOGGER.debug("Setting up ha_wp_publisher for entry_id=%s", entry.entry_id)

    # Initialize and store the coordinator
    coordinator = WordPressPublisherCoordinator(hass, entry.data)

    # If there's a non-zero update interval, DataUpdateCoordinator will handle scheduled updates
    # We'll still do the initial refresh to set up any needed data structures.
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    # If publish_interval is 0 or None, we rely on real-time triggers (state_changed events)
    interval = entry.data.get(CONF_PUBLISH_INTERVAL, 0)
    if not interval or interval <= 0:
        _LOGGER.debug("Publish interval is 0 (real-time). Setting up state_changed listener.")

        @callback
        def _state_listener(event):
            entity_id = event.data.get("entity_id")
            new_state_obj = event.data.get("new_state")
            if not new_state_obj:
                return  # State is None (e.g., entity got removed)
            # Check if the changed entity is one the user wants to publish
            if entity_id in coordinator.entities:
                new_state = new_state_obj.state
                # Publish asynchronously (don't block the event loop)
                hass.async_create_task(coordinator.async_publish_state(entity_id, new_state))

        # Listen for all state changes in HA, then filter by coordinator.entities
        hass.bus.async_listen(EVENT_STATE_CHANGED, _state_listener)

    # Forward the entry setup to any platforms (like sensor) you might have
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """
    Handle removal of a config entry.
    Unload platforms and remove references to the coordinator.
    """
    _LOGGER.debug("Unloading ha_wp_publisher entry_id=%s", entry.entry_id)

    # Unload the platforms first
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        coordinator = hass.data[DOMAIN].pop(entry.entry_id, None)
        if coordinator is not None:
            # Perform any coordinator-related cleanup if needed
            _LOGGER.debug("Coordinator cleaned up for entry_id=%s", entry.entry_id)

    return unload_ok
