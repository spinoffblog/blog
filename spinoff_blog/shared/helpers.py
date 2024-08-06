import streamlit as st
import json
import os
import requests


API_URL = os.getenv("API_URL")
USE_LOCAL_DATA = os.getenv("USE_LOCAL_DATA", "false")


def get_properties():
    if USE_LOCAL_DATA:
        return load_local_properties()
    else:
        return []


def get_property(id):
    response = requests.get(f"{API_URL}landrecord/{id}/")
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch data for ID {id}")
        return None


def get_comparison_land_sales(suburb):
    if USE_LOCAL_DATA:
        return load_local_comparison_land_sales()
    else:
        return fetch_comparison_land_sales(suburb)


@st.cache_data
def fetch_comparison_land_sales(suburb):
    response = requests.get(
        f"{API_URL}suburb-latest-landsalerecord/sales-by-suburb/?suburb={suburb}"
    )
    if response.status_code == 200:
        # add dollars_per_m2 to response
        result = []
        for sale in response.json():
            sale["dollars_per_m2"] = sale["amount"] / sale["land_area"]
            result.append(sale)
        return result
    else:
        st.error(f"Failed to fetch data for suburb {suburb}")
        return None


def load_local_properties():
    # Load the JSON file
    with open("spinoff_blog/data/properties.json", "r") as file:
        data = json.load(file)
    return data


def load_local_comparison_land_sales():
    # Load the JSON file
    with open("spinoff_blog/data/comparison_land_sales.json", "r") as file:
        data = json.load(file)
    return data
