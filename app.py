import streamlit as st

st.set_page_config(page_title="The Spinoff Blog - Home")

# TODO: make the home link not hard coded
st.logo("_pages/images/logo/logo.png", link=None)

# Pages
home = st.Page("./_pages/home.py", title="Home", icon="🏠", url_path=None, default=True)
categories = st.Page(
    "./_pages/categories.py", title="Categories", icon="🔎", url_path=None
)
_2024_07_04 = st.Page(
    "./_pages/posts/2024_07_04/serve-up-a-streamlit-app-on-digital-ocean-20240704.py",
    title="How to host a Streamlit app on Digital Ocean - 2024-07-04",
)
_2024_07_05 = st.Page(
    "./_pages/posts/2024_07_05/value-of-land-in-cottesloe-20240705.py",
    title="Value of house+land in Cottesloe",
)
_2024_07_08 = st.Page(
    "./_pages/posts/2024_07_08/value-of-empty-blocks-in-cottesloe-20240708.py",
    title="Value of empty blocks in Cottesloe",
)
_2024_07_12 = st.Page(
    "./_pages/posts/2024_07_12/serve-meta-open-graph-tags-with-streamlit-20240712.py",
    title="Serve meta / Open Graph tags with Streamlit",
)
_2024_07_13 = st.Page(
    "./_pages/posts/2024_07_13/value-of-empty-blocks-in-peppermint-grove-20240713.py",
    title="Value of empty blocks in Peppermint Grove",
)
_2024_07_16 = st.Page(
    "./_pages/posts/2024_07_16/using-video-in-og-tags-20240716.py",
    title="Using video in og tags",
)
_2024_07_18 = st.Page(
    "./_pages/posts/2024_07_18/property-value-tracker-20240718.py",
    title="Property sales tracker",
)

# Sidebar
pages = {
    "": [home, categories],
    "Posts": [
        _2024_07_18,
        _2024_07_16,
        _2024_07_13,
        _2024_07_12,
        _2024_07_08,
        _2024_07_05,
        _2024_07_04,
    ],
}


pg = st.navigation(pages=pages)
pg.run()
