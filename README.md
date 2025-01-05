# HA WP Publisher 🚀📄

*Transform your Home Assistant sensor data into engaging WordPress posts with ease!*

![HA WP Publisher Logo](https://github.com/henzard/ha_wp_publisher/raw/main/logo.png)

## Overview 🌟

**HA WP Publisher** is a nifty Home Assistant custom integration that automatically publishes your sensor data to your WordPress site. Whether you want to blog about your home's temperature, humidity, or any other sensor magic, HA WP Publisher has got you covered!

## Features ✨

- **Seamless Integration**: Connect Home Assistant with WordPress effortlessly.
- **Customizable Post Types & Fields**: Choose how your sensor data is structured in WordPress.
- **Dynamic Templating**: Craft beautiful and informative posts using Jinja2 templates.
- **Real-Time & Scheduled Publishing**: Publish immediately on sensor changes or at set intervals.
- **Advanced Logging & Monitoring**: Keep track of your publishing activities with ease.
- **User-Friendly Config Flow**: Set up everything through Home Assistant’s intuitive UI.
- **Custom Lovelace Card**: Visualize your publishing status right on your dashboard.

## Installation 🛠️

You can install this integration using HACS. Click the button below to add it to your Home Assistant:

[![Add to HACS](https://raw.githubusercontent.com/henzard/ha_wp_publisher/main/logo.png)](https://github.com/henzard/ha_wp_publisher)

## Configuration 📝

1. **Add the Integration**:
   - Go to **Settings > Devices & Services** in Home Assistant.
   - Click **Add Integration** and search for **HA WP Publisher**.
   - Follow the setup wizard to enter your WordPress URL, credentials, and select the sensors you wish to publish.

2. **Customize Your Posts**:
   - Utilize Jinja2 templates to format your post titles and content.
   - Example:
     ```yaml
     post_title: "Current Temperature: {{ states('sensor.temperature') }}°C"
     post_content: "The temperature in the living room is now {{ states('sensor.temperature') }}°C as of {{ now().strftime('%Y-%m-%d %H:%M:%S') }}."
     ```

## Adding the Custom Lovelace Card 🎨

Since HA WP Publisher includes a custom Lovelace card for monitoring publish status, follow these steps to add it to your dashboard:

1. **Upload the Lovelace Card JavaScript File**:
   - Ensure `wp_publisher_status-card.js` is placed in the `www/wp_publisher_status-card/` directory of your Home Assistant configuration:
     ```
     /config/www/wp_publisher_status-card/wp_publisher_status-card.js
     ```

2. **Add Lovelace Resource**:
   - Go to **Settings > Dashboards > Resources**.
   - Click **Add Resource**.
   - **URL**: `/local/wp_publisher_status-card/wp_publisher_status-card.js`
   - **Resource type**: **JavaScript Module**
   - Click **Create**.

3. **Add the Card to Your Dashboard**:
   - Navigate to your desired dashboard and enter **Edit** mode.
   - Click **Add Card** and select **Manual Card**.
   - Paste the following YAML configuration:
     ```yaml
     type: 'custom:wp-publisher-status-card'
     entity: sensor.wp_publisher_status
     ```
   - Adjust the `entity` field if your sensor has a different entity ID.
   - Click **Save** to add the card to your dashboard.

## Usage Notes 🛡️

- **Authentication**:
  - For enhanced security, consider using [WordPress Application Passwords](https://wordpress.org/support/article/application-passwords/) instead of your main username/password.

- **Custom Endpoints**:
  - Modify `coordinator.py` to publish data to custom WordPress routes or plugin endpoints if needed.

- **Error Handling**:
  - HA WP Publisher gracefully handles connectivity issues by logging errors and retrying as configured.

## Unit Testing 🧪

Ensure everything runs smoothly by running the included unit tests:

1. **Navigate to the Repository**:
   ```bash
   cd ha_wp_publisher
   ```

2. **Install Dependencies**:
   ```bash
   pip install pytest pytest-homeassistant-custom
   ```

3. **Run Tests**:
   ```bash
   pytest --maxfail=1 --disable-warnings -q
   ```

## Contributing 🤝

Love HA WP Publisher and want to make it even better? Contributions are welcome!

1. **Fork the Repository**: Click the **Fork** button at the top right of [the repository](https://github.com/henzard/ha_wp_publisher).

2. **Create a Feature Branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Commit Your Changes**:
   ```bash
   git commit -m "Add awesome feature"
   ```

4. **Push to Your Fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Open a Pull Request**: Go to the original repository and click **Compare & pull request**.

## License 📝

![License](https://img.shields.io/badge/License-MIT-blue.svg)

**HA WP Publisher** is [MIT Licensed](LICENSE). Have fun, share freely, and keep the good vibes flowing!

## Documentation

For more information, visit the [documentation](https://github.com/henzard/ha_wp_publisher/blob/main/README.md).
