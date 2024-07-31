import streamlit as st
import folium
from streamlit_folium import folium_static

# Sample GeoJSON data (a simple polygon)
geojson_data = {
    "type": "Feature",
    "properties": {
        "name": "Sample Area",
        "description": "This is a sample polygon area.",
    },
    "geometry": {
        "type": "Polygon",
        "coordinates": [
            [
                [-122.4194, 37.7749],
                [-122.4094, 37.7749],
                [-122.4094, 37.7649],
                [-122.4194, 37.7649],
                [-122.4194, 37.7749],
            ]
        ],
    },
}


def main():
    # st.set_page_config(page_title="Spinoff - Real Estate")
    st.set_page_config(page_title="Data manager", page_icon=":material/edit:")

    # add "/subdomains/realestate/property_list.py" page
    property_list = st.Page(
        "./subdomains/realestate/pages/property_list.py",
        title="Property List",
        icon="🏠",
        url_path=None,
        default=True,
    )
    property_details = st.Page(
        "./subdomains/realestate/pages/property_details.py",
        title="Property Details",
        icon=None,
        url_path=None,
        default=False,
    )
    pg = st.navigation(pages=[property_list, property_details])
    pg.run()

    # # Create a map centered on the GeoJSON coordinates
    # m = folium.Map(location=[37.7749, -122.4194], zoom_start=12)

    # # Function to create popup content
    # def create_popup(feature):
    #     return folium.Popup(
    #         f"Name: {feature['properties']['name']}<br>"
    #         f"Description: {feature['properties']['description']}",
    #         max_width=300,
    #     )

    # # Add the GeoJSON data to the map with popup
    # folium.GeoJson(
    #     geojson_data,
    #     name="geojson",
    #     style_function=lambda feature: {
    #         "fillColor": "blue",
    #         "color": "black",
    #         "weight": 2,
    #         "fillOpacity": 0.3,
    #     },
    #     popup=create_popup(geojson_data),
    # ).add_to(m)

    # # Display the map
    # folium_static(m)


if __name__ == "__main__":
    main()
