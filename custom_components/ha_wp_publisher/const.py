"""
Constants for the ha_wp_publisher integration.
"""

DOMAIN = "ha_wp_publisher"

# Config Flow / Entry Data Keys
CONF_WP_URL = "wp_url"
CONF_WP_USER = "wp_user"
CONF_WP_PASSWORD = "wp_password"
CONF_POST_TYPE = "post_type"
CONF_CUSTOM_FIELDS = "custom_fields"
CONF_PUBLISH_INTERVAL = "publish_interval"
CONF_ENTITIES = "entities"

# List of platforms this integration provides:
PLATFORMS = ["sensor"]
