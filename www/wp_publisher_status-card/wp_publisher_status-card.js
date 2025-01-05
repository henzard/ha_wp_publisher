class WpPublisherStatusCard extends HTMLElement {
  set hass(hass) {
    // If we haven't created content yet, build the basic card structure
    if (!this.content) {
      this.innerHTML = `
        <ha-card header="WP Publisher Status">
          <div class="card-content" id="cardContent">Loading...</div>
        </ha-card>
      `;
      this.content = this.querySelector("#cardContent");
    }

    // Grab the entity from the card config
    const entityId = this.config.entity;
    const stateObj = hass.states[entityId];

    if (!stateObj) {
      this.content.innerHTML = `Entity '${entityId}' not found.`;
      return;
    }

    // Build the display string
    const stateDisplay = stateObj.state;  // "idle", "ok", or "error"
    const attrs = stateObj.attributes;
    const lastEntity = attrs.last_published_entity || "None";
    const lastTime = attrs.last_published_time || "Unknown";
    const lastError = attrs.last_publish_error || "None";

    this.content.innerHTML = `
      <p><strong>Status:</strong> ${stateDisplay}</p>
      <p><strong>Last Published Entity:</strong> ${lastEntity}</p>
      <p><strong>Last Published Time:</strong> ${lastTime}</p>
      <p><strong>Last Error:</strong> ${lastError}</p>
    `;
  }

  setConfig(config) {
    // Basic validation: check that we have an entity in the config
    if (!config.entity) {
      throw new Error("You must define an entity in the card config");
    }
    this.config = config;
  }

  getCardSize() {
    // Helps Lovelace figure out how much space the card might take
    return 2;
  }
}

// Define the custom element so HA can use it
customElements.define("wp-publisher-status-card", WpPublisherStatusCard);
