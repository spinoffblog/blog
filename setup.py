from setuptools import setup, find_packages

# Read the contents of your README file
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

# Read requirements from requirements.txt
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="spinoff_blog",
    version="0.1",
    author="spinoffblog",
    author_email="your.email@example.com",  # You may want to update this
    description="A Streamlit app for the Spinoff Blog",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/spinoffblog/blog",
    packages=find_packages(exclude=["tests"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "spinoff-blog-root=spinoff_blog.root.main:run",
            "spinoff-blog-real-estate=spinoff_blog.real_estate.main:run",
        ],
    },
    install_requires=requirements,
    include_package_data=True,
)