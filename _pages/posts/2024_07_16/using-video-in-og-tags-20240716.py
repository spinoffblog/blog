import streamlit as st

st.markdown(
    f"""
# Using video in og tags

###### 2024/07/16

### Summary

You need to use the `og:video:secure_url`, `og:image`, and `og:video:type` og tags to use a video in your og tags.

"""
)

"""

### Example of the html with og tags for this page:

```html
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
    <title>Using video in og tags</title>
    <script>window.prerenderReady = !1</script>
    <script defer="defer" src="./static/js/main.7994a814.js"></script>
    <link href="./static/css/main.3aaaea00.css" rel="stylesheet" />
    <meta content="Using video in og tags" property="og:title" />
    <meta content="" property="og:description" />
    <meta content="" property="og:type" />
    <meta content="https://spinoff.blog/using-video-in-og-tags-20240716" property="og:url" />
    <meta content="https://spinoff.blog/media/images/using-video-in-og-tags-20240716.jpg" property="og:image" />
    <meta content="https://spinoff.blog/media/video/using-video-in-og-tags-20240716.mp4"
        property="og:video:secure_url" />
    <meta content="video/mp4" property="og:video:type" />
    <meta content="The Spinoff Blog" property="og:site_name" />
    <meta content="" name="twitter:card" />
    <meta content="" name="twitter:site" />
    <meta content="" name="twitter:creator" />
</head>

<body><noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
</body>

</html>
```

### Conclusion
Enjoy!

"""
