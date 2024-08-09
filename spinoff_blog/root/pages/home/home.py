import streamlit as st
import os


def streamlit_page():
    filepath = os.path.abspath(__file__)
    return st.Page(filepath, title="Home", icon="🏠", url_path=None, default=True)


st.title("The Spinoff Blog")
st.write("Home page")
