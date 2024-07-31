import streamlit as st
import sys
import requests
import folium
from streamlit_folium import folium_static
from datetime import datetime
from pathlib import Path

# Add the shared directory to the Python path
shared_dir = Path(__file__).parent.parent.parent.parent / "shared"
print(shared_dir)
sys.path.append(str(shared_dir))

# Now we can import the land_record_component
from land_record_details_panel import land_record_details_panel  # noqa

BASE_URL = "http://10.147.19.200:8000/api/landrecord/"


def fetch_record(id):
    response = requests.get(f"{BASE_URL}{id}/")
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch data for ID {id}")
        return None


def display_map(geometry):
    # Create a map centered on the property
    coordinates = geometry["coordinates"][0][0]
    center_lat = sum(coord[1] for coord in coordinates) / len(coordinates)
    center_lon = sum(coord[0] for coord in coordinates) / len(coordinates)
    m = folium.Map(location=[center_lat, center_lon], zoom_start=18)

    # Add the GeoJSON to the map
    folium.GeoJson(
        geometry, style_function=lambda x: {"fillColor": "red", "color": "black"}
    ).add_to(m)

    # Display the map
    folium_static(m)


def format_currency(amount):
    return f"${amount:,}"


def format_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d").strftime("%B %d, %Y")


css_example = """                                                                                                                                                      
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.6.0/css/all.min.css">
"""
st.write(css_example, unsafe_allow_html=True)

# Get the ID from the query parameter
id = st.query_params.get("id")

if id:
    record = fetch_record(id)
    if record:
        land_record_details_panel(record)

        # Display zoning information
        # if record["zoning"]:
        #     zoning = record["zoning"][0]  # Assuming there's only one zoning record
        #     st.write(f"Zoning: {zoning['r_code']}")
        #     st.write(
        #         f"Scheme: {zoning['scheme_name']} (Number: {zoning['scheme_number']})"
        #     )

        # # Display land sale records
        # st.write("## Land Sale History")
        # for sale in record["land_sale_records"]:
        #     st.write(f"{format_date(sale['date'])}: {format_currency(sale['amount'])}")

        # # Display the map
        # st.write("## Property Location")
        # display_map(record["geometry"])

        # # Display the full JSON data
        # with st.expander("View Full Record Data"):
        #     st.json(record)
else:
    st.write("No property ID provided. Please select a property from the main page.")

# Add a button to return to the main page
if st.button("Back to Main Page"):
    st.query_params.clear()
    st.rerun()
