import streamlit as st

home = st.Page("./_pages/home.py", title="Home", icon="🏠", url_path=None, default=True)
_2024_07_04 = st.Page(
    "./_pages/posts/2024_07_04/set-up-streamlit-as-a-blog-on-digital-ocean-20240704.py",
    title="How to make a Streamlit blog on Digital Ocean - 2024-07-04",
)

pages = {"": [home], "Posts": [_2024_07_04]}

pg = st.navigation(pages=pages)
pg.run()
