# In subdomain.py
import streamlit as st
from spinoff_blog.real_estate.property_details.property_details import (
    run as run_property_details,
)


def run():
    st.title("Real estate")
    run_property_details()
