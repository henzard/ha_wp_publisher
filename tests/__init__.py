# tests/__init__.py

"""Initialize the test environment."""
import os
import sys
from pathlib import Path

# Get the root directory of the project
ROOT_DIR = Path(__file__).parent.parent.absolute()

# Add the custom_components directory to the Python path
CUSTOM_COMPONENTS_DIR = os.path.join(ROOT_DIR, "custom_components")
sys.path.insert(0, str(CUSTOM_COMPONENTS_DIR))
