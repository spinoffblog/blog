import os
import streamlit as st
import pandas as pd
import json

from spinoff_blog.shared.helpers import get_properties


# Function to create a link to the details page
def make_clickable(id):
    return f'<a href="/property_details?id={id}" target="_self">View Details</a>'


def streamlit_page():
    filepath = os.path.abspath(__file__)
    return st.Page(
        filepath,
        title="Property List",
        icon="🏠",
        url_path=None,
        default=True,
    )


st.title("Real Estate Records")

data = get_properties()


# Extract the 'single_family' array
single_family = data["single_family"]

# Create a DataFrame
df = pd.json_normalize(
    single_family,
    record_path=None,
    meta=[
        ["properties", "description"],
        ["properties", "id"],
        ["properties", "slug"],
        ["geometry", "type"],
        ["geometry", "coordinates"],
    ],
)

# Rename columns for clarity
df = df.rename(
    columns={
        "properties.description": "description",
        "properties.id": "id",
        "properties.slug": "slug",
        "geometry.type": "geometry_type",
        "geometry.coordinates": "coordinates",
    }
)

# Split coordinates into separate latitude and longitude columns
df[["longitude", "latitude"]] = pd.DataFrame(df["coordinates"].tolist(), index=df.index)

# Drop the original coordinates column
df = df.drop("coordinates", axis=1)

# Optional: Save the DataFrame to a CSV file
# df.to_csv('single_family_data.csv', index=False)

# Add a column with clickable links
df["Details"] = df.apply(lambda row: make_clickable(row["id"]), axis=1)

# Display the DataFrame
st.write("Click on 'View Details' to see more information:")
st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)
