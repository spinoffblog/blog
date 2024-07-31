import streamlit as st
import pandas as pd


# Function to create a link to the details page
def make_clickable(id):
    return f'<a href="/property_details?id={id}" target="_self">View Details</a>'


st.title("Real Estate Records")

# Create a sample DataFrame (you would typically load this from a database or API)
data = {
    "address": ["16 Grant St", "18 Grant St", "2 Ozone Parade"],
    "id": [12607, 12608, 12609],
}
df = pd.DataFrame(data)

# Add a column with clickable links
df["Details"] = df.apply(lambda row: make_clickable(row["id"]), axis=1)

# Display the DataFrame
st.write("Click on 'View Details' to see more information:")
st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)
