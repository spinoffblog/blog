import streamlit as st

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
    title="Value of land in Cottesloe",
)

# Sidebar
pages = {"": [home, categories], "Posts": [_2024_07_05, _2024_07_04]}


pg = st.navigation(pages=pages)
pg.run()
