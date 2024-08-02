import streamlit as st
import requests
from datetime import datetime

from spinoff_blog.real_estate.shared import (
    land_record_details_panel,
    land_record_financials_panel,
    land_record_zoning_panel,
    land_sales_panel,
    land_sales_suburb_house_and_land_per_m2_curve_panel,
    land_sales_suburb_sale_curve_panel,
    land_sales_suburb_scatter_plot_panel,
)


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


def run():
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
            land_record_details_panel.land_record_details_panel(record)
            land_sales_panel.land_sales_panel(record)
            land_record_financials_panel.land_record_financials_panel(record)
            land_sales_suburb_sale_curve_panel.land_sales_suburb_sale_curve_panel(
                record, comparison_sales
            )
            land_sales_suburb_house_and_land_per_m2_curve_panel.land_sales_suburb_house_and_land_per_m2_curve_panel(
                record, comparison_sales
            )
            land_sales_suburb_scatter_plot_panel.land_sales_suburb_scatter_plot_panel(
                record, comparison_sales
            )
            land_record_zoning_panel.land_record_zoning_panel(record)
    else:
        st.write(
            "No property ID provided. Please select a property from the main page."
        )

    # Add a button to return to the main page
    if st.button("Back to Main Page"):
        st.query_params.clear()
        st.rerun()
