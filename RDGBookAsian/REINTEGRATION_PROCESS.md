# Reintegration Process

## Overview
This document explains how to merge approved markdown changes back into the master JSON file (RDGAsianMaster.json).

## When to Reintegrate
Reintegration should happen when:
1. Markdown file has been edited
2. Changes have been reviewed
3. Changes have been approved by project owner
4. You're ready to update the master JSON

## Prerequisites
- Python 3.6 or higher
- Approved markdown changes committed to repository
- Backup of RDGAsianMaster.json (script creates this automatically)

## The Reintegration Script

### Location
`reintegrate_markdown.py`

### What It Does
1. Reads the markdown file
2. Extracts all paragraphs with IDs (e.g., p9-1, p10-5)
3. Finds matching IDs in RDGAsianMaster.json
4. Updates the JSON content with markdown content
5. Increments the JSON version number
6. Creates a backup before saving
7. Saves the updated master JSON

## Usage

### Basic Usage - Single Section
```bash
# Reintegrate a specific markdown file
python reintegrate_markdown.py section4_introduction_english.md

# Or by section number
python reintegrate_markdown.py --section 4
```

### Dry Run (See Changes Without Saving)
```bash
# Preview what would change without actually updating
python reintegrate_markdown.py section4_introduction_english.md --dry-run
```

### Reintegrate All Sections
```bash
# Reintegrate all section markdown files
python reintegrate_markdown.py --all

# Dry run for all sections
python reintegrate_markdown.py --all --dry-run
```

### Custom Master JSON Path
```bash
# If master JSON is in a different location
python reintegrate_markdown.py section4_introduction_english.md --master-json /path/to/RDGAsianMaster.json
```

## Step-by-Step Process

### Step 1: Verify Markdown Changes
```bash
# Review what changed in the markdown
git diff section4_introduction_english.md
```

### Step 2: Run Dry Run
```bash
# See what would be updated
python reintegrate_markdown.py section4_introduction_english.md --dry-run
```

Review the output carefully. It will show:
- How many paragraphs would be updated
- Old vs new content for each change
- Version number change

### Step 3: Run Actual Reintegration
```bash
# Update the master JSON
python reintegrate_markdown.py section4_introduction_english.md
```

### Step 4: Review Changes
```bash
# Check what changed in the JSON
git diff RDGAsianMaster.json
```

Verify:
- ✅ Only expected content was updated
- ✅ JSON structure is intact
- ✅ Version number was incremented
- ✅ Backup file was created

### Step 5: Commit Changes
```bash
# Stage both files
git add section4_introduction_english.md RDGAsianMaster.json

# Commit with descriptive message
git commit -m "Reintegrate Section 4 edits to master JSON

- Fixed typos in Chapter 9
- Improved clarity in Chapter 10
- Updated JSON version to 3.2"

# Push to branch
git push -u origin [your-branch-name]
```

## Safety Features

### Automatic Backups
Every time you run the script, it creates a timestamped backup:
```
RDGAsianMaster.backup-20251107-143025.json
```

These backups are saved in the same directory as the master JSON.

### Dry Run Mode
Always test with `--dry-run` first to see changes before applying them.

### Version Increment
The script automatically increments the JSON version number in metadata.

## Output Examples

### Successful Reintegration
```
============================================================
MARKDOWN → JSON REINTEGRATION
============================================================
Loading master JSON: RDGAsianMaster.json
✓ Loaded JSON version 3.1

Parsing markdown: section4_introduction_english.md
✓ Found 42 paragraphs with IDs

Searching for IDs in JSON...

============================================================
CHANGES SUMMARY (3 updates)
============================================================

1. ID: p9-1
   OLD: Dharma is a Sanscrit word meaning "truth"...
   NEW: Dharma is a Sanskrit word meaning "truth"...

2. ID: p9-5
   OLD: This is a renunciation based program...
   NEW: This is a renunciation-based program...

3. ID: p10-3
   OLD: As we learn about the Four Noble Truths...
   NEW: As we learn about the Four Noble Truths — including...

Creating backup: RDGAsianMaster.backup-20251107-143025.json

✓ Version updated: 3.1 → 3.2

Saving master JSON: RDGAsianMaster.json
✓ Master JSON updated successfully

============================================================
✓ SUCCESS: 3 paragraphs updated
============================================================
```

### No Changes
```
============================================================
MARKDOWN → JSON REINTEGRATION
============================================================
Loading master JSON: RDGAsianMaster.json
✓ Loaded JSON version 3.1

Parsing markdown: section4_introduction_english.md
✓ Found 42 paragraphs with IDs

Searching for IDs in JSON...

⚠ No changes detected

============================================================
No changes to apply
============================================================
```

## Troubleshooting

### Error: "File not found"
- Check that you're in the RDGBookAsian directory
- Verify the markdown file name is correct
- Use `ls section*.md` to see available files

### Error: "No paragraph IDs found"
- Verify the markdown file has IDs in format: `### ID: p9-1`
- Check ID_SPECIFICATION.md for correct format

### Error: Python not found
```bash
# Check Python version
python3 --version

# Use python3 if python doesn't work
python3 reintegrate_markdown.py section4_introduction_english.md
```

### Changes Not Showing Up
Possible reasons:
1. IDs in markdown don't match IDs in JSON
2. Content is identical (no actual changes)
3. Wrong section file being processed

Solution: Run with `--dry-run` first to debug

## Best Practices

### ✅ DO
- Always run dry-run first
- Review the changes summary carefully
- Keep backups (script does this automatically)
- Commit markdown and JSON together
- Test the script on a single section before using `--all`

### ❌ DON'T
- Don't skip the dry-run step
- Don't manually edit the JSON after reintegration
- Don't delete backup files until changes are confirmed
- Don't reintegrate without approval from project owner

## Rollback Process

If something goes wrong:

### Option 1: Use Git
```bash
# Discard JSON changes
git checkout RDGAsianMaster.json
```

### Option 2: Use Backup File
```bash
# Find the latest backup
ls -lt RDGAsianMaster.backup-*.json | head -1

# Restore from backup
cp RDGAsianMaster.backup-20251107-143025.json RDGAsianMaster.json
```

## Advanced Usage

### Custom ID Pattern
If you need to modify the ID pattern, edit the regex in `reintegrate_markdown.py`:
```python
# Current pattern: ### ID: p9-1
pattern = r'###\s+ID:\s+(p\d+[a-z]?-\d+(?:\.\d+)?)\s*\n...'
```

### Batch Processing with Verification
```bash
# Process all sections with pause between each
for file in section*_english.md; do
    echo "Processing $file..."
    python reintegrate_markdown.py "$file" --dry-run
    read -p "Apply changes? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        python reintegrate_markdown.py "$file"
    fi
done
```

## Questions?
Contact: scott@farclass.com
Repository: https://github.com/scott009/RDGBookAsian
