import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


def land_sales_suburb_scatter_plot_panel(subject_property, other_sales):
    # Extract the last sale price of the subject property
    subject_property_sales = subject_property.get("land_sale_records", [])
    if not subject_property_sales:
        st.error("No sales data available for the subject property.")
        return
    last_sale = max(subject_property_sales, key=lambda x: x["date"])
    subject_price = last_sale["amount"]
    subject_date = last_sale["date"]
    subject_address = f"{subject_property['house_number']} {subject_property['road']}"

    # Convert other sales to DataFrame
    df = pd.DataFrame(other_sales)
    df["date"] = pd.to_datetime(df["date"])
    df["address"] = df["house_number"] + " " + df["road"]
    df["is_subject"] = False  # Explicitly set is_subject to False for all other sales

    # Create a scatter plot of sales over time
    fig_scatter = px.scatter(
        df,
        x="date",
        y="amount",
        hover_data=["address"],
        title="Neighborhood Sales Over Time",
    )

    # Add the subject property as a different colored point
    fig_scatter.add_trace(
        go.Scatter(
            x=[pd.to_datetime(subject_date)],
            y=[subject_price],
            mode="markers",
            marker=dict(color="red", size=10),
            name=f"{subject_address}",
            hoverinfo="text",
            hovertext=f"{subject_address}<br>${subject_price:,}<br>{subject_date}",
        )
    )

    fig_scatter.update_layout(
        xaxis_title="Sale Date", yaxis_title="Sale Price ($)", yaxis_tickformat="$,.0f"
    )

    # Display the scatter plot in Streamlit
    st.plotly_chart(fig_scatter)
