import os
from datetime import datetime
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
# sort listings by "first_seen" datetime
listings.sort(key=lambda x: x["first_seen"], reverse=True)

st.title("Real Estate Listings")

for listing in listings:
    st.markdown("---")
    # parse first_seen datetime, e.g. "first_seen": "2024-08-13T00:00:00Z"
    date = datetime.fromisoformat(listing["first_seen"][:-1])

    # get date dd/mm/yyyy from first_seen datetime
    date = date.strftime("%d/%m/%Y")
    st.write(f"**{date}**")
    link = make_clickable(
        listing["address"]["id"], listing["address"]["formatted_address"]
    )
    st.write(link, unsafe_allow_html=True)
    st.write(listing["price_words"])
