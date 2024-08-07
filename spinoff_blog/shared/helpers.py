import streamlit as st
import json
import os
import requests
import inflect
from thefuzz import process

API_URL = os.getenv("API_URL")
USE_LOCAL_DATA = False  # os.getenv("USE_LOCAL_DATA", "false")

USER_CURRENCY = "AUD"

CURRENCIES = {
    "AUD": {"symbol": "$", "name": "Australian Dollar", "code": "AUD", "rate": 1}
}

# For ordinalizing numbers
p = inflect.engine()


def get_simple_addresses():
    if USE_LOCAL_DATA:
        return get_local_simple_addresses()
    else:
        return get_remote_simple_addresses()


def get_property(id):
    response = requests.get(f"{API_URL}landrecord/{id}/")
    if response.status_code == 200:
        return response.json()
    else:
        st.warning(f"Failed to fetch data for ID {id}")
        return None


def get_comparison_land_sales(suburb):
    if USE_LOCAL_DATA:
        return get_local_comparison_land_sales()
    else:
        return get_remote_comparison_land_sales(suburb)


def get_financial_data(id):
    response = requests.get(f"{API_URL}property-stats/{id}/financial_stats/")
    if response.status_code == 200:
        return response.json()
    else:
        st.warning(f"Failed to fetch financial data for ID {id}")
        return None


@st.cache_data
def get_remote_comparison_land_sales(suburb):
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
        st.warning(f"Failed to fetch data for suburb {suburb}")
        return None


@st.cache_data
def get_remote_simple_addresses():
    url = f"{API_URL}simple-addresses/"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.warning("Failed to fetch data")
        return None


def get_local_simple_addresses():
    # Load the JSON file
    with open("spinoff_blog/data/simple-addresses.json", "r") as file:
        data = json.load(file)
    return data


def get_local_comparison_land_sales():
    # Load the JSON file
    with open("spinoff_blog/data/comparison_land_sales.json", "r") as file:
        data = json.load(file)
    return data


def fuzzy_match_address(query, properties, score_cutoff=80, limit=None):
    # Extract just the names for initial matching
    addresses = [item["formatted_address"] for item in properties]

    # Perform fuzzy matching
    matches = process.extractBests(
        query, addresses, score_cutoff=score_cutoff, limit=limit
    )

    # If we have matches, find the corresponding full records
    results = []
    for match in matches:
        matched_name, score = match
        # Find the original dict that contains this name
        original_record = next(
            item for item in properties if item["formatted_address"] == matched_name
        )
        results.append((original_record, score))

    return results


## Formatting


def ordinalize_number(number):
    return p.ordinal(number)


def format_currency(amount):
    in_user_currency = amount * CURRENCIES[USER_CURRENCY]["rate"]
    return f"{CURRENCIES[USER_CURRENCY]['symbol']}{in_user_currency:,.0f}"
