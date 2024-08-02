# from spinoff_blog.real_estate.property_details.property_details import (
#     run as run_property_details,
# )
import streamlit as st
from spinoff_blog.real_estate.property_list.property_list import (
    streamlit_page as property_list_page,
)
from spinoff_blog.real_estate.property_details.property_details import (
    streamlit_page as property_details_page,
)


def run():
    property_list = property_list_page()
    property_details = property_details_page()
    pg = st.navigation(pages=[property_list, property_details])
    pg.run()
