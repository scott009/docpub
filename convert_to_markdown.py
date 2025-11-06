#!/usr/bin/env python3
"""
Convert Recovery Dharma JSON files to English-only markdown format.
Extracts English paragraphs and headings with their IDs.
"""

import json
import os
from pathlib import Path


def extract_english_content(data, level=1):
    """Recursively extract English content from JSON structure."""
    content_lines = []

    if isinstance(data, dict):
        # Handle section with title
        if data.get('type') == 'section' and data.get('title'):
            content_lines.append(f"# Section {data.get('id')}: {data['title']}\n")

        # Handle chapters
        if data.get('type') == 'chapter':
            chapter_id = data.get('id')
            title = data.get('title', '')
            if title:
                content_lines.append(f"## Chapter {chapter_id}: {title}\n")

        # Handle sections within chapters
        if data.get('type') == 'section' and 'heading' in data:
            heading = data.get('heading', '')
            if heading and heading != '':
                content_lines.append(f"### {heading}\n")

        # Handle subsections
        if data.get('type') == 'subsection':
            heading = data.get('heading', '')
            if heading and heading != '':
                content_lines.append(f"#### {heading}\n")

        # Handle paragraphs
        if data.get('type') == 'paragraph':
            para_id = data.get('id', '')
            text = data.get('text', '')
            if para_id and text:
                content_lines.append(f"### ID: {para_id}")
                content_lines.append(f"{text}\n")

        # Recursively process nested content
        for key in ['chapters', 'sections', 'content']:
            if key in data:
                nested_content = extract_english_content(data[key], level + 1)
                if nested_content:
                    content_lines.extend(nested_content)

    elif isinstance(data, list):
        for item in data:
            nested_content = extract_english_content(item, level)
            if nested_content:
                content_lines.extend(nested_content)

    return content_lines


def convert_json_to_markdown(json_file_path):
    """Convert a single JSON file to markdown."""
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Extract English content
    content_lines = extract_english_content(data)

    # Join lines with proper spacing
    markdown_content = '\n'.join(content_lines)

    # Create output filename
    base_name = Path(json_file_path).stem
    output_file = Path(json_file_path).parent / f"{base_name}_english.md"

    # Write markdown file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(markdown_content)

    print(f"Created: {output_file}")
    return output_file


def main():
    """Convert all section JSON files in RDGBookAsian directory."""
    # Get the directory containing JSON files
    script_dir = Path(__file__).parent
    json_dir = script_dir / 'RDGBookAsian'

    if not json_dir.exists():
        print(f"Error: Directory not found: {json_dir}")
        return

    # Find all section JSON files
    json_files = sorted(json_dir.glob('section*.json'))

    if not json_files:
        print(f"No section*.json files found in {json_dir}")
        return

    print(f"Found {len(json_files)} JSON files to convert\n")

    # Convert each file
    for json_file in json_files:
        print(f"Converting {json_file.name}...")
        try:
            convert_json_to_markdown(json_file)
        except Exception as e:
            print(f"Error converting {json_file.name}: {e}")

    print("\nConversion complete!")


if __name__ == '__main__':
    main()
