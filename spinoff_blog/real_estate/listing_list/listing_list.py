import os
import streamlit as st
from spinoff_blog.shared.helpers import get_listings


# Function to create a link to the details page
def make_clickable(id, value):
    return f'<a href="/property_details?id={id}" target="_self">{value}</a>'


def streamlit_page():
    filepath = os.path.abspath(__file__)
    return st.Page(
        filepath,
        title="Listings List",
        icon="💵",
        url_path=None,
        default=True,
    )


listings = get_listings()

st.title("Real Estate Listings")

for listing in listings:
    link = make_clickable(
        listing["address"]["id"], listing["address"]["formatted_address"]
    )
    st.write(link, unsafe_allow_html=True)
    st.write(listing["price_words"])
    # horizontal line
    st.markdown("---")
