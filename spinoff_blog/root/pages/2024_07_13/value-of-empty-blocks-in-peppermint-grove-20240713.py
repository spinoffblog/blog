from datetime import datetime, timedelta
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from matplotlib.ticker import MaxNLocator


df = pd.read_csv("spinoff_blog/root/data/2024_07_13/pg_real_estate.csv")

# filter df for dates only in the past 96 months
# Calculate the date 48 months ago from today
cutoff_date = datetime.now() - timedelta(days=365 * 4)  # Approximate 96 months

# Filter the DataFrame
df["sale_date"] = pd.to_datetime(df["sale_date"], errors="coerce")
df = df[df["sale_date"] > cutoff_date]

# Format the dates in dd/mm/yyyy
df["sale_date"] = df["sale_date"].dt.strftime("%Y/%m/%d")

# delete column 'multi_lot_sale'
df = df.drop(columns=["multi_lot_sale"])

df["dollars_per_m2"] = df["sale_amount"] / df["land_area"]

# order by sale_date
df = df.sort_values(by="sale_date", ascending=False)

# Calculate the average cost per m²
# sum the sale_amount and land_area columns and divide
average_cost_per_m2 = df["sale_amount"].sum() / df["land_area"].sum()
total_sales = df["sale_amount"].sum()
total_land = df["land_area"].sum()
earliest_sale_date = df["sale_date"].min()
latest_sale_date = df["sale_date"].max()

previous_post_url = "/value-of-empty-blocks-in-cottesloe-20240708"
st.markdown(
    f"""
# Value of empty residential blocks in Peppermint Grove

###### 2024/07/13

### Background

Building from a <a href="{previous_post_url}" target="_self">previous post</a> which analysed the value of empty residential blocks in Cottesloe, this post will focus on the value of empty residential blocks in Peppermint Grove.

The key focus will be on the question "What was the average price of of **empty** residential land in Peppermint Grove over the past 8 years?".

The post will be updated with sales data as it becomes available.  Check back for updates.
""",
    unsafe_allow_html=True,
)
st.image(
    "https://spinoff.blog/media/images/value-of-empty-blocks-in-peppermint-grove-20240713.jpg",
    caption="Peppermint Grove, Western Australia",
)

"""
### Summary
"""
st.metric(
    "Average Peppermint Grove vacant land cost per m²",
    f"${average_cost_per_m2:,.0f}",
)

st.markdown(
    f"""

There have only been {df.shape[0]} empty residential blocks sold in Peppermint Grove in the past 8 years, with the earliest sale on {earliest_sale_date} and the most recent sale on {latest_sale_date}.
    
The average cost per m² in Peppermint Grove for vacant residential housing land in the past 8 years was :blue-background[\\${average_cost_per_m2:,.0f}].

The total sales amount was :blue-background[\\${total_sales:,.0f}] and the total land area sold was :blue-background[{total_land:,.0f} m²].

The lowest cost per m² was :blue-background[{df['address'][df['dollars_per_m2'].idxmin()].title()}] with a cost of :blue-background[\\${df['dollars_per_m2'].min():,.0f}] per m².

The highest cost per m² was :blue-background[{df['address'][df['dollars_per_m2'].idxmax()].title()}] with a cost of :blue-background[\\${df['dollars_per_m2'].max():,.0f}] per m².

#### Initial raw data
"""
)

styled_df = df.style.format(
    {
        "sale_amount": "${:,.0f}",
        "dollars_per_m2": "${:,.0f}",
        "land_area": "{:,.0f} m²",
        "address": lambda x: x.title(),  # This line formats 'address' to title case
    }
)
st.dataframe(styled_df, hide_index=True)

# Check if df is a proper DataFrame
if not isinstance(df, pd.DataFrame):
    st.warning(
        "Error: 'df' is not a pandas DataFrame. Please check your data loading process."
    )
    st.stop()

# Check if required columns exist
required_columns = ["sale_amount", "land_area", "dollars_per_m2"]
missing_columns = [col for col in required_columns if col not in df.columns]
if missing_columns:
    st.warning(
        f"Error: The following required columns are missing from the DataFrame: {', '.join(missing_columns)}"
    )
    st.stop()


# Function to create histogram with Seaborn
def create_histogram(data, column):
    fig, ax = plt.subplots(figsize=(12, 6))

    # Create the histogram using Seaborn
    sns.histplot(data=data, x=column, kde=True, ax=ax)

    # Format x-axis labels
    if column in ["sale_amount", "dollars_per_m2"]:
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"${x:,.0f}"))
    else:
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"{x:,.0f}"))

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha="right")

    ax.yaxis.set_major_locator(MaxNLocator(integer=True))

    ax.set_title(
        f"Distribution of {column.replace('_', ' ').title()} for Peppermint Grove residential land sales ({earliest_sale_date} to {latest_sale_date})"
    )
    ax.set_xlabel(column.replace("_", " ").title())
    ax.set_ylabel("Count")

    # Adjust layout to prevent cutting off labels
    plt.tight_layout()

    return fig


# Create and display the histograms
for column in required_columns:
    st.markdown(f"#### {column.replace('_', ' ').title()} Distribution")
    fig = create_histogram(df, column)
    st.pyplot(fig)
