import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from spinoff_blog.shared.helpers import ordinalize_number


def land_sales_suburb_sale_curve_panel(subject_property, other_sales):
    # Extract the last sale price of the subject property
    subject_property_sales = subject_property.get("land_sale_records", [])
    if not subject_property_sales:
        st.error("No sales data available for the subject property.")
        return
    last_sale = max(subject_property_sales, key=lambda x: x["date"])
    subject_price = last_sale["amount"]
    subject_address = f"{subject_property['house_number']} {subject_property['road']}"

    # Convert other sales to DataFrame
    df = pd.DataFrame(other_sales)
    df["date"] = pd.to_datetime(df["date"])
    df["address"] = df["house_number"] + " " + df["road"]
    df["is_subject"] = False  # Explicitly set is_subject to False for all other sales

    def create_price_curve_chart(df, subject_price, subject_address):
        # Create a DataFrame for the subject property
        subject_df = pd.DataFrame(
            {
                "amount": [subject_price],
                "address": [subject_address],
                "is_subject": [True],
            }
        )

        # Combine all sales including the subject property
        all_sales = pd.concat([df, subject_df], ignore_index=True)

        # Sort by price
        all_sales = all_sales.sort_values("amount")

        # Add rank column
        all_sales["rank"] = range(1, len(all_sales) + 1)

        # Calculate percentile
        all_sales["percentile"] = all_sales["rank"] / len(all_sales) * 100

        # Create the bar chart
        fig = px.bar(
            all_sales,
            x="rank",
            y="amount",
            hover_data=["address", "percentile"],
            labels={
                "address": "Address",
                "rank": "Rank",
                "amount": "Sale Price ($)",
                "percentile": "Percentile",
            },
            title="Sales price curve",
        )

        # Highlight the subject property
        subject_data = all_sales[all_sales["is_subject"] == True]
        if not subject_data.empty:
            fig.add_trace(
                go.Bar(
                    x=[subject_data["rank"].iloc[0]],
                    y=[subject_data["amount"].iloc[0]],
                    name=f"{subject_address}",
                    marker_color="red",
                )
            )

        # Customize the layout
        fig.update_layout(
            xaxis_title="Properties (Ranked by Price)",
            yaxis_title="Sale Price ($)",
            yaxis_tickformat="$,.0f",
            showlegend=True,
        )

        return fig, subject_data.iloc[0] if not subject_data.empty else None

    # Create and display the price curve chart
    price_curve_fig, subject_row = create_price_curve_chart(
        df, subject_price, subject_address
    )
    st.plotly_chart(price_curve_fig)

    # Display subject property's position in the price curve
    # if subject_row is not None:
    #     st.write(
    #         f"Rank: {ordinalize_number(len(df) + 1 - subject_row['rank'])} most expensive out of {len(df) + 1} sales"
    #     )
    #     st.write(f"Percentile: {subject_row['percentile']:.2f}%")
