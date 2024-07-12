#!/bin/bash

# Update the app and restart the Streamlit service to apply the changes

git remote update
git rebase origin/master
source ../venv/bin/activate
pip install -r ../requirements.txt

cd og_tag_generator
python og_tag_generator.py
cp output/* /var/www/spinoff/static_html/
sudo chmod 755 /var/www/spinoff/ && sudo chown -R www-data:www-data /var/www/spinoff/

cd -
sudo systemctl restart streamlit.service
