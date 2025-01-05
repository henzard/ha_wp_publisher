# tests/__init__.py

"""Initialize the test environment."""
import os
import sys
from pathlib import Path

# Get the root directory of the project
ROOT_DIR = Path(__file__).parent.parent.absolute()

# Add both the root directory and custom_components to the Python path
sys.path.insert(0, str(ROOT_DIR))
sys.path.insert(0, str(ROOT_DIR / "custom_components"))

# Create an empty ha_wp_publisher module if it doesn't exist
ha_wp_publisher_init = ROOT_DIR / "custom_components" / "ha_wp_publisher" / "__init__.py"
if not ha_wp_publisher_init.exists():
    ha_wp_publisher_init.touch()
