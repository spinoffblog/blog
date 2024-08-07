import streamlit as st
import plotly.express as px
import pandas as pd


def land_sales_suburb_house_and_land_per_m2_curve_panel(subject_property, other_sales):
    # Extract the last sale price of the subject property
    subject_property_sales = subject_property.get("land_sale_records", [])
    if not subject_property_sales:
        st.error("No sales data available for the subject property.")
        return

    last_sale = max(subject_property_sales, key=lambda x: x["date"])
    subject_price = last_sale["amount"]
    subject_address = f"{subject_property['house_number']} {subject_property['road']}"
    subject_dollars_per_m2 = subject_price / subject_property["land_area"]

    # Convert other sales to DataFrame
    df = pd.DataFrame(other_sales)
    df["date"] = pd.to_datetime(df["date"])
    df["address"] = df["house_number"] + " " + df["road"]
    df["dollars_per_m2"] = df["amount"] / df["land_area"]

    def create_price_curve_chart(df, subject_price, subject_address):
        # Create a DataFrame for the subject property
        subject_df = pd.DataFrame(
            {
                "dollars_per_m2": [subject_dollars_per_m2],
                "address": [subject_address],
            }
        )

        # Combine all sales including the subject property
        all_sales = pd.concat([df, subject_df], ignore_index=True)
        all_sales = all_sales.sort_values("dollars_per_m2")
        all_sales["rank"] = range(1, len(all_sales) + 1)
        all_sales["percentile"] = all_sales["rank"] / len(all_sales) * 100

        # Create the bar chart
        fig = px.bar(
            all_sales,
            x="rank",
            y="dollars_per_m2",
            hover_data=["address", "percentile"],
            labels={
                "address": "Address",
                "rank": "Rank",
                "dollars_per_m2": "Price per m² ($)",
                "percentile": "Percentile",
            },
            title=f"{subject_property["city"].title()} per m² curve",
            color_discrete_sequence=["#1E90FF"] * len(all_sales),
        )

        # Find the subject property's position
        subject_row = all_sales[all_sales["address"] == subject_address].iloc[0]
        subject_rank = subject_row["rank"]
        subject_price_per_m2 = subject_row["dollars_per_m2"]

        # Add an arrow annotation for the subject property
        fig.add_annotation(
            x=subject_rank,
            y=subject_price_per_m2,
            text=f"{subject_address}<br>Rank: {subject_rank}/{len(all_sales)}<br>Price per m²: ${subject_price_per_m2:,.0f}<br>Percentile: {subject_row['percentile']:.1f}%",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor="red",
            align="left",
            xanchor="right",
            yanchor="middle",
            bgcolor="white",
            bordercolor="red",
            borderwidth=2,
        )

        # Highlight the subject property bar in red
        fig.update_traces(
            marker_color=[
                "red" if r == subject_rank else "#1E90FF" for r in all_sales["rank"]
            ]
        )

        # Customize the layout
        fig.update_layout(
            xaxis_title="Properties (Ranked by Price per m²)",
            yaxis_title="Sale Price per m² ($)",
            yaxis_tickformat="$,.0f",
            showlegend=False,  # Hide the legend as it's not needed
        )

        return fig, subject_row

    # Create and display the price curve chart
    price_curve_fig, subject_row = create_price_curve_chart(
        df, subject_price, subject_address
    )
    st.plotly_chart(price_curve_fig)
