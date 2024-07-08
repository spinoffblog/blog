#!/bin/bash

# Update the app and restart the Streamlit service to apply the changes
# Get the directory of the script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Navigate to the root directory (assuming it's one level up from scripts)
cd "$SCRIPT_DIR/.."

git remote update
git rebase origin/master
source ../venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart streamlit.service
