import folium
from streamlit_folium import folium_static
from shapely.geometry import shape


def land_record_zoning_panel(record):
    # Create map
    property_shape = shape(record["geometry"])
    center_lat, center_lon = property_shape.centroid.y, property_shape.centroid.x
    m = folium.Map(location=[center_lat, center_lon], zoom_start=18)

    # Add zoning boundary with popup
    for zone in record["zoning"]:
        folium.GeoJson(
            zone["geometry"],
            style_function=lambda x: {
                "fillColor": "blue",
                "color": "blue",
                "weight": 2,
                "fillOpacity": 0.2,
            },
            name=f"Zoning: {zone['r_code']}",
            popup=folium.Popup(f"Zoning: {zone['r_code']}", parse_html=True),
        ).add_to(m)

    # Add property boundary with popup
    folium.GeoJson(
        record["geometry"],
        style_function=lambda x: {
            "fillColor": "red",
            "color": "red",
            "weight": 2,
            "fillOpacity": 0.5,
        },
        name="Property Boundary",
        popup=folium.Popup("Property Boundary", parse_html=True),
    ).add_to(m)

    # Add layer control
    folium.LayerControl().add_to(m)

    # Display the map
    folium_static(m)
