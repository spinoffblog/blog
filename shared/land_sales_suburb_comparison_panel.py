import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


def land_sales_suburb_comparison_panel(subject_property, other_sales):
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

    # Create the histogram
    fig = go.Figure()

    # Add histogram for neighborhood sales
    fig.add_trace(
        go.Histogram(
            x=df["amount"],
            nbinsx=50,
            name="Neighborhood Sales",
            marker_color="blue",
            opacity=0.7,
        )
    )

    # Add a vertical line for the subject property
    fig.add_trace(
        go.Scatter(
            x=[subject_price, subject_price],
            y=[0, df["amount"].value_counts().max()],
            mode="lines",
            name="Subject Property",
            line=dict(color="red", width=2, dash="dash"),
        )
    )

    # Customize the layout
    fig.update_layout(
        title="Comparison of Subject Property Sale Price with Neighborhood Sales",
        xaxis_title="Sale Price ($)",
        yaxis_title="Number of Sales",
        bargap=0.1,
        showlegend=True,
    )

    # Add annotations
    fig.add_annotation(
        x=subject_price,
        y=df["amount"].value_counts().max(),
        text=f"Subject Property: ${subject_price:,}<br>{subject_address}<br>Date: {subject_date}",
        showarrow=True,
        arrowhead=2,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="red",
        font=dict(size=12, color="red"),
        align="center",
        yshift=10,
    )

    # Display the histogram in Streamlit
    st.plotly_chart(fig)

    # Display summary statistics
    st.write("Summary Statistics:")
    stats = df["amount"].describe()
    st.write(f"Median Neighborhood Sale Price: ${stats['50%']:,.0f}")
    st.write(f"Mean Neighborhood Sale Price: ${stats['mean']:,.0f}")
    st.write(f"Subject Property Sale Price: ${subject_price:,}")

    percentile = (df["amount"] < subject_price).mean() * 100
    st.write(
        f"Subject Property is in the {percentile:.1f}th percentile of neighborhood sales."
    )

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
            name="Subject Property",
            hoverinfo="text",
            hovertext=f"Subject Property<br>{subject_address}<br>${subject_price:,}<br>{subject_date}",
        )
    )

    fig_scatter.update_layout(
        xaxis_title="Sale Date", yaxis_title="Sale Price ($)", yaxis_tickformat="$,.0f"
    )

    # Display the scatter plot in Streamlit
    st.plotly_chart(fig_scatter)

    # Create a price curve table

    def create_price_curve_chart(df, subject_price, subject_address):
        # Combine all sales including the subject property
        all_sales = df.copy()
        all_sales = pd.concat(
            [
                all_sales,
                pd.DataFrame(
                    {
                        "amount": [subject_price],
                        "address": [subject_address],
                        "is_subject": [True],
                    }
                ),
            ],
            ignore_index=True,
        )

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
                "rank": "Rank",
                "amount": "Sale Price ($)",
                "percentile": "Percentile",
            },
            title="Price Curve: Neighborhood Sales",
        )

        # Highlight the subject property
        subject_index = all_sales[all_sales["is_subject"]].index[0]
        fig.add_trace(
            go.Bar(
                x=[all_sales.loc[subject_index, "rank"]],
                y=[all_sales.loc[subject_index, "amount"]],
                name="Subject Property",
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

        return fig, all_sales[all_sales["is_subject"]].iloc[0]

    # Create and display the price curve chart
    price_curve_fig, subject_row = create_price_curve_chart(
        df, subject_price, subject_address
    )
    st.plotly_chart(price_curve_fig)

    # Display subject property's position in the price curve
    st.write(f"Subject Property Position:")
    st.write(f"Rank: {subject_row['rank']} out of {len(df) + 1}")
    st.write(f"Percentile: {subject_row['percentile']:.2f}%")


# Example usage (commented out as it's part of the component, not the main app)
# import json
#
# # Load JSON data (replace this with how you actually get the JSON data)
# with open('subject_property.json', 'r') as file:
#     subject_property = json.load(file)
#
# with open('other_sales.json', 'r') as file:
#     other_sales = json.load(file)
#
# neighborhood_sales_comparison(subject_property, other_sales)
