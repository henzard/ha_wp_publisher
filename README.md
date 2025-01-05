# HA WP Publisher

*Home Assistant custom integration to publish sensor data to WordPress.*

## Overview
- Publishes sensor state changes automatically to a WordPress REST endpoint
- Uses Home Assistant’s **Config Flow** to manage WordPress credentials and sensor selections
- Can be installed via [HACS](https://hacs.xyz/) or manually copied into `custom_components/`

## Features
- **Config Flow UI**: Easily configure your WordPress URL, credentials, and sensor entities
- **Dynamic Updates**: Automatically publishes sensor state changes in real time
- **Customizable**: Use your own WordPress endpoints or the default REST API (`wp-json/wp/v2/posts`)

## Installation

### 1. HACS (Preferred)
1. Add this repository as a *Custom Repository* in HACS:
   - *HACS > Integrations > ... (3-dot menu) > Custom Repositories*
   - Paste the GitHub URL, select *Integration*, and click *Add*.
2. Search for *“HA WP Publisher”* in HACS Integrations and click *Install*.
3. **Restart** Home Assistant.

### 2. Manual Installation
1. Download or clone this repository.
2. Copy the `ha_wp_publisher` folder into your `custom_components` directory, so you have:
   ```
   custom_components/
   └── ha_wp_publisher/
       ├── __init__.py
       ├── manifest.json
       ├── config_flow.py
       ├── const.py
       ├── coordinator.py
   ```
3. **Restart** Home Assistant.

## Configuration
1. Go to **Settings > Devices & Services** in Home Assistant.
2. Click **Add Integration** and search for *“HA WP Publisher”*.
3. In the setup form (Config Flow):
   - Enter your WordPress URL (e.g., `https://example.com`).
   - Enter your WordPress credentials (username and password, or application password).
   - Select the sensor entities you want to publish.
4. Click **Finish**. Now the integration will post updates whenever the selected sensors change state.

## Usage Notes
- **Authentication**:  
  - If you prefer, use [WordPress Application Passwords](https://wordpress.org/support/article/application-passwords/) for more secure integration.
- **Custom Endpoints**:  
  - Feel free to modify `coordinator.py` to publish data to a custom WP route or plugin endpoint.
- **Templating**:  
  - Combine with Home Assistant automations or scripts to generate templated post titles and content.

## Contributing
- Pull requests and suggestions are welcome.
- Please open issues for any bugs or feature requests.

## License
- [MIT License](LICENSE) – You’re free to modify and distribute.
