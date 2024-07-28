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
rm -rf output/*
python og_tag_generator.py
cp output/* /var/www/spinoff/static_html/
cd -

echo "Copying files to /var/www/spinoff/..."
echo "Current directory: $(pwd)"

# Copy all .jpg files to /var/www/spinoff/media/images/
find ../_pages -type f -name "*.jpg" -exec cp -v --update=none {} /var/www/spinoff/media/images/ \;
# Copy all .mp4 files to /var/www/spinoff/media/video/
find ../_pages -type f -name "*.mp4" -exec cp -v --update=none {} /var/www/spinoff/media/video/ \;

sudo chmod 755 /var/www/spinoff/ && sudo chown -R www-data:www-data /var/www/spinoff/

sudo systemctl restart streamlit.service
sudo systemctl restart real_estate_streamlit.service

echo "Cleaning up git repository..."
git clean -f

exit 0
