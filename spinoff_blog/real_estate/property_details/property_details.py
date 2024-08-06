import os
import streamlit as st
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

from spinoff_blog.shared.helpers import (
    get_property,
    get_comparison_land_sales,
    get_financial_data,
)


def format_currency(amount):
    return f"${amount:,}"


def format_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d").strftime("%B %d, %Y")


def streamlit_page():
    filepath = os.path.abspath(__file__)
    return st.Page(
        filepath,
        title="Property Details",
        icon=None,
        url_path=None,
        default=False,
    )


# TODO: perhaps put FA in the header for all pages
css_example = """                                                                                                                                                      
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.6.0/css/all.min.css">
"""
st.write(css_example, unsafe_allow_html=True)

# Get the ID from the query parameter
id = st.query_params.get("id")

if id:
    record = get_property(id)
    comparison_sales = get_comparison_land_sales(record["city"])
    financial_stats = get_financial_data(id)
    if record:
        land_record_details_panel.land_record_details_panel(record)
        land_sales_panel.land_sales_panel(record)
        land_record_financials_panel.land_record_financials_panel(
            record, financial_stats
        )
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
    st.write("No property ID provided. Please select a property from the main page.")

# Add a button to return to the main page
if st.button("Back to Main Page"):
    st.query_params.clear()
    st.rerun()
