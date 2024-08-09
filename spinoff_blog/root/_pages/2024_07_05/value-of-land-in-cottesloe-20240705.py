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

df = pd.read_csv("spinoff_blog/root/data/2024_07_05/cott_real_estate.csv")
df = df.drop_duplicates(subset=["address", "sale_amount", "sale_date"], keep="first")
# make "address" title case
df["address"] = df["address"].str.title()
truncated_df = df

# "We need to remove the rows where 'property_status' == 'Strata'"
filtered_df = truncated_df[
    (df["multi_lot_sale"] != "Y")
    & (df["property_status"] != "Strata")
    & (df["data_source"] == "residential")
    & (df["sale_amount"] > truncation_amount)
]

filtered_array = filtered_df["sale_amount"].to_numpy()

# Calculate $ per m2 for each row and convert to numpy array
df_columns_dropped = filtered_df.drop(columns=["property_status", "multi_lot_sale"])
df_columns_dropped["dollars_per_m2"] = (
    df_columns_dropped["sale_amount"] / df_columns_dropped["land_area"]
).round()
df_columns_dropped["dollars_per_m2"] = df_columns_dropped["dollars_per_m2"].astype(int)
df_columns_dropped["land_area"] = df_columns_dropped["land_area"].astype(int)
dollars_per_m2_array = (
    df_columns_dropped["sale_amount"] / df_columns_dropped["land_area"]
).to_numpy()


# Get the date 12 months ago from today
twelve_months_ago = datetime.now().date() - timedelta(days=365)
df_columns_dropped["sale_date"] = pd.to_datetime(df_columns_dropped["sale_date"])
# Remove time component, keeping only the date
df_columns_dropped['sale_date'] = df_columns_dropped['sale_date'].dt.date

# Filter the DataFrame
df_truncated_sales = df_columns_dropped[
    df_columns_dropped["sale_date"] > twelve_months_ago
]
df_truncated_sales = df_truncated_sales[df_truncated_sales["dollars_per_m2"] > 500]

average_per_m2_in_2024 = df_truncated_sales["dollars_per_m2"].mean()
total_sales_in_past_year = df_truncated_sales.shape[0]
##

# Chart processing
#
fig, ax, n, bins, patches = None, None, None, None, None
fig2, ax2, n2, bins2, patches2 = None, None, None, None, None


fig, ax = plt.subplots()
n, bins, patches = ax.hist(filtered_array, bins=10, edgecolor="black")

fig2, ax2 = plt.subplots()
n2, bins2, patches2 = ax2.hist(dollars_per_m2_array, bins=10, edgecolor="black")

fig4, ax4 = plt.subplots()
n4, bins4, patches4 = ax4.hist(
    df_truncated_sales["dollars_per_m2"], bins=10, edgecolor="black"
)
y_min, y_max = plt.ylim()
# Create new y-ticks with increments of 2
new_yticks = np.arange(0, y_max + 2, 2)

# Set the new y-ticks
plt.yticks(new_yticks)

# Optionally, you can adjust the y-axis limits to match the new ticks
plt.ylim(0, new_yticks[-1])


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
ax4.xaxis.set_major_formatter(thousands_formatter)


# Set the tick locations to match bin edges
ax.set_xticks(bins)
ax2.set_xticks(bins2)
ax4.set_xticks(bins4)

# Rotate and align the tick labels so they look better
plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
plt.setp(ax2.get_xticklabels(), rotation=45, ha="right")
plt.setp(ax4.get_xticklabels(), rotation=45, ha="right")

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
ax.set_xlabel("Sales price (Millions of $)")
ax.set_ylabel("Number of properties sold")
ax.set_title("Sales price of properties in Cottesloe (all time)")

ax2.set_xlabel("Cost ($ per m²)")
ax2.set_ylabel("Number of properties sold")
ax2.set_title(f"Average cost per m² of house+land in Cottesloe (all time)")

ax4.set_xlabel("Cost ($ per m²)")
ax4.set_ylabel("Number of properties sold")
ax4.set_title(f"Average cost per m² of house+land in Cottesloe (past 12 months)")


# Convert sale_date to datetime and extract year
df_columns_dropped["year"] = pd.to_datetime(df_columns_dropped["sale_date"]).dt.year

# Create the histogram data
hist_data = df_columns_dropped.groupby("year")["dollars_per_m2"].mean()


# Create the histogram using matplotlib
fig3, ax3 = plt.subplots(figsize=(12, 6))
ax3.bar(hist_data.index, hist_data.values)
ax3.set_xlabel("Year")
ax3.set_ylabel("Average cost per m²")
ax3.set_title("Average house+land cost per m² by year in Cottesloe")
ax3.yaxis.set_major_formatter(thousands_formatter)

##


# Text content
#
f"""
# Value of residential house+land in Cottesloe

###### 2024/07/05

### Background

Cottesloe is a beach-side suburb of Perth, Western Australia.

It is known for its beaches, cafes, and relaxed lifestyle.

This post will explore the current value of residential house+land in Cottesloe.

The key focus will be on the question "What is the average value of a m² of residential house+land land in Cottesloe over the past 12 months?".  The post will be updated with sales data as it becomes available.  Check back for updates.
"""
# add an image
st.image("spinoff_blog/root/images/2024_07_05/cottesloe.jpg", caption="Cottesloe Beach")

st.markdown("### Summary")
st.metric("Average Cottesloe house+land cost per m²", f"${average_per_m2_in_2024:,.0f}")
st.markdown(
    f"The average cost per m² in Cottesloe for residential house+land land in the past 12 months was :blue-background[\\${average_per_m2_in_2024:,.0f}].  Read on for methodology and data."
)
st.markdown("#### Initial raw data")
f"The initial data consists of {df.shape[0]:,.0f} sales records in Cottesloe from {df['sale_date'].min()} to {df['sale_date'].max()}."
st.write(truncated_df)
"We need to remove the strata and multi-lot sales as these are not indicative of general residential house+land value.  Also need to remove sales less than $100,000, as these are likely outliers."
st.markdown(
    "#### Data after removing strata, multi-lot, commercial sales, and outliers"
)
st.write(filtered_df)
st.markdown("##### Property sales prices")
st.pyplot(fig)
st.markdown("##### Property cost per m²")
"Now to determine the cost per m² for each property."
st.write(df_columns_dropped)
st.pyplot(fig2)

st.markdown("##### Property house+land cost per m² over time")
st.pyplot(fig3)

# format truncation_amount as currency
truncation_amount = f"${truncation_amount:,.0f}"
f"##### Property cost per m² in {year_of_focus} (only property sales above {truncation_amount})"
f"Now to focus on the past 12 months of sales data.  We will also remove outlier sales where the cost per m² is less than $500. There were {total_sales_in_past_year} sales in the past 12 months."
st.dataframe(data=df_truncated_sales, hide_index=True)
st.pyplot(fig4)
f"### Conclusion"
f" The average cost per m² for the past 12 months for houses in Cottesloe was :blue-background[\\${average_per_m2_in_2024:,.0f}]"
f"### Next steps"
"""
- Filter for only land sales (and potential knockdowns?)
- Consider how housing value fits into a model
- Allow user to filter by street and or year

### Feedback
Is always welcomed.  Please raise an issue at the [GitHub for this app](https://github.com/spinoffblog/blog/issues) with any suggestions or changes.
"""
##
