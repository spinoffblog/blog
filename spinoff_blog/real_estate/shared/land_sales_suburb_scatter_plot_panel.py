import streamlit as st
import pandas as pd
import altair as alt


def land_sales_suburb_scatter_plot_panel(subject_property, other_sales):
    # Extract the last sale price of the subject property
    subject_property_sales = subject_property.get("land_sale_records", [])
    if not subject_property_sales:
        st.warning("No sales data available for the subject property.")
        return
    last_sale = max(subject_property_sales, key=lambda x: x["date"])
    subject_price = last_sale["amount"]
    subject_date = last_sale["date"]
    subject_address = (
        f"{subject_property['house_number']} {subject_property['road']}".title()
    )

    # Convert other sales to DataFrame
    df = pd.DataFrame(other_sales)
    df["date"] = pd.to_datetime(df["date"])
    df["address"] = (df["house_number"] + " " + df["road"]).str.title()
    df["amount_formatted"] = df["amount"].apply(lambda x: f"${x:,.0f}")
    df["is_subject"] = False  # Explicitly set is_subject to False for all other sales

    # Create a scatter plot of sales over time
    scatter = (
        alt.Chart(df)
        .mark_point()
        .encode(
            x=alt.X("date:T", title="Sale Date"),
            y=alt.Y("amount:Q", title="Sale Price ($)", axis=alt.Axis(format="$,.0f")),
            tooltip=["address", "amount_formatted", "date"],
        )
        .properties(title=f"{subject_property["city"].title()} Sales Over Time")
    )

    # Add the subject property as a different colored point
    subject_df = pd.DataFrame(
        [
            {
                "date": pd.to_datetime(subject_date),
                "amount": subject_price,
                "address": subject_address,
                "amount_formatted": f"${subject_price:,.0f}",
                "is_subject": True,
            }
        ]
    )
    subject_point = (
        alt.Chart(subject_df)
        .mark_point(color="red", size=100)
        .encode(
            x="date:T",
            y="amount:Q",
            tooltip=["address", "amount_formatted", "date"],
            order=alt.Order("is_subject:O", sort="descending"),
        )
    )

    # Combine the scatter plot and subject property point
    chart = scatter + subject_point


    st.write(" ")
    st.write(" ")
    # Display the chart in Streamlit
    st.altair_chart(chart, use_container_width=True)
