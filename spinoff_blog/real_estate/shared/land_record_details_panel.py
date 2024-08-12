import streamlit as st


def land_record_details_panel(record):

    # st.write(f"### {record['city'].title()}, {record['state']}")
    # TODO: make zoning safe
    st.write(" ")

    r_code = "N/A"
    if record["zoning"] and len(record["zoning"]) and record["zoning"][0]:
        r_code = record["zoning"][0]["r_code"]

    text_with_icons = f"""
    <i class="fa-solid fa-maximize"></i>   {record['land_area']:,.0f} m² <br />
    <i class="fa-solid fa-file-lines"></i>   {record['land_type']}<br />
    <i class="fa-solid fa-person-digging"></i>   {r_code}<br />
    """
    st.write(text_with_icons, unsafe_allow_html=True)
