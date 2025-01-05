# HA WP Publisher

*Home Assistant integration to publish sensor data to WordPress, along with a custom Lovelace card.*

## Features
- **Config Flow UI**: Easily configure your WordPress URL, credentials, and sensor entities.
- **Customizable Post Types & Fields**: Publish to custom WordPress post types and include custom fields.
- **Expanded Templating & Formatting**: Use Jinja2 templates for post titles and content.
- **Real-Time or Scheduled Publishing**: Choose between immediate publishing on state changes or scheduled batch updates.
- **Advanced Logging & Monitoring**: Track publish status and errors via a sensor entity.
- **Custom Lovelace Card**: Visualize publish status directly on your Home Assistant dashboard.

## Installation

### 1. Install the Integration via HACS (Preferred)
1. **Add Custom Repository in HACS**:
   - Go to **HACS > Integrations > ... (3-dot menu) > Custom Repositories**.
   - Enter `https://github.com/henzard/ha_wp_publisher` as the repository URL.
   - Select **Integration** as the category.
   - Click **Add**.

2. **Install HA WP Publisher**:
   - Search for **HA WP Publisher** in **HACS > Integrations**.
   - Click **Install** and follow the prompts.
   - **Restart** Home Assistant if prompted.

3. **Configure the Integration**:
   - Navigate to **Settings > Devices & Services** in Home Assistant.
   - Click **Add Integration**, search for **HA WP Publisher**, and follow the setup steps.

### 2. Add the Custom Lovelace Card Manually
Since the Lovelace card isn't automatically managed by HACS in a combined repository, you'll need to add it manually:

1. **Upload the Lovelace Card JavaScript File**:
   - Ensure `wp_publisher_status-card.js` is placed in the `www/wp_publisher_status-card/` directory of your Home Assistant configuration.

2. **Add Lovelace Resource**:
   - Go to **Settings > Dashboards > Resources**.
   - Click **Add Resource**.
   - **URL**: `/local/wp_publisher_status-card/wp_publisher_status-card.js`
   - **Resource type**: **JavaScript Module**
   - Click **Create**.

3. **Add the Lovelace Card to Your Dashboard**:
   - Go to your desired dashboard and enter **Edit** mode.
   - Click **Add Card**.
   - Select **Manual Card**.
   - Paste the following YAML configuration:
     ```yaml
     type: 'custom:wp-publisher-status-card'
     entity: sensor.wp_publisher_status
     ```
   - Adjust the `entity` field if your sensor has a different entity ID.
   - Click **Save** to add the card to your dashboard.

## Configuration

1. **Configure the Integration**:
   - During setup, enter your WordPress URL, credentials, select sensor entities, and configure advanced options like post type and publish interval.

2. **Using Templates**:
   - Utilize Home Assistant’s Jinja2 templating within automations or scripts to customize post titles and content.

## Usage Notes

- **Authentication**:
  - For enhanced security, consider using [WordPress Application Passwords](https://wordpress.org/support/article/application-passwords/) instead of your main username/password.

- **Custom Endpoints**:
  - Modify the `coordinator.py` to publish data to custom WordPress routes or plugin endpoints if needed.

- **Templating**:
  - Combine with Home Assistant automations or scripts to generate templated post titles and content.

## Contributing

- Pull requests and suggestions are welcome.
- Please open issues for any bugs or feature requests.

## License

- [MIT License](LICENSE) – You’re free to modify and distribute.
