# WP Publisher Status Card

A custom Lovelace card to display the status of the **ha_wp_publisher** integration.

## Installation

1. Copy `wp_publisher_status-card.js` into your Home Assistant `www/wp_publisher_status-card/` folder.  
2. In Home Assistant, go to **Settings > Dashboards** > **Resources** > Add resource:
   - URL: `/local/wp_publisher_status-card/wp_publisher_status-card.js`
   - Resource type: **JavaScript Module**
3. Add a manual card to your Lovelace UI:
   ```yaml
   type: 'custom:wp-publisher-status-card'
   entity: sensor.wp_publisher_status
