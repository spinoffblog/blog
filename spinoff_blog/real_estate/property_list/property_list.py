import os
import streamlit as st
from st_keyup import st_keyup
from spinoff_blog.shared.helpers import (
    get_simple_addresses,
    fuzzy_match_address,
    slugify,
)


# Function to create a link to the details page
def make_clickable(id, value):
    slug = slugify(value)
    return f'<a href="/property_details?id={slug}" target="_self">{value["formatted_address"]}</a>'


def streamlit_page():
    filepath = os.path.abspath(__file__)
    return st.Page(
        filepath,
        title="Property List",
        icon="🏠",
        url_path=None,
        default=True,
    )


properties = get_simple_addresses()

st.title("Real Estate Records")
address = st_keyup("Search by address:", placeholder="165 Broome St")
results = fuzzy_match_address(address, properties, score_cutoff=80, limit=5)

for result in results:
    st.write(
        f"{make_clickable(result[0]['id'], result[0])}",
        unsafe_allow_html=True,
    )
