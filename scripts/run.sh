#!/bin/bash

# This script needs to technically run from the project root

# Get the directory of the script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Navigate to the root directory (assuming it's one level up from scripts)
cd "$SCRIPT_DIR/.."

# Run the application
python -m streamlit run app.py
