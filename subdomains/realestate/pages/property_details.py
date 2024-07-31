import streamlit as st
import sys
import requests
from datetime import datetime
from pathlib import Path

# Add the shared directory to the Python path
# TODO: make the project a proper Python project and use relative imports
shared_dir = Path(__file__).parent.parent.parent.parent / "shared"
sys.path.append(str(shared_dir))

# Now we can import the land_record_component
from land_record_details_panel import land_record_details_panel  # noqa
from land_sales_panel import land_sales_panel  # noqa
from land_sales_suburb_sale_curve_panel import (
    land_sales_suburb_sale_curve_panel,
)  # noqa
from land_sales_suburb_house_and_land_per_m2_curve_panel import (
    land_sales_suburb_house_and_land_per_m2_curve_panel,
)  # noqa
from land_sales_suburb_scatter_plot_panel import (
    land_sales_suburb_scatter_plot_panel,
)  # noqa
from land_record_zoning_panel import land_record_zoning_panel  # noqa

# TODO: make this ENV or similar
HOST = "http://localhost"
BASE_URL = f"{HOST}:8000/api/"


@st.cache_data
def fetch_record(id):
    response = requests.get(f"{BASE_URL}landrecord/{id}/")
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch data for ID {id}")
        return None


@st.cache_data
def fetch_comparison_land_sales(suburb):
    response = requests.get(
        f"{BASE_URL}suburb-latest-landsalerecord/sales-by-suburb/?suburb={suburb}"
    )
    if response.status_code == 200:
        # add dollars_per_m2 to response
        result = []
        for sale in response.json():
            sale["dollars_per_m2"] = sale["amount"] / sale["land_area"]
            result.append(sale)
        return result
    else:
        st.error(f"Failed to fetch data for suburb {suburb}")
        return None


def format_currency(amount):
    return f"${amount:,}"


def format_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d").strftime("%B %d, %Y")


# TODO: make this more cohesive and better organized
css_example = """                                                                                                                                                      
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.6.0/css/all.min.css">
"""
st.write(css_example, unsafe_allow_html=True)

# Get the ID from the query parameter
id = st.query_params.get("id")

if id:
    record = fetch_record(id)
    comparison_sales = fetch_comparison_land_sales(record["city"])
    if record:
        land_record_details_panel(record)
        land_sales_panel(record)
        land_sales_suburb_sale_curve_panel(record, comparison_sales)
        land_sales_suburb_house_and_land_per_m2_curve_panel(record, comparison_sales)
        land_sales_suburb_scatter_plot_panel(record, comparison_sales)
        land_record_zoning_panel(record)

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

        # # Display the full JSON data
        # with st.expander("View Full Record Data"):
        #     st.json(record)
else:
    st.write("No property ID provided. Please select a property from the main page.")

# Add a button to return to the main page
if st.button("Back to Main Page"):
    st.query_params.clear()
    st.rerun()
