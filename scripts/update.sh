#!/bin/bash

# Update the app and restart the Streamlit service to apply the changes
git remote update
git rebase origin/master
sudo systemctl restart streamlit.service
