from setuptools import setup, find_packages

setup(
    name="my_streamlit_app",
    version="0.1",
    packages=find_packages(exclude=["tests"]),
    entry_points={
        "console_scripts": [
            "my-streamlit-app=my_streamlit_app.main:run",
        ],
    },
    install_requires=[
        "streamlit",
        # Add other dependencies
    ],
)
