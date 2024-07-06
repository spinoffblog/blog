import streamlit as st

section_1 = """
# Set up Streamlit to run on Digital Ocean

###### 2024/07/04

### Background

[Streamlit](https://streamlit.io) helps you quickly and easily turn Python scripts and data apps into shareable web apps.  This post will show you how to set up a Streamlit app on a Digital Ocean droplet so you can share your app with the world.

### Start your Streamlit app locally

Make a development directory:
```shellSession
mkdir my_streamlit_app && cd my_streamlit_app
```

Add a Python `.gitignore` file:
```shellSession
wget https://raw.githubusercontent.com/github/gitignore/main/Python.gitignore -O .gitignore
```

Create a Git repo:
```shellSession
git init
```

Create a virtual environment:
```shellSession
python -m venv ./venv
source venv/bin/activate
```

Install Streamlit and Watchdog:
```shellSession
pip install streamlit
pip install watchdog
pip freeze > requirements.txt
```

Add a "Hello World" app post:
```shellSession
echo "import streamlit as st

st.title('Hello, Streamlit!')
st.write('This is a test app.')" > ./app.py
```

Test the Streamlit app is working:
```shellSession
streamlit run ./app.py
```

Your browser should automatically open to your Streamlit app.  If it doesn't automatically open, navigate to the "Local" URL which is shown in your console.  You should see output in your console similar to the following:
```shellSession

  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.189.6:8501
```

Stop the app in your console with `CTRL+c`

Save your work as a Git commit:
```shellSession
git add . && git commit -m "First streamlit commit"
```

Make a repo for your app on GitHub.  Ensure you set it to "public" and do not check the box with "Add a README file".  It should look like the following:
"""

section_2 = """
Push your repo to your new remote:
```shellSession
git remote add origin https://github.com/<YOUR_GITHUB_USERNAME>/my_streamlit_app.git
git branch -M main
git push -u origin main
```

Make sure to keep the url for `https://github.com/<YOUR_GITHUB_USERNAME>/my_streamlit_app.git` somewhere handy, you'll need it in a bit.

Now you'll get your Streamlit app working on Digital Ocean

### Set up remote Digital Ocean host

In your [Digital Ocean new droplet screen](https://cloud.digitalocean.com/droplets/new) create a new Ubuntu droplet.  Choose your authentication method, making sure to save the details of whichever method you choose.

Navigate to the dashboard for your droplet and click the `Console` button:
"""

section_3 = """
Install `pip` so you can install Streamlit and other Python programs.
```shellSession
apt install python3-pip
apt install python3.12-venv
```

Make the necessary user:
```shellSession
sudo adduser streamlit_user
```

Navigate to the directory for your streamlit app and clone it from GitHub, while setting necessary permissions:
```shellSession
cd /opt
mkdir my_streamlit_app
sudo chown streamlit_user:streamlit_user /opt/my_streamlit_app
```


Create the necesssary Python environment and clone and setup your Streamlit app
```shellSession
sudo su - streamlit_user
cd /opt/my_streamlit_app
git clone https://github.com/<YOUR_GITHUB_USERNAME>/my_streamlit_app.git .
sudo chown -R streamlit_user:streamlit_user /opt/my_streamlit_app
python3 -m venv ./venv
source venv/bin/activate
pip install -r ./requirements.txt
```

Test your app works:
```shellSession
streamlit run app.py
```

Your output should look like the below.  Try navigating to the URL which is shown as `External URL`.  Note that the IP address in your instance will be different.  Keep the IP address for your server handy, you'll need it in a bit:
```shellSession
(venv) streamlit_user@ubuntu-s-1vcpu-512mb-10gb-nyc1-01:/opt/my_streamlit_app$ streamlit run ./app.py 

Collecting usage statistics. To deactivate, set browser.gatherUsageStats to false.


  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://100.227.100.127:8501
  External URL: http://100.227.100.127:8501
```

Exit the app with `CTRL+c`

Exit the `streamlit_user` session:
```shellSession
exit
```

Create the `.service` file to run Streamlit in the background as a service using [`systemd`](https://en.wikipedia.org/wiki/Systemd).
```shellSession
sudo nano /etc/systemd/system/streamlit.service
```

Add the following as the contents of your service file:
```
[Unit]
Description=Streamlit App
After=network.target

[Service]
User=streamlit_user
WorkingDirectory=/opt/my_streamlit_app
ExecStart=/opt/my_streamlit_app/venv/bin/streamlit run app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Save and close the file (in nano, press Ctrl+X, then Y, then Enter)

Reload `systemd`, start the Streamlit service, and enable the service to start on boot:
```shellSession
sudo systemctl daemon-reload
sudo systemctl start streamlit
sudo systemctl enable streamlit
```

Check the status of your service:
```shellSession
sudo systemctl status streamlit
```

Now to take care of [`nginx`](https://en.wikipedia.org/wiki/nginx) which will sit between the internet and the Streamlit application on your droplet.

Install nginx if not already installed:
```shellSession
sudo apt update
sudo apt install nginx
```

And create an `nginx` config file for your Streamlit app:
```shellSession
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
```shellSession
sudo ln -s /etc/nginx/sites-available/streamlit /etc/nginx/sites-enabled
```

Test the nginx configuration:
```shellSession
sudo nginx -t
```

If the test is successful, restart nginx:
```shellSession
sudo systemctl restart nginx
```

Create the systemd service file for nginx (if it doesn't already exist):
```shellSession
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
```shellSession
sudo rm /etc/nginx/sites-enabled/default
```

Reload `systemd` and enable required services:
```shellSession
sudo systemctl daemon-reload
sudo systemctl start nginx
sudo systemctl enable nginx
sudo systemctl start streamlit
```

Wait for a few seconds and restart nginx:
```shellSession
sudo systemctl restart nginx
```

In your web browser, navigate to the IP address you saved earlier.  You should see your Streamlit app running!
"""

section_4 = """

You can also view the status of the nginx and Streamlit services:
```shellSession
sudo systemctl status nginx
sudo systemctl status streamlit
```

### Conclusion
The page you are reading now is a Streamlit app running on a Digital Ocean droplet following the above instructions.  You can see the source code for this app on [GitHub](https://github.com/spinoffblog/blog).

### Next steps
- Setting your own custom domain for the site
- Using subdomains for different Streamlit apps
- Making a basic deploy script so you can develop locally and deploy with one command


### Feedback
Is always welcomed.  Please raise an issue at the [GitHub for this app](https://github.com/spinoffblog/blog/issues) with any suggestions or changes.
"""


st.markdown(section_1)
st.image("_pages/images/2024_07_04/_2024_07_04_01.png")
st.markdown(section_2)
st.image("_pages/images/2024_07_04/_2024_07_04_02.png")
st.markdown(section_3)
st.image("_pages/images/2024_07_04/_2024_07_04_03.png")
st.markdown(section_4)
