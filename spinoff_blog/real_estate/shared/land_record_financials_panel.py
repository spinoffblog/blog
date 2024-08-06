import streamlit as st
from spinoff_blog.real_estate.shared.land_record import LandRecord


def land_record_financials_panel(record: LandRecord, financial_stats):
    st.write(f"### Financials")
    st.write(f"##### House and land value per m²: {record.formatted_cost_per_m2()}")
    st.write(f"##### Bowl over value per m²: $---")
    st.write(f"##### Implied dwelling value: $---")
