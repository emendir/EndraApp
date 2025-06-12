
import sys
import xml.etree.ElementTree as ET
from datetime import date
import os
try:
    import tomllib  # Python 3.11+
except ModuleNotFoundError:
    import tomli as tomllib  # Python <3.11

import re
from pathlib import Path

def load_long_description(directory:str):
    readme_candidates = ["README.md", "README.rst", "README.txt", "README"]

    # Find a valid README file
    readme_path = next((Path(directory)/Path(f) for f in readme_candidates if (Path(directory)/Path(f)).is_file()), None)
    if not readme_path:
        raise FileNotFoundError("No README file found.")

    with readme_path.open(encoding="utf-8") as f:
        content = f.read()

    # Split into paragraphs
    paragraphs = re.split(r"\n\s*\n", content)

    for para in paragraphs:
        para = para.strip()

        # Skip headings: Markdown or reStructuredText style
        if para.startswith("#") or re.match(r"^[=\-]{3,}$", para):
            continue

        # Skip paragraphs in italic (Markdown-style)
        if re.match(r"^[_*].*[_*]$", para) and not re.search(r"\*\*", para):
            continue

        # Normalize line breaks, ensure it's >80 chars
        para_flat = " ".join(para.splitlines()).strip()
        if len(para_flat) >= 80:
            return para_flat

    raise ValueError("No suitable paragraph found in README.")

def generate_metainfo(pyproject_path: str, app_id: str, output_path):
    with open(pyproject_path, "rb") as f:
        pyproject = tomllib.load(f)

    project = pyproject.get("project", {})

    name = project.get("name", "unknown")
    summary_raw = project.get("description", "No description provided.")
    summary = summary_raw.rstrip(".")  # Flathub requires no trailing dot
    version = project.get("version", "0.1.0")
    homepage = project.get("urls", {}).get("Homepage", "")
    authors = project.get("authors", [])
    license = project.get("license", [])
    author_name = authors[0]["name"] if authors else "Unknown Developer"
    author_id = authors[0]["email"].split("@")[-1] if authors else "Unknown Developer"

    # Start XML structure
    root = ET.Element("component", type="desktop")
    ET.SubElement(root, "id").text = app_id
    ET.SubElement(root, "metadata_license").text = license
    ET.SubElement(root, "name").text = name
    ET.SubElement(root, "summary").text = summary

    # Description (long enough first paragraph)
    description = ET.SubElement(root, "description")
    ET.SubElement(description, "p").text =        load_long_description(os.path.dirname(pyproject_path)    )

    # Developer
    developer = ET.SubElement(root, "developer", id=author_id)
    ET.SubElement(developer, "name").text = author_name

    # Homepage
    if homepage:
        url_elem = ET.SubElement(root, "url", type="homepage")
        url_elem.text = homepage

    # Launchable
    ET.SubElement(root, "launchable", type="desktop-id").text = f"{app_id}.desktop"

    # Content rating placeholder (generate real one at https://hughsie.github.io/oars/)
    rating = ET.SubElement(root, "content_rating", type="oars-1.1")
    ET.SubElement(rating, "content_attribute", id="violence-cartoon").text = "none"
    ET.SubElement(rating, "content_attribute", id="language-profanity").text = "none"

    # Release
    releases_elem = ET.SubElement(root, "releases")
    release_elem = ET.SubElement(releases_elem, "release", version=version, date=date.today().isoformat())

    # Output to file
    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ")
    tree.write(output_path, encoding="utf-8", xml_declaration=True)
    print(f"Generated {output_path} with Flathub-compatible metadata.")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python generate_metainfo.py pyproject.toml com.example.MyApp com.example.MyApp.desktop")
        sys.exit(1)
    # print(sys.argv)
    generate_metainfo(sys.argv[1], sys.argv[2], sys.argv[3])
