import streamlit as st
import argparse
import sys
from real_estate import run_main as run_subdomain_main


def run():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Run Spinoff Blog Streamlit app")
    parser.add_argument(
        "domain", choices=["main", "real_estate"], help="Choose domain: main or real_estate"
    )

    # Check if running with `streamlit run`
    if sys.argv[0].endswith("streamlit"):
        # Remove 'streamlit' and 'run' from sys.argv
        sys.argv = sys.argv[2:]

    args = parser.parse_args()

    st.set_page_config(page_title="Spinoff Blog", layout="wide")

    if args.domain == "main":
        with st.sidebar:
            st.title("Main Domain")
    elif args.domain == "real_estate":  # real_estate
        run_subdomain_main()
    else:
        # exit if domain is not valid
        print("Invalid domain")
        sys.exit(1)


if __name__ == "__main__":
    run()
