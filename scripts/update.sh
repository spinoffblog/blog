#!/bin/bash

# Update the app and restart the Streamlit service to apply the changes
git remote update
git rebase origin/master
source ../venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart streamlit.service
