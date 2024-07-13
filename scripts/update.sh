#!/bin/bash

# Update the app and restart the Streamlit service to apply the changes

# if the git repository is not clean, exit
if [ -n "$(git status --porcelain)" ]; then
    echo "The git repository is not clean. Please commit your changes before updating."
    exit 1
fi

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
