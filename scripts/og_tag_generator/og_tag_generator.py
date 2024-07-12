import os
import shutil

import yaml
from bs4 import BeautifulSoup


def generate_opengraph_tags(meta_data):
    """Generate OpenGraph tags based on meta.yaml content."""
    og_tags = []
    for key, value in meta_data.get("og", {}).items():
        og_tags.append(f'<meta property="og:{key}" content="{value}">')

    for key, value in meta_data.get("twitter", {}).items():
        og_tags.append(f'<meta name="twitter:{key}" content="{value}">')

    return "\n".join(og_tags)


def get_output_filename(directory):
    """Get the name of the first .py file in the directory and change extension to .html"""
    for file in os.listdir(directory):
        if file.endswith(".py"):
            return os.path.splitext(file)[0] + ".html"
    return "index.html"  # Default filename if no .py file is found


def process_meta_file(meta_file_path, template_path, output_dir, proxy_static_dir=None):
    """Process a single meta.yaml file and generate the corresponding HTML."""
    with open(meta_file_path, "r") as file:
        meta_data = yaml.safe_load(file)

    og_tags = generate_opengraph_tags(meta_data)

    with open(template_path, "r") as file:
        template = BeautifulSoup(file, "html.parser")

    # Find the <head> tag and insert the OpenGraph tags
    head_tag = template.find("head")
    if head_tag:
        head_tag.append(BeautifulSoup(og_tags, "html.parser"))

    # Update the <title> tag
    title_tag = template.find("title")
    if title_tag:
        title_tag.string = meta_data.get("title", "Untitled")
    else:
        new_title_tag = template.new_tag("title")
        new_title_tag.string = meta_data.get("title", "Untitled")
        head_tag.append(new_title_tag)

    # Generate the output filename based on the first .py file in the directory
    directory = os.path.dirname(meta_file_path)
    output_filename = get_output_filename(directory)
    output_path = os.path.join(output_dir, output_filename)

    # Save the generated HTML
    with open(output_path, "w") as file:
        file.write(str(template))

    # Copy to proxy_static_dir if specified
    if proxy_static_dir:
        proxy_output_path = os.path.join(proxy_static_dir, output_filename)
        shutil.copy2(output_path, proxy_output_path)


def main():
    pages_dir = "../../_pages"
    template_path = "./templates/index.html"
    output_dir = "./output/"
    proxy_static_dir = os.environ.get("PROXY_STATIC_DIR")

    # Ensure the output directories exist
    os.makedirs(output_dir, exist_ok=True)
    if proxy_static_dir:
        os.makedirs(proxy_static_dir, exist_ok=True)

    # Traverse the /_pages directory
    for root, _, files in os.walk(pages_dir):
        if "meta.yaml" in files:
            meta_file_path = os.path.join(root, "meta.yaml")
            process_meta_file(
                meta_file_path, template_path, output_dir, proxy_static_dir
            )


if __name__ == "__main__":
    main()
