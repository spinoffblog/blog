import streamlit as st
import os
from dotenv import load_dotenv


# Determine the environment
env = os.getenv("STREAMLIT_ENV", "development")

# Load the appropriate .env file
load_dotenv(f".env.{env}")


def main():
    property_list = st.Page("./property_list/property_list.py")
    property_details = st.Page("./property_details/property_details.py")
    pg = st.navigation(pages=[property_list, property_details])
    pg.run()


if __name__ == "__main__":
    main()
