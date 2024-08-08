import folium
from streamlit_folium import folium_static
from shapely.geometry import shape


def land_record_zoning_panel(record):
    # Create map
    property_shape = shape(record["geometry"])
    center_lat, center_lon = property_shape.centroid.y, property_shape.centroid.x
    m = folium.Map(location=[center_lat, center_lon], zoom_start=18)

    # Add zoning boundary with label
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
        ).add_to(m)

        # Add permanent text label for zoning
        zone_shape = shape(zone["geometry"])
        zone_center = zone_shape.centroid
        folium.Marker(
            [zone_center.y, zone_center.x],
            icon=folium.DivIcon(
                html=f'<div style="font-size: 10pt; color: blue;"><strong>{zone["r_code"]}</strong></div>'
            ),
        ).add_to(m)

    # Add property boundary with label
    folium.GeoJson(
        record["geometry"],
        style_function=lambda x: {
            "fillColor": "red",
            "color": "red",
            "weight": 2,
            "fillOpacity": 0.5,
            "dashArray": "5, 5"  # This creates the dashed line effect
        },
        name="Property Boundary",
        tooltip=folium.Tooltip(f"{record["formatted_address"]}", permanent=False),
    ).add_to(m)

    # Add permanent text label for property
    # folium.Marker(
    #     [center_lat, center_lon],
    #     icon=folium.DivIcon(
    #         html='<div style="font-size: 12pt; color: red;">Property</div>'
    #     ),
    # ).add_to(m)

    # Add layer control
    folium.LayerControl().add_to(m)

    # Display the map
    folium_static(m)
