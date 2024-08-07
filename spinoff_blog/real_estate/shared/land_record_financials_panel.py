import streamlit as st
import pandas as pd
from spinoff_blog.real_estate.shared.land_record import LandRecord


def land_record_financials_panel(record: LandRecord, financial_stats):
    st.write(f"##### Metrics")

    data = {
        f"{record.formatted_address()}": [record.formatted_cost_per_m2()],
        f"{record.city.title()} average": ["-"],
    }
    df = pd.DataFrame(
        data,
        index=[
            "House and land value per m²",
        ],
    )

    st.dataframe(df, hide_index=False)
