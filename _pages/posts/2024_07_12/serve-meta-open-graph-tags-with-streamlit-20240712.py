import streamlit as st

previous_post_url = "serve-up-a-streamlit-app-on-digital-ocean-20240704"

section_1 = f"""
# Serve meta / Open Graph tags with Streamlit

###### 2024/07/12

### Background

Streamlit is super useful for creating data visualizations and interactive web apps. However, it doesn't provide a way to serve meta tags for Open Graph (OG) and Twitter cards. This is important for sharing your app on social media platforms like Twitter, Facebook, and LinkedIn.

This post will show you how to use nginx to serve meta tags for Open Graph and Twitter cards with Streamlit.

It builds on a previous post, [How to host a Streamlit app on Digital Ocean](./{previous_post_url}).

### Summary

You'll generate the meta tags using a yaml template and a python script, which will create static html files.  The static html files with the tags will be served by nginx.

### Prerequisites

Check out the previous post, [How to host a Streamlit app on Digital Ocean](./{previous_post_url}), to set up your server.

### nginx

Edit your nginx configuration to serve static html files.  You will recall fromt the previous post that the config is located at `/etc/nginx/sites-available/streamlit`.

```shellSession
sudo nano /etc/nginx/sites-available/streamlit
```

You can use the following configuration:
"""

config = """
server {
    listen 80;
    server_name spinoff.blog;
    root /var/www/spinoff;
    index index.html;

    location = / {
        try_files /static_html/index.html @fallback;
    }

    location /media/ {
        alias /var/www/spinoff/media/;
        try_files $uri $uri/ @fallback;
    }

    location / {
        try_files /static_html/$uri.html @fallback;
    }

    location @fallback {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
"""

section_2 = """
The configuration file is set up to check the `/static_html` directory for static html files.  If it doesn't find one, it will proxy the request to the Streamlit app.

The static html files contain the meta tags for Open Graph and Twitter cards.  These need to be pre-generated and served statically so they can be crawled.

How to generate these files will be discussed later in the post.

Save the configuration file using `Ctrl + O` and exit using `Ctrl + X`.

Now test your nginx configuration:
    
```shellSession
sudo nginx -t
```

And if it's successful, reload nginx:
    
```shellSession
sudo systemctl reload nginx
```

Now - change user to `www-data` and create the `/var/www/spinoff/static_html` directory:
        
```shellSession
sudo su -l www-data -s /bin/bash
mkdir /var/www/spinoff/static_html
```

(thanks to https://askubuntu.com/a/948488 for the tip on changing user to `www-data`).

Next, create your `index.html` file in the `/var/www/spinoff/static_html` directory.  You can copy the initial template from your Streamlit app's `index.html` file.

In my case it looks like this, from my Streamlit app's project directory:
```shellSession
cp venv/lib/<YOUR_PYTHON_VERSION>/site-packages/streamlit/static/index.html /var/www/spinoff/static_html/index.html
```

Now edit your `index.html` file to include the meta tags for Open Graph and Twitter cards.

```shellSession
nano /var/www/spinoff/static_html/index.html
```

Here's an example of the `index.html` for this site - `spinoff.blog`:
"""

index_html = """
<!DOCTYPE html>

<html lang="en">

<head>
    <meta charset="utf-8" />
    <meta content="width=device-width,initial-scale=1,shrink-to-fit=no" name="viewport" />
    <link href="./favicon.png" rel="shortcut icon" />
    <link as="font" crossorigin="" href="./static/media/SourceSansPro-Regular.0d69e5ff5e92ac64a0c9.woff2" rel="preload"
        type="font/woff2" />
    <link as="font" crossorigin="" href="./static/media/SourceSansPro-SemiBold.abed79cd0df1827e18cf.woff2" rel="preload"
        type="font/woff2" />
    <link as="font" crossorigin="" href="./static/media/SourceSansPro-Bold.118dea98980e20a81ced.woff2" rel="preload"
        type="font/woff2" />
    <title>The Spinoff Blog - Home</title>
    <script>window.prerenderReady = !1</script>
    <script defer="defer" src="./static/js/main.7994a814.js"></script>
    <link href="./static/css/main.3aaaea00.css" rel="stylesheet" />
    <meta content="The Spinoff Blog - Home" property="og:title" />
    <meta content="" property="og:description" />
    <meta content="" property="og:type" />
    <meta content="" property="og:url" />
    <meta content="https://spinoff.blog/media/images/home.png" property="og:image" />
    <meta content="" property="og:site_name" />
    <meta content="" name="twitter:card" />
    <meta content="" name="twitter:site" />
    <meta content="" name="twitter:creator" />
</head>

<body><noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
</body>

</html>
"""

