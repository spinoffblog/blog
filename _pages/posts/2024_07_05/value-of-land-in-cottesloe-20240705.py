import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Data processing
#
truncation_size = 100
year_of_focus = 2023
truncation_amount = 100000

df = pd.read_csv("./_pages/data/2024_07_05/full_cott_real_estate_filtered.csv")
df = df.drop_duplicates(subset=["address", "sale_amount", "sale_date"], keep="first")
truncated_df = df

# "We need to remove the rows where 'property_status' == 'Strata'"
filtered_df = truncated_df[
    (df["multi_lot_sale"] != "Y")
    & (df["property_status"] != "Strata")
    & (df["data_source"] == "RES")
    & (df["sale_amount"] > truncation_amount)
]

filtered_array = filtered_df["sale_amount"].to_numpy()

# Calculate $ per m2 for each row and convert to numpy array
df_columns_dropped = filtered_df.drop(columns=["property_status", "multi_lot_sale"])
df_columns_dropped["dollar_per_m2"] = (
    df_columns_dropped["sale_amount"] / df_columns_dropped["land_area"]
).round()
df_columns_dropped["dollar_per_m2"] = df_columns_dropped["dollar_per_m2"].astype(int)
df_columns_dropped["land_area"] = df_columns_dropped["land_area"].astype(int)
dollar_per_m2_array = (
    df_columns_dropped["sale_amount"] / df_columns_dropped["land_area"]
).to_numpy()

df_truncated_sales = df_columns_dropped[
    (df_columns_dropped["sale_date"].str.contains(str(year_of_focus)))
]

average_per_m2_in_2024 = df_truncated_sales["dollar_per_m2"].mean()
latest_year = df_truncated_sales["sale_date"].max().split("-")[0]
##

# Chart processing
#
fig, ax, n, bins, patches = None, None, None, None, None
fig2, ax2, n2, bins2, patches2 = None, None, None, None, None


fig, ax = plt.subplots()
n, bins, patches = ax.hist(filtered_array, bins=10, edgecolor="black")

fig2, ax2 = plt.subplots()
n2, bins2, patches2 = ax2.hist(dollar_per_m2_array, bins=10, edgecolor="black")

fig4, ax4 = plt.subplots()
n4, bins4, patches4 = ax4.hist(
    df_truncated_sales["dollar_per_m2"], bins=10, edgecolor="black"
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
ax.set_xlabel("Value (Millions of $)")
ax.set_ylabel("Number of properties sold")
ax.set_title("Sales price of properties in Cottesloe (all time)")

ax2.set_xlabel("Cost ($ per m²)")
ax2.set_ylabel("Number of properties sold")
ax2.set_title(f"Average cost per m² of properties in Cottesloe (all time)")

ax4.set_xlabel("Cost ($ per m²)")
ax4.set_ylabel("Number of properties sold")
ax4.set_title(f"Average cost per m² of properties in Cottesloe ({latest_year})")


# Convert sale_date to datetime and extract year
df_columns_dropped["year"] = pd.to_datetime(df_columns_dropped["sale_date"]).dt.year

# Create the histogram data
hist_data = df_columns_dropped.groupby("year")["dollar_per_m2"].mean()


# Create the histogram using matplotlib
fig3, ax3 = plt.subplots(figsize=(12, 6))
ax3.bar(hist_data.index, hist_data.values)
ax3.set_xlabel("Year")
ax3.set_ylabel("Average cost per m²")
ax3.set_title("Average property cost per m² by year in Cottesloe")
ax3.yaxis.set_major_formatter(thousands_formatter)

##


# Text content
#
f"""
# Value of land in Cottesloe

###### 2024/07/05

### Background

Cottesloe is a beach-side suburb of Perth, Western Australia.

It is known for its beaches, cafes, and relaxed lifestyle.

This post will explore the current value of land in Cottesloe.

The key focus will be on the question "What is the average value of a m² land in Cottesloe in {latest_year}?".  The post will be updated with sales data as it becomes available.  Check back for updates.
"""
# add an image
st.image("./_pages/images/2024_07_05/cottesloe.jpg")
# st.image("https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Flive.staticflickr.com%2F3084%2F3251405982_3cc7b69cec_b.jpg&f=1&nofb=1&ipt=5a91db16c85b1bb7652136e06423c8c0bd873381198746ecc685cf9ab765f6b7&ipo=images", caption="Cottesloe Beach")

st.markdown("#### Initial raw data")
f"The initial data consists of {df.shape[0]} sales records in Cottesloe from {df['sale_date'].min()} to {df['sale_date'].max()}."
st.write(truncated_df)
"We need to remove the strata and multi-lot sales as these are not indicative of general land value.  Also need to remove sales less than $100,000, as these are likely outliers."
st.markdown("#### Data after removing strata, multi-lot, commercial sales, and outliers")
st.write(filtered_df)
st.markdown("##### Property sales prices")
st.pyplot(fig)
st.markdown("##### Property cost per m²")
"Now to determine the cost per m² for each property."
st.write(df_columns_dropped)
st.pyplot(fig2)

st.markdown("##### Property cost per m² over time")
st.pyplot(fig3)

# format truncation_amount as currency
truncation_amount = f"${truncation_amount:,.0f}"
f"Now to focus on latest year of data, {year_of_focus}, removing any outlier sales with prices below {truncation_amount}."
f"##### Property cost per m² in {year_of_focus} (only property sales above {truncation_amount})"
st.pyplot(fig4)
f"## *The average cost per m² in {year_of_focus} for houses in Cottesloe was \\${average_per_m2_in_2024:,.0f}*"

##
