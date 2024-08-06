import streamlit as st


def land_record_financials_panel(record, financial_stats):
    st.write(f"### Financials")
    st.write(
        f"##### House and land value per m²: {financial_stats['suburb_statistics']['avg_cost_per_sqm']}"
    )
    st.write(f"##### Bowl over value per m²: $---")
    st.write(f"##### Implied dwelling value: $---")
