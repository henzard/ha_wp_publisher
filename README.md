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
  - Modify `coordinator.py` to publish data to a custom WP route or plugin endpoint if you don’t want to use the default REST API.
- **Templating**:  
  - Combine with Home Assistant automations or scripts to generate templated post titles and content.

## Unit Testing
This repository contains a simple test structure using **pytest** to validate the integration’s functionality (e.g., config flow).  
1. Install **pytest** and **pytest-homeassistant-custom** (or the official `pytest-homeassistant` package) in your development environment:
   ```bash
   pip install pytest pytest-homeassistant-custom
   ```
2. Create a `tests` folder at the same level as your `ha_wp_publisher` directory:
   ```
   custom_components/
   └── ha_wp_publisher/
       ├── __init__.py
       ├── manifest.json
       ├── config_flow.py
       ├── const.py
       ├── coordinator.py
   tests/
   └── test_config_flow.py
   ```
3. Example `test_config_flow.py`:
   ```python
   import pytest
   from unittest.mock import patch
   from homeassistant import config_entries, data_entry_flow
   from custom_components.ha_wp_publisher.config_flow import WPConfigFlow
   from custom_components.ha_wp_publisher.const import DOMAIN

   @pytest.mark.asyncio
   async def test_user_step(hass):
       """Test we can configure the integration via the user step."""
       flow = WPConfigFlow()
       flow.hass = hass

       # Start the config flow
       result = await flow.async_step_user(
           user_input={
               "wp_url": "https://example.com",
               "wp_user": "username",
               "wp_password": "password",
               "entities": "sensor.my_sensor"
           }
       )
       # We expect the flow to create an entry
       assert result["type"] == data_entry_flow.FlowResultType.CREATE_ENTRY
       assert result["title"] == "HA to WP Publisher"
       assert result["data"]["wp_url"] == "https://example.com"
       assert result["data"]["wp_user"] == "username"
       assert result["data"]["wp_password"] == "password"
       assert result["data"]["entities"] == "sensor.my_sensor"
   ```
4. Run tests:
   ```bash
   pytest --maxfail=1 --disable-warnings -q
   ```
   - *Adjust your command flags as needed.*  

**Tips**:
- **Mock external services** (e.g., WordPress REST API) to avoid making real network requests during tests.
- **Add more tests** for coordinator logic, error handling, etc.

## Contributing
- Pull requests and suggestions are welcome.
- Please open issues for any bugs or feature requests.

## License
- [MIT License](LICENSE) – You’re free to modify and distribute.
