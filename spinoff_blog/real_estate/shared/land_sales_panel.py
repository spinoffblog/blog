import streamlit as st
import pandas as pd

from spinoff_blog.shared.helpers import format_currency


def land_sales_panel(json_data):
    # Extract land sale records from the JSON data
    land_sales = json_data.get("land_sale_records", [])

    if not land_sales:
        st.warning("No land sale records recorded.")
        return

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
    for_table = df[["amount", "date"]].copy()

    st.write(" ")
    st.write(" ")
    st.markdown("##### Sales")
    st.dataframe(for_table, hide_index=True)

    # Create the Plotly Express scatter plot with line
    #
    # fig = px.scatter(
    #     df,
    #     x="date",
    #     y="amount",
    #     title="Sales history",
    #     labels={"date": "Sale Date", "amount": "Sale Amount ($)"},
    #     hover_data={"date": "|%B %d, %Y", "amount": ":$,.0f"},
    # )

    # # Add line connecting points
    # fig.add_scatter(x=df["date"], y=df["amount"], mode="lines", showlegend=False)

    # # Customize the chart
    # fig.update_traces(marker=dict(size=12))
    # fig.update_layout(
    #     xaxis_title="Sale Date",
    #     yaxis_title="Sale Amount ($)",
    #     yaxis_tickformat="$,.0f",
    #     hovermode="x unified",
    # )

    # # Display the chart in Streamlit
    # st.plotly_chart(fig)

    # Example usage (commented out as it's part of the component, not the main app)
    # import json
    #
    # # Load JSON data (replace this with how you actually get the JSON data)
    # with open('land_data.json', 'r') as file:
    #     json_data = json.load(file)
    #
    # land_sales_chart_component(json_data)
