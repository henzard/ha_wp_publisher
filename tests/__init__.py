# tests/__init__.py

import sys
import os

# Get the root directory (assuming tests are in ha_wp_publisher/tests/)
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CUSTOM_COMPONENTS_DIR = os.path.join(ROOT_DIR, 'custom_components')

# Add custom_components to PYTHONPATH
sys.path.insert(0, CUSTOM_COMPONENTS_DIR)