section_3 = """
Save the file using `Ctrl + O` and exit using `Ctrl + X`.

Now generate html files for each of your Streamlit app's pages.  Give the files the same name as their corresponding Streamlit app's page.

e.g. on this site for the page `https://spinoff.blog/serve-up-a-streamlit-app-on-digital-ocean-20240704`, the html file is `/var/www/spinoff/serve-up-a-streamlit-app-on-digital-ocean-20240704.html`.

```shellSession
nano /var/www/spinoff/serve-up-a-streamlit-app-on-digital-ocean-20240704.html
```

An example of the html file for this page is:
"""

individual_page_html = """
<!DOCTYPE html>

<html lang="en">

<head>
    <meta charset="utf-8" />
    <meta content="width=device-width,initial-scale=1,shrink-to-fit=no" name="viewport" />
    <link href="./favicon.png" rel="shortcut icon" />
    <link as="font" crossorigin="" href="./static/media/SourceSansPro-Regular.0d69e5ff5e92ac64a0c9.woff2" rel="preload"
        type="font/woff2" />
    <link as="font" crossorigin="" href="./static/media/SourceSansPro-SemiBold.abed79cd0df1827e18cf.woff2" rel="preload"
        type="font/woff2" />
    <link as="font" crossorigin="" href="./static/media/SourceSansPro-Bold.118dea98980e20a81ced.woff2" rel="preload"
        type="font/woff2" />
    <title>Serve up a Streamlit app on your own Digital Ocean server</title>
    <script>window.prerenderReady = !1</script>
    <script defer="defer" src="./static/js/main.7994a814.js"></script>
    <link href="./static/css/main.3aaaea00.css" rel="stylesheet" />
    <meta content="Serve up a Streamlit app on your own Digital Ocean server" property="og:title" />
    <meta content="" property="og:description" />
    <meta content="" property="og:type" />
    <meta content="" property="og:url" />
    <meta content="https://spinoff.blog/media/images/serve-up-a-streamlit-app-on-digital-ocean-20240704.jpg"
        property="og:image" />
    <meta content="" property="og:site_name" />
    <meta content="" name="twitter:card" />
    <meta content="" name="twitter:site" />
    <meta content="" name="twitter:creator" />
</head>

<body><noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
</body>

</html>
"""

section_4 = """
### Python script
In order to simplify the process of generating the html files, you can use a python script.  This script will read yaml files containing the meta tags for each of your Streamlit pages and generate the html files.

You can see an example of the script [here](https://github.com/spinoffblog/blog/blob/master/scripts/og_tag_generator/og_tag_generator.py).

By placing a file named `meta.yaml` in the same directory as each of your Streamlit pages, you can generate static html files with the required meta tags.

An example of the `meta.yaml` file for this current page is:
"""

meta_yaml = """
# Blog post meta information
title: "Serve meta / Open Graph tags with Streamlit"
description: ""
author: ""
date: ""

# Open Graph meta tags
og:
  title: "Serve meta / Open Graph tags with Streamlit"
  description: ""
  type: ""
  url: ""
  image: "https://spinoff.blog/media/images/serve-meta-open-graph-tags-with-streamlit-20240712.jpg"
  site_name: ""

# Twitter Card meta tags
twitter:
  card: ""
  site: ""
  creator: ""

# Additional meta tags
keywords:
  - 
  - 
  - 
  -
"""

section_5 = """
You can also create a directory for static media files, such as images, and serve them from nginx.  This will allow you to include images in your meta tags.

```shellSession
mkdir /var/www/spinoff/media
mkdir /var/www/spinoff/media/images
```
You can see images for this site are being served from `https://spinoff.blog/media/images/` - e.g. `https://spinoff.blog/media/images/serve-meta-open-graph-tags-with-streamlit-20240712.jpg` and these images are used in the above `meta.yaml` file.
"""

conclusion = """
### Conclusion
nginx is great as a reverse proxy for serving static html files with meta tags for Open Graph and Twitter cards.  It's a bit of effort, but it's worth it for the improved sharing experience on social media platforms and chat apps like iMessage etc.
"""

st.markdown(section_1)
st.code(config, language="nginx", line_numbers=True)
st.markdown(section_2)
st.code(index_html, language="html", line_numbers=True)
st.markdown(section_3)
st.code(individual_page_html, language="html", line_numbers=True)
st.markdown(section_4)
st.code(meta_yaml, language="yaml", line_numbers=True)
st.markdown(section_5)
st.markdown(conclusion)
