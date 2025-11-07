#!/usr/bin/env python3
"""
Reintegrate Markdown to JSON
Syncs approved markdown changes back to RDGAsianMaster.json

Usage:
    python reintegrate_markdown.py section4_introduction_english.md
    python reintegrate_markdown.py --section 4
    python reintegrate_markdown.py --all --dry-run
"""

import json
import re
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime

class MarkdownReintegrator:
    def __init__(self, master_json_path: str = "RDGAsianMaster.json"):
        self.master_json_path = Path(master_json_path)
        self.master_data = None
        self.changes = []

    def load_master_json(self):
        """Load the master JSON file"""
        print(f"Loading master JSON: {self.master_json_path}")
        with open(self.master_json_path, 'r', encoding='utf-8') as f:
            self.master_data = json.load(f)
        print(f"✓ Loaded JSON version {self.master_data['metadata']['json_version']}")

    def parse_markdown(self, md_path: Path) -> Dict[str, str]:
        """
        Parse markdown file and extract content by ID
        Returns: {id: content}
        """
        print(f"\nParsing markdown: {md_path}")

        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Pattern to match: ### ID: p9-1\nContent here
        pattern = r'###\s+ID:\s+(p\d+[a-z]?-\d+(?:\.\d+)?)\s*\n((?:(?!###\s+ID:)(?!##\s+Chapter).)*)'

        matches = re.finditer(pattern, content, re.DOTALL)

        id_content_map = {}
        for match in matches:
            paragraph_id = match.group(1).strip()
            paragraph_content = match.group(2).strip()
            id_content_map[paragraph_id] = paragraph_content

        print(f"✓ Found {len(id_content_map)} paragraphs with IDs")
        return id_content_map

    def find_and_update_content(self, data: dict, id_content_map: Dict[str, str]) -> int:
        """
        Recursively find IDs in JSON and update content
        Returns: number of updates made
        """
        updates = 0

        if isinstance(data, dict):
            # Check if this is a content item with an ID
            if 'type' in data and data['type'] == 'paragraph' and 'id' in data:
                para_id = data['id']
                if para_id in id_content_map:
                    new_text = id_content_map[para_id]
                    old_text = data.get('text', '')

                    if new_text != old_text:
                        self.changes.append({
                            'id': para_id,
                            'old': old_text[:100] + '...' if len(old_text) > 100 else old_text,
                            'new': new_text[:100] + '...' if len(new_text) > 100 else new_text
                        })
                        data['text'] = new_text
                        updates += 1

            # Recurse through all dict values
            for key, value in data.items():
                updates += self.find_and_update_content(value, id_content_map)

        elif isinstance(data, list):
            # Recurse through all list items
            for item in data:
                updates += self.find_and_update_content(item, id_content_map)

        return updates

    def increment_version(self):
        """Increment the JSON version number"""
        current_version = self.master_data['metadata']['json_version']

        # Parse version (e.g., "3.1" -> major=3, minor=1)
        match = re.match(r'(\d+)\.(\d+)', str(current_version))
        if match:
            major = int(match.group(1))
            minor = int(match.group(2))
            new_version = f"{major}.{minor + 1}"
        else:
            new_version = f"{current_version}.1"

        self.master_data['metadata']['json_version'] = new_version
        print(f"\n✓ Version updated: {current_version} → {new_version}")

    def save_master_json(self, backup: bool = True):
        """Save the updated master JSON"""
        if backup:
            backup_path = self.master_json_path.with_suffix(f'.backup-{datetime.now().strftime("%Y%m%d-%H%M%S")}.json')
            print(f"\nCreating backup: {backup_path}")
            with open(backup_path, 'w', encoding='utf-8') as f:
                json.dump(self.master_data, f, ensure_ascii=False, indent=2)

        print(f"Saving master JSON: {self.master_json_path}")
        with open(self.master_json_path, 'w', encoding='utf-8') as f:
            json.dump(self.master_data, f, ensure_ascii=False, indent=2)

        print("✓ Master JSON updated successfully")

    def print_changes(self):
        """Print summary of changes"""
        if not self.changes:
            print("\n⚠ No changes detected")
            return

        print(f"\n{'='*60}")
        print(f"CHANGES SUMMARY ({len(self.changes)} updates)")
        print(f"{'='*60}")

        for i, change in enumerate(self.changes, 1):
            print(f"\n{i}. ID: {change['id']}")
            print(f"   OLD: {change['old']}")
            print(f"   NEW: {change['new']}")

    def reintegrate(self, md_path: Path, dry_run: bool = False):
        """Main reintegration process"""
        print(f"\n{'='*60}")
        print(f"MARKDOWN → JSON REINTEGRATION")
        print(f"{'='*60}")

        # Load master JSON
        self.load_master_json()

        # Parse markdown
        id_content_map = self.parse_markdown(md_path)

        # Update content
        print(f"\nSearching for IDs in JSON...")
        updates = self.find_and_update_content(self.master_data, id_content_map)

        # Print changes
        self.print_changes()

        if updates > 0 and not dry_run:
            # Increment version
            self.increment_version()

            # Save
            self.save_master_json(backup=True)

            print(f"\n{'='*60}")
            print(f"✓ SUCCESS: {updates} paragraphs updated")
            print(f"{'='*60}")
        elif updates > 0 and dry_run:
            print(f"\n{'='*60}")
            print(f"DRY RUN: Would update {updates} paragraphs")
            print(f"{'='*60}")
        else:
            print(f"\n{'='*60}")
            print(f"No changes to apply")
            print(f"{'='*60}")

def validate_markdown_file(md_path: Path) -> bool:
    """Basic validation of markdown file"""
    if not md_path.exists():
        print(f"❌ Error: File not found: {md_path}")
        return False

    if not md_path.suffix == '.md':
        print(f"❌ Error: Not a markdown file: {md_path}")
        return False

    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
        if 'ID: p' not in content:
            print(f"❌ Error: No paragraph IDs found in {md_path}")
            return False

    return True

def main():
    parser = argparse.ArgumentParser(
        description='Reintegrate markdown changes back to RDGAsianMaster.json'
    )
    parser.add_argument(
        'markdown_file',
        nargs='?',
        help='Markdown file to reintegrate (e.g., section4_introduction_english.md)'
    )
    parser.add_argument(
        '--section',
        type=int,
        help='Section number to reintegrate (e.g., 4 for section 4)'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='Reintegrate all section markdown files'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be changed without actually updating'
    )
    parser.add_argument(
        '--master-json',
        default='RDGAsianMaster.json',
        help='Path to master JSON file (default: RDGAsianMaster.json)'
    )

    args = parser.parse_args()

    # Determine which files to process
    files_to_process = []

    if args.markdown_file:
        files_to_process.append(Path(args.markdown_file))
    elif args.section:
        # Find the section file
        section_files = list(Path('.').glob(f'section{args.section}_*_english.md'))
        if not section_files:
            print(f"❌ Error: No markdown file found for section {args.section}")
            sys.exit(1)
        files_to_process.append(section_files[0])
    elif args.all:
        files_to_process = sorted(Path('.').glob('section*_english.md'))
        if not files_to_process:
            print("❌ Error: No section markdown files found")
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)

    # Validate files
    for md_file in files_to_process:
        if not validate_markdown_file(md_file):
            sys.exit(1)

    # Process each file
    reintegrator = MarkdownReintegrator(args.master_json)

    for md_file in files_to_process:
        try:
            reintegrator.reintegrate(md_file, dry_run=args.dry_run)
        except Exception as e:
            print(f"\n❌ Error processing {md_file}: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

if __name__ == '__main__':
    main()
