import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
from statistics import mean


def flatten_coordinates(coords):
    """Flatten potentially nested coordinate lists"""
    flattened = []
    for item in coords:
        if isinstance(item[0], (int, float)):
            flattened.append(item)
        else:
            flattened.extend(flatten_coordinates(item))
    return flattened


def get_center_coordinates(coordinates):
    """Helper function to get center coordinates of a geometry"""
    flat_coords = flatten_coordinates(coordinates)
    lats = [coord[1] for coord in flat_coords]
    lons = [coord[0] for coord in flat_coords]
    return mean(lats), mean(lons)


def land_record_zoning_panel(record):
    house_geometry = record["geometry"]
    zoning_data = record["zoning"][0]

    # Get center coordinates for the house
    center_lat, center_lon = get_center_coordinates(house_geometry["coordinates"])

    # Create a map centered on the property
    m = folium.Map(location=[center_lat, center_lon], zoom_start=18)

    # Add the house GeoJSON to the map
    folium.GeoJson(
        house_geometry, style_function=lambda x: {"fillColor": "red", "color": "black"}
    ).add_to(m)

    # Add the zoning GeoJSON to the map
    folium.GeoJson(
        zoning_data["geometry"],
        style_function=lambda x: {"fillColor": "blue", "color": "black"},
    ).add_to(m)

    # Create a MarkerCluster for better performance with multiple markers
    marker_cluster = MarkerCluster().add_to(m)

    # Add marker with tooltip for the house
    folium.Marker(
        [center_lat, center_lon],
        tooltip=folium.Tooltip(f"Property boundary", permanent=True),
    ).add_to(marker_cluster)

    # Get center coordinates for the zoning
    zoning_center_lat, zoning_center_lon = get_center_coordinates(
        zoning_data["geometry"]["coordinates"]
    )

    # Add marker with tooltip for the zoning
    folium.Marker(
        [zoning_center_lat, zoning_center_lon],
        tooltip=folium.Tooltip(f"Zoning Code: {zoning_data['r_code']}", permanent=True),
    ).add_to(marker_cluster)

    # Display the map
    folium_static(m)
