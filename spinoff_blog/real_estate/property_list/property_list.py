import os
import streamlit as st
from st_keyup import st_keyup
from spinoff_blog.shared.helpers import get_properties, fuzzy_match_address


# Function to create a link to the details page
def make_clickable(id, address):
    return f'<a href="/property_details?id={id}" target="_self">{address}</a>'


def streamlit_page():
    filepath = os.path.abspath(__file__)
    return st.Page(
        filepath,
        title="Property List",
        icon="🏠",
        url_path=None,
        default=True,
    )


properties = get_properties()
# get single_family.properties.description from properties
# properties = [property["formatted_address"] for property in properties]

st.title("Real Estate Records")

address = st_keyup("Search by address:", placeholder="165 Broome St")
results = fuzzy_match_address(address, properties, score_cutoff=80, limit=5)
print(results)

for result in results:
    st.write(
        f"{make_clickable(result[0]['id'], result[0]['formatted_address'])}",
        unsafe_allow_html=True,
    )
