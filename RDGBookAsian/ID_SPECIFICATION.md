# ID Specification for RDGBookAsian

## Overview
This document defines the ID system used throughout the RDGBookAsian project to maintain consistency between markdown files and the master JSON file.

## ID Format

### Basic Pattern
```
p[chapter]-[number]
```

### Components
- **Prefix**: Always `p` (for paragraph/section)
- **Chapter Number**: The chapter number (1-31+)
- **Separator**: Always a hyphen `-`
- **Sequential Number**: Incremental number starting at 1

### Examples
```markdown
### ID: p9-1
First paragraph of Chapter 9

### ID: p9-2
Second paragraph of Chapter 9

### ID: p10-1
First paragraph of Chapter 10
```

### Special Cases: Sub-chapters
Some chapters have sub-chapters (e.g., 11a, 11b):
```markdown
### ID: p11a-1
First paragraph of Chapter 11a

### ID: p11a-2
Second paragraph of Chapter 11a
```

## ID Assignment Rules

### Rule 1: Sequential Numbering
IDs within a chapter must be sequential without gaps:
✅ Correct: p9-1, p9-2, p9-3, p9-4
❌ Incorrect: p9-1, p9-2, p9-5, p9-7

### Rule 2: No ID Changes
**NEVER change existing IDs** unless specifically instructed by the project owner.

Why? IDs are references that may be used in:
- Cross-references within the document
- External references
- Translation files
- Reintegration scripts

### Rule 3: Adding New Content
When adding new paragraphs between existing ones:

**Option A: Insert with decimal** (Preferred for minor additions)
```markdown
### ID: p9-1
Original paragraph

### ID: p9-1.1
NEW paragraph inserted between p9-1 and p9-2

### ID: p9-2
Next original paragraph
```

**Option B: Renumber** (Only with explicit permission)
Request permission from project owner to renumber all subsequent IDs.

### Rule 4: Deleting Content
When removing a paragraph:
1. **Mark for deletion** (don't delete immediately)
2. Add comment: `<!-- ID p9-5 MARKED FOR DELETION - [reason] -->`
3. Request approval before final deletion
4. After approval, either delete (leaving gap) or renumber with permission

## Markdown Structure

### Section Header
```markdown
# Section [number]: [Title]
```

### Chapter Header
```markdown
## Chapter [number]: [TITLE]
```

### Content with ID
```markdown
### ID: p[chapter]-[number]
Content paragraph here.
```

### Complete Example
```markdown
# Section 4: Introduction

## Chapter 9: WHAT IS RECOVERY DHARMA?

### ID: p9-1
Dharma is a Sanskrit word meaning "truth," "phenomena," or "the nature of things."

### ID: p9-2
The Buddha knew that all human beings struggle with craving.

## Chapter 10: WHERE TO BEGIN

### ID: p10-1
How can we use Buddhism for our recovery?

### ID: p10-2
We come to understand the Four Noble Truths.
```

## JSON Structure Mapping

### Markdown
```markdown
### ID: p9-1
Dharma is a Sanskrit word meaning "truth."
```

### Corresponding JSON
```json
{
  "type": "section",
  "id": 1,
  "heading": "",
  "content": [
    {
      "type": "paragraph",
      "id": "p9-1",
      "text": "Dharma is a Sanskrit word meaning \"truth.\""
    }
  ]
}
```

## ID Update Procedures

### Scenario 1: Fixing Content (No ID Change)
```markdown
# BEFORE
### ID: p9-1
Dharma is a Sanscrit word meaning "truth."

# AFTER
### ID: p9-1
Dharma is a Sanskrit word meaning "truth."
```
✅ Content fixed, ID unchanged - Safe to proceed

### Scenario 2: Adding Content Mid-Chapter
```markdown
# BEFORE
### ID: p9-1
First paragraph.

### ID: p9-2
Third paragraph.

# AFTER - Using decimal notation
### ID: p9-1
First paragraph.

### ID: p9-1.1
NEW second paragraph inserted here.

### ID: p9-2
Third paragraph (originally second).
```
✅ New content added with decimal ID - Safe to proceed
⚠️ Document the addition in commit message

### Scenario 3: Major Restructuring
```markdown
# When restructuring requires renumbering
```
❌ **STOP** - Request permission from project owner first
✅ After permission, document all ID changes in a mapping file

## Validation Checklist

Before committing markdown changes, verify:
- [ ] All IDs follow the p[chapter]-[number] format
- [ ] IDs are sequential within each chapter (allowing for decimals)
- [ ] No existing IDs were changed (unless authorized)
- [ ] New IDs are documented in commit message
- [ ] Deleted content is marked, not removed (unless authorized)

## Common Mistakes to Avoid

❌ Changing ID when fixing typos:
```markdown
# WRONG
### ID: p9-001  # Changed format
Dharma is a Sanskrit word...
```

❌ Skipping numbers:
```markdown
# WRONG
### ID: p9-1
### ID: p9-3  # Missing p9-2
### ID: p9-4
```

❌ Duplicate IDs:
```markdown
# WRONG
### ID: p9-1
First paragraph.

### ID: p9-1  # Duplicate!
Second paragraph.
```

❌ Wrong chapter number:
```markdown
## Chapter 9: WHAT IS RECOVERY DHARMA?

### ID: p10-1  # WRONG - Should be p9-1
```

## Tools and Scripts

### Validation Script
`validate_ids.py` (to be created) - Checks for:
- Duplicate IDs
- Missing sequential numbers
- Format violations
- Chapter/ID mismatches

### Reintegration Script
`reintegrate_markdown.py` - Syncs markdown changes back to JSON:
- Matches IDs between markdown and JSON
- Updates content while preserving structure
- Validates before writing

## Questions?
Contact: scott@farclass.com
