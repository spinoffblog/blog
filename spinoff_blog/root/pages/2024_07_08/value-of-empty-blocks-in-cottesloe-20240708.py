import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from datetime import datetime, timedelta

# Data processing
#
truncation_size = 100
year_of_focus = 2024
truncation_amount = 100000

df = pd.read_csv("./_pages/data/2024_07_08/cott_real_estate.csv")
df = df.drop_duplicates(subset=["address", "sale_amount", "sale_date"], keep="first")
# make "address" title case
df["address"] = df["address"].str.title()
truncated_df = df
filtered_df = truncated_df
filtered_array = filtered_df["sale_amount"].to_numpy()

# Calculate $ per m2 for each row and convert to numpy array
df_columns_dropped = filtered_df.drop(columns=["multi_lot_sale"])

df_columns_dropped["dollars_per_m2"] = (
    df_columns_dropped["sale_amount"] / df_columns_dropped["land_area"]
).round()
df_columns_dropped["dollars_per_m2"] = df_columns_dropped["dollars_per_m2"].astype(int)
df_columns_dropped["land_area"] = df_columns_dropped["land_area"].astype(int)
dollars_per_m2_array = (
    df_columns_dropped["sale_amount"] / df_columns_dropped["land_area"]
).to_numpy()


# Get the date 12 months ago from today
twelve_months_ago = datetime.now().date() - timedelta(days=1461)
df_columns_dropped["sale_date"] = pd.to_datetime(df_columns_dropped["sale_date"])
# Remove time component, keeping only the date
df_columns_dropped['sale_date'] = df_columns_dropped['sale_date'].dt.date

# Filter the DataFrame
df_truncated_sales = df_columns_dropped[
    df_columns_dropped["sale_date"] > twelve_months_ago
]
df_truncated_sales = df_truncated_sales[df_truncated_sales["dollars_per_m2"] > 500]

average_per_m2_in_past_48_months = df_truncated_sales["dollars_per_m2"].mean()
total_sales_in_past_year = df_truncated_sales.shape[0]

# Chart processing
fig, ax, n, bins, patches = None, None, None, None, None
fig2, ax2, n2, bins2, patches2 = None, None, None, None, None


fig, ax = plt.subplots()
n, bins, patches = ax.hist(filtered_array, bins=10, edgecolor="black")

fig2, ax2 = plt.subplots()
n2, bins2, patches2 = ax2.hist(dollars_per_m2_array, bins=10, edgecolor="black")


# Function to format x-axis labels
def millions(x, pos):
    return f"${x/1e6:,.0f}M"


def thousands(x, pos):
    return f"${x/1e3:,.1f}K"


# Create the formatter
millions_formatter = FuncFormatter(millions)
thousands_formatter = FuncFormatter(thousands)

# Set the formatter to the x-axis
ax.xaxis.set_major_formatter(millions_formatter)
ax2.xaxis.set_major_formatter(thousands_formatter)



# Set the tick locations to match bin edges
ax.set_xticks(bins)
ax2.set_xticks(bins2)


# Rotate and align the tick labels so they look better
plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
plt.setp(ax2.get_xticklabels(), rotation=45, ha="right")


# Add frequency labels on top of each bar
for i in range(len(n)):
    # Calculate the center of each bar
    bar_center = (bins[i] + bins[i + 1]) / 2
    ax.text(bar_center, n[i], str(int(n[i])), ha="center", va="bottom")

for i in range(len(n2)):
    # Calculate the center of each bar
    bar_center = (bins2[i] + bins2[i + 1]) / 2
    ax2.text(bar_center, n2[i], str(int(n2[i])), ha="center", va="bottom")

# Use a FigureManager to adjust the layout to prevent label cutoff
plt.tight_layout()

# Customize the plot
ax.set_xlabel("Value (Millions of $)")
ax.set_ylabel("Number of properties sold")
ax.set_title("Sales price of empty residential land in Cottesloe (past 48 months)")

ax2.set_xlabel("Cost ($ per m²)")
ax2.set_ylabel("Number of properties sold")
ax2.set_title(f"Average cost per m² of empty residential land in Cottesloe (past 48 months)")


# Convert sale_date to datetime and extract year
df_columns_dropped["year"] = pd.to_datetime(df_columns_dropped["sale_date"]).dt.year

# Create the histogram data
hist_data = df_columns_dropped.groupby("year")["dollars_per_m2"].mean()


# Create the histogram using matplotlib
fig3, ax3 = plt.subplots(figsize=(12, 6))
ax3.bar(hist_data.index, hist_data.values, )
ax3.set_xlabel("Year")
ax3.set_ylabel("Average cost per m²")
ax3.set_title("Average cost per m² of empty residential land in Cottesloe")
ax3.yaxis.set_major_formatter(thousands_formatter)
# Set specific years for x-axis ticks
specific_years = [2020, 2021, 2022, 2023]
ax3.set_xticks(specific_years)
ax3.set_xticklabels(specific_years)
#



# Text content
#
previous_post_url = "/value-of-land-in-cottesloe-20240705"
st.markdown(f"""
# Value of empty residential blocks in Cottesloe

###### 2024/07/08

### Background

Building on a <a href="{previous_post_url}" target="_self">previous post</a>, this post will explore the current value of empty residential blocks in Cottesloe.

The key focus will be on the question "What is the average value of a m² of **empty** residential land in Cottesloe over the past 48 months?".  The post will be updated with sales data as it becomes available.  Check back for updates.
""", unsafe_allow_html=True)
# add an image
st.image("./_pages/images/2024_07_08/cottesloe.jpg", caption="Cottesloe, Western Australia")

st.markdown("### Summary")
st.metric("Average Cottesloe vacant land cost per m²", f"${average_per_m2_in_past_48_months:,.0f}")
st.markdown(
    f"The average cost per m² in Cottesloe for vacant residential housing land in the past 48 months was :blue-background[\\${average_per_m2_in_past_48_months:,.0f}].  Read on for methodology and data."
)
st.markdown("#### Initial raw data")
f"The initial data consists of {df.shape[0]} sales records in Cottesloe from {df['sale_date'].min()} to {df['sale_date'].max()}.  There are not a lot of empty land sales in Cottesloe each year."

df_columns_dropped = df_columns_dropped.drop(columns=["year"])
st.dataframe(df_columns_dropped, hide_index=True)
st.markdown("##### Empty land sales prices")
st.pyplot(fig)
st.markdown("##### Empty land cost per m²")
st.pyplot(fig2)

st.markdown("##### Empty land cost per m² over time")
st.pyplot(fig3)

f"### Conclusion"
f" Based on the above data, the average cost per m² in the past 48 months for empty residential housing land in Cottesloe was :blue-background[\\${average_per_m2_in_past_48_months:,.0f}]"
f"### Next steps"
"""
- Filter for potential knockdowns?
- Consider how housing value fits into a model
- Allow user to filter by street and or year

### Feedback
Is always welcomed.  Please raise an issue at the [GitHub for this app](https://github.com/spinoffblog/blog/issues) with any suggestions or changes.
"""
##
