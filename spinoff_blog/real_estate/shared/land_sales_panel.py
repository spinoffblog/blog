import streamlit as st
import pandas as pd

from spinoff_blog.shared.helpers import format_currency


def land_sales_panel(json_data):
    # Extract land sale records from the JSON data
    land_sales = json_data.get("land_sale_records", [])

    st.write(" ")
    st.write(" ")
    st.markdown("##### Sales")

    if not land_sales:
        st.warning("No land sale records recorded.")
    else:
        # Convert to DataFrame
        df = pd.DataFrame(land_sales)

        # Format the amount column as currency
        df["amount"] = df["amount"].apply(format_currency)

        # Convert date strings to datetime objects
        df["date"] = pd.to_datetime(df["date"])

        # Sort by date
        df = df.sort_values("date")

        # Make date dd/mm/yyyy
        df["date"] = df["date"].dt.strftime("%d/%m/%Y")

        # make a copy of df with only amount and date
        for_table = df[["date", "amount"]].copy()

        st.dataframe(for_table, hide_index=True)
