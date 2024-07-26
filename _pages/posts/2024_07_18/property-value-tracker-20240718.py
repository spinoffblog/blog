import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import timedelta


# Load the data
# @st.cache_data
def load_data():
    df = pd.read_csv("./_pages/data/2024_07_18/data.csv")
    df["sale_date"] = pd.to_datetime(df["sale_date"])
    # convert 'suburb' column to title case
    df["suburb"] = df["suburb"].str.title()
    # remove 'multi_lot_sale' column
    df.drop(columns=["multi_lot_sale"], inplace=True)
    return df


# round all numbers up to whole numbers
# summary = summary.applymap(lambda x: round(x, 0))
def format_currency(value):
    return f"${value:,.0f}" if pd.notnull(value) else ""


def format_area(value):
    return f"{value:,.0f} m²" if pd.notnull(value) else ""


def format_price_per_m2(value):
    if value < 1:
        return f"${value:,.2f}" if pd.notnull(value) else ""
    else:
        return f"${value:,.0f}" if pd.notnull(value) else ""


df = load_data()

max_years = (df["sale_date"].max() - df["sale_date"].min()).days // 365
suburbs = sorted(df["suburb"].unique())


# Set page title
st.markdown(
    f"""
# Property sales tracker

###### 2024/07/18

### Summary

This sales tracker has property sales data from the past {max_years} years for Cottesloe and Peppermint Grove.
"""
)

# horizontal rule
st.markdown("---")

# Suburb selection (on main page)
selected_suburb = st.selectbox("Suburb", suburbs)

property_types = ["House", "Empty block", "Strata"]

# Create a multiselect dropdown
selected_types = st.multiselect(
    "Property Type(s)",
    options=property_types,
    default=property_types,  # Optional: selects all by default
)


# dropdown to select years to analyze
year_range = range(1, max_years + 1)
years_back = st.selectbox("Years of transactions", year_range, index=max_years - 1)

# Filter data based on user inputs
end_date = df["sale_date"].max()
start_date = end_date - timedelta(days=years_back * 365)

filtered_df = df[
    (df["suburb"] == selected_suburb)
    & (df["sale_date"] >= start_date)
    & (df["property_status"].isin(selected_types))
].copy()
filtered_df["price_per_m2"] = filtered_df["sale_amount"] / filtered_df["land_area"]

# Aggregate data by quarter
quarterly_data = (
    filtered_df.groupby(pd.Grouper(key="sale_date", freq="QE"))
    .agg(
        {"sale_amount": ["count", "mean"], "land_area": "mean", "price_per_m2": "mean"}
    )
    .reset_index()
)

quarterly_data.columns = [
    "sale_date",
    "num_sales",
    "avg_sale_amount",
    "avg_land_area",
    "avg_price_per_m2",
]

# Create quarter-year labels for x-axis
quarterly_data["quarter_year"] = (
    quarterly_data["sale_date"].dt.to_period("Q").astype(str)
)

# Create and display charts
# st.header(f"Real Estate Trends in {selected_suburb}")

# Number of sales chart (interactive bar chart)
fig1 = px.bar(
    quarterly_data,
    x="quarter_year",
    y="num_sales",
    title="Quarterly sales volume",
    labels={"quarter_year": "Quarter", "num_sales": "Number of Sales"},
    hover_data=["avg_sale_amount", "avg_land_area", "avg_price_per_m2"],
)
fig1.update_xaxes(tickangle=45)
fig1.update_traces(
    hovertemplate="<br>".join(
        [
            "Quarter: %{x}",
            "Properties sold: %{y}",
            "Average sale amount: $%{customdata[0]:,.0f}",
            "Average land area: %{customdata[1]:.0f}m²",
        ]
    )
)


sales_volume_chart_container = st.empty()
with sales_volume_chart_container:
    st.plotly_chart(fig1)

# Average price per m2 chart (interactive bar chart)
fig2 = px.bar(
    quarterly_data,
    x="quarter_year",
    y="avg_price_per_m2",
    title="Average sale price per m²",
    labels={"quarter_year": "Quarter", "avg_price_per_m2": "Price per m²"},
    hover_data=["num_sales", "avg_sale_amount", "avg_land_area"],
)
fig2.update_xaxes(tickangle=45)
fig2.update_layout(
    yaxis=dict(
        tickprefix="$",
        tickformat=",",
    )
)
fig2.update_traces(
    hovertemplate="<br>".join(
        [
            "Quarter: %{x}",
            "Price per m²: $%{y:,.0f}",
            "Properties sold: %{customdata[0]}",
            "Average sale amount: $%{customdata[1]:,.0f}",
            "Average land area: %{customdata[2]:.0f}m²",
        ]
    )
)

per_m2_chart_container = st.empty()
with per_m2_chart_container:
    st.plotly_chart(fig2)

# Display summary statistics
st.header("Summary Statistics")
st.write(
    f"From records of {filtered_df.shape[0]:,.0f} properties sold in {selected_suburb} in the last {years_back} years."
)

# exclude datetime columns from summary
summary = filtered_df.select_dtypes(exclude=["datetime64"]).describe()
# exclude count row from summary
summary = summary.drop("count")


# Assuming 'df' is your summary DataFrame
summary = summary.style.format(
    {
        "sale_amount": format_currency,
        "land_area": format_area,
        "price_per_m2": format_price_per_m2,
    }
)
st.dataframe(summary)


# Display raw data
st.header("Raw Data")
styled_filtered_df = filtered_df.drop(columns=["suburb"])
styled_filtered_df["address"] = styled_filtered_df["address"].str.title()
styled_filtered_df = styled_filtered_df.sort_values(by="sale_date", ascending=False)

styled_filtered_df = styled_filtered_df[
    [
        "sale_date",
        "address",
        "sale_amount",
        "land_area",
        "price_per_m2",
        "property_status",
    ]
]

styled_filtered_df = styled_filtered_df.style.format(
    {
        "sale_amount": format_currency,
        "land_area": format_area,
        "price_per_m2": format_price_per_m2,
        "sale_date": "{:%d/%m/%Y}",
    }
)

st.dataframe(styled_filtered_df, hide_index=True)

# Add a download button for the filtered data
filtered_df["sale_date"] = filtered_df["sale_date"].dt.strftime("%Y-%m-%d %H:%M:%S")
csv = filtered_df.to_csv(index=False)
st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name=f"{selected_suburb}_real_estate_data.csv",
    mime="text/csv",
)
