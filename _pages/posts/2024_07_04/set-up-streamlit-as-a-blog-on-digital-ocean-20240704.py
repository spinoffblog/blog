import streamlit as st

section_1 = """
# Set up Streamlit to run as a blog on Digital Ocean

#### 2024/07/04

## Start your Streamlit blog locally

Make a development directory:
```bash
mkdir my_streamlit_blog && cd my_streamlit_blog
```

Add a Python `.gitignore` file:
```bash
wget https://raw.githubusercontent.com/github/gitignore/main/Python.gitignore -O .gitignore
```

Create a Git repo:
```bash
git init
```

Create a virtual environment:
```bash
python -m venv ./venv
source venv/bin/activate
```

Install Streamlit and Watchdog:
```bash
pip install streamlit
pip install watchdog
pip freeze > requirements.txt
```

Add a "Hello World" blog post:
```bash
echo "import streamlit as st

st.title('Hello, Streamlit!')
st.write('This is a test app.')" > ./app.py
```

Test the Streamlit app is working:
```bash
streamlit run ./app.py
```

Your browser should automatically open to your Streamlit app.  If it doesn't automatically open, navigate to the "Local" URL which is shown in your console.  You should see output in your console similar to the following:
```bash

  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.189.6:8501
```

Stop the app in your console with `CTRL+c`

Save your work as a Git commit:
```bash
git add . && git commit -m "First streamlit commit"
```

Make a repo for your blog on GitHub.  Ensure you set it to "public" and do not check the box with "Add a README file".  It should look like the following:
"""

section_2 = """
Push your repo to your new remote:
```bash
git remote add origin https://github.com/<YOUR_GITHUB_USERNAME>/my_streamlit_blog.git
git branch -M main
git push -u origin main
```

Make sure to keep the url for `https://github.com/<YOUR_GITHUB_USERNAME>/my_streamlit_blog.git` somewhere handy, you'll need it in a bit.

Now you'll get your Streamlit blog working on Digital Ocean

## Set up remote Digital Ocean host

In your [Digital Ocean new droplet screen](https://cloud.digitalocean.com/droplets/new) create a new Ubuntu droplet.  Choose your authentication method, making sure to save the details of whichever method you choose.

Navigate to the dashboard for your droplet and click the `Console` button:
"""

section_3 = """
Install `pip` so you can install Streamlit and other Python programs.
```bash
apt install python3-pip
apt install python3.12-venv
```

Make the necessary user:
```bash
sudo adduser streamlit_user
```

Navigate to the directory for your streamlit blog and clone it from GitHub, while setting necessary permissions:
```bash
cd /opt
mkdir my_streamlit_blog
sudo chown streamlit_user:streamlit_user /opt/my_streamlit_blog
```


Create the necesssary Python environment and clone and setup your Streamlit app
```bash
sudo su - streamlit_user
cd /opt/my_streamlit_blog
git clone https://github.com/<YOUR_GITHUB_USERNAME>/my_streamlit_blog.git .
python3 -m venv ./venv
source venv/bin/activate
pip install -r ./requirements.txt
```

Test your app works:
```bash
streamlit run app.py
```

Your output should look like the below.  Try navigating to the URL which is shown as `External URL`.  Note that the IP address in your instance will be different.  Keep the IP address for your server handy, you'll need it in a bit:
```bash
(venv) streamlit_user@ubuntu-s-1vcpu-512mb-10gb-nyc1-01:/opt/my_streamlit_blog$ streamlit run ./app.py 

Collecting usage statistics. To deactivate, set browser.gatherUsageStats to false.


  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://100.227.100.127:8501
  External URL: http://100.227.100.127:8501
```

Exit the app with `CTRL+c`

Exit the `streamlit_user` session:
```bash
exit
```

Create the `.service` file to run Streamlit in the background as a service using [`systemd`](https://en.wikipedia.org/wiki/Systemd).
```bash
sudo nano /etc/systemd/system/streamlit.service
```

Add the following as the contents of your service file:
```
[Unit]
Description=Streamlit App
After=network.target

[Service]
User=streamlit_user
WorkingDirectory=/opt/my_streamlit_blog
ExecStart=/opt/my_streamlit_blog/venv/bin/streamlit run app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Save and close the file (in nano, press Ctrl+X, then Y, then Enter)

Reload `systemd`, start the Streamlit service, and enable the service to start on boot:
```bash
sudo systemctl daemon-reload
sudo systemctl start streamlit
sudo systemctl enable streamlit
```

Check the status of your service:
```bash
sudo systemctl status streamlit
```

Now to take care of [`nginx`](https://en.wikipedia.org/wiki/nginx) which will sit between the internet and the Streamlit application on your droplet.

Install nginx if not already installed:
```bash
sudo apt update
sudo apt install nginx
```

And create an `nginx` config file for your Streamlit app:
```bash
sudo nano /etc/nginx/sites-available/streamlit
```

Add the following as contents of the file:
```
server {
    listen 80;
    server_name <YOUR_SERVER_IP>;  # Replace with your server IP you saved earlier, not using the port, just the IP

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

Save and close the file (in nano, press Ctrl+X, then Y, then Enter)

Create a symlink to enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/streamlit /etc/nginx/sites-enabled
```

Test the nginx configuration:
```bash
sudo nginx -t
```

If the test is successful, restart nginx:
```bash
sudo systemctl restart nginx
```

Create the systemd service file for nginx (if it doesn't already exist):
```bash
sudo nano /etc/systemd/system/nginx.service
```

Add the following as contents of the file:

```
[Unit]
Description=nginx - high performance web server
Documentation=https://nginx.org/en/docs/
After=network-online.target remote-fs.target nss-lookup.target
Wants=network-online.target

[Service]
Type=forking
PIDFile=/run/nginx.pid
ExecStartPre=/usr/sbin/nginx -t -q -g 'daemon on; master_process on;'
ExecStart=/usr/sbin/nginx -g 'daemon on; master_process on;'
ExecReload=/usr/sbin/nginx -g 'daemon on; master_process on;' -s reload
ExecStop=/bin/kill -s QUIT $MAINPID
TimeoutStopSec=5
KillMode=mixed
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

Save and close the file.

Delete the default nginx configuration:
```bash
sudo rm /etc/nginx/sites-enabled/default
```

Reload `systemd` and enable required services:
```bash
sudo systemctl daemon-reload
sudo systemctl start nginx
sudo systemctl enable nginx
sudo systemctl start streamlit
```

Wait for a few seconds and restart nginx:
```bash
sudo systemctl restart nginx
```

In your web browser, navigate to the IP address you saved earlier.  You should see your Streamlit app running!
"""

section_4 = """

You can also view the status of the nginx and Streamlit services:
```bash
sudo systemctl status nginx
sudo systemctl status streamlit
```

## Next steps
- Setting your own custom domain for the site
- Using subdomains for different Streamlit apps
- Making a basic deploy script so you can develop locally and deploy with one command


## Feedback
Is always welcomed.  Please raise an issue at the [GitHub for this blog](https://github.com/spinoffblog/blog/issues) with any suggestions or changes.
"""

st.markdown(section_1)
st.image('./_pages/images/2024_07_04/_2024_07_04_01.png')
st.markdown(section_2)
st.image('./_pages/images/2024_07_04/_2024_07_04_02.png')
st.markdown(section_3)
st.image('./_pages/images/2024_07_04/_2024_07_04_03.png')
st.markdown(section_4)
