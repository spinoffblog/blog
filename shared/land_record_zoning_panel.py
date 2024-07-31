import folium
from streamlit_folium import folium_static


def land_record_zoning_panel(record):
    house_geometry = record["geometry"]
    zoning_geometry = record["zoning"][0]["geometry"]
    # Create a map centered on the property
    coordinates = house_geometry["coordinates"][0][0]
    center_lat = sum(coord[1] for coord in coordinates) / len(coordinates)
    center_lon = sum(coord[0] for coord in coordinates) / len(coordinates)
    m = folium.Map(location=[center_lat, center_lon], zoom_start=18)

    # Add the GeoJSON to the map
    folium.GeoJson(
        house_geometry, style_function=lambda x: {"fillColor": "red", "color": "black"}
    ).add_to(m)

    folium.GeoJson(
        zoning_geometry,
        style_function=lambda x: {"fillColor": "blue", "color": "black"},
    ).add_to(m)
    # Display the map
    folium_static(m)
