import argparse
import sys
from spinoff_blog.real_estate.main import run as run_real_estate_main
from spinoff_blog.root.main import run as run_root_main
import os
from dotenv import load_dotenv


# Determine the environment
env = os.getenv("STREAMLIT_ENV", "development")

# Load the appropriate .env file
load_dotenv(f".env.{env}")

# Rest of your main.py code...


def run():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Run Spinoff Blog Streamlit app")
    parser.add_argument(
        "domain",
        choices=["root", "real_estate"],
        help="Choose domain: root or real_estate",
    )

    # Check if running with `streamlit run`
    if sys.argv[0].endswith("streamlit"):
        # Remove 'streamlit' and 'run' from sys.argv
        sys.argv = sys.argv[2:]

    args = parser.parse_args()

    if args.domain == "root":
        run_root_main()
    elif args.domain == "real_estate":  # real_estate
        run_real_estate_main()
    else:
        # exit if domain is not valid
        print("Invalid domain")
        sys.exit(1)


if __name__ == "__main__":
    run()
