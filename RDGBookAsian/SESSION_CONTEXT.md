# Session Context for RDGBookAsian Project

**Last Updated**: 2025-11-07
**Repository**: https://github.com/scott009/RDGBookAsian
**Current Branch**: claude/rdg-asian-master-setup-011CUtTgXHAgHdwcMFgSfCSA

## Project Overview
**Goal**: Produce the final accepted version of RDGAsianMaster.json through collaborative editing and translation work.

**Master File**: `RDGBookAsian/RDGAsianMaster.json`
- This is the AUTHORITATIVE source of truth
- All changes must eventually be reintegrated back to this file
- Contains 8 sections, 32 chapters

## Current File Structure
```
RDGBookAsian/
├── RDGAsianMaster.json              # MASTER FILE - authoritative source
├── section1_title_legal_dedication.json
├── section1_title_legal_dedication_english.md
├── section2_table_of_contents.json
├── section2_table_of_contents_english.md
├── section3_preface.json
├── section3_preface_english.md
├── section4_introduction.json
├── section4_introduction_english.md
├── section5_truths_and_paths.json
├── section5_truths_and_paths_english.md
├── section6_community.json
├── section6_community_english.md
├── section7_recovery_is_possible.json
├── section7_recovery_is_possible_english.md
├── section8_personal_stories.json
└── section8_personal_stories_english.md
```

## Workflow

### 1. Markdown Editing
- Edit `section*_english.md` files in online markdown editors (StackEdit.io, HackMD, etc.)
- GitHub's built-in editor can also be used
- Files are structured with IDs (e.g., p9-1, p9-2)

### 2. ID Management
- IDs follow pattern: `p[chapter]-[number]`
- Example: `p9-1` = Chapter 9, section 1
- See ID_SPECIFICATION.md for detailed rules

### 3. Reintegration
- After markdown approval, changes must be merged back to RDGAsianMaster.json
- Use reintegration script (to be created)
- Never manually edit JSON unless absolutely necessary

## Active Work
**Current Focus**: Setting up collaborative workflow and documentation

**Recent Completion**:
- Extracted 8 sections from RDGAsianMaster.json
- Created English markdown versions for all sections
- Translations for Chapter 9 in Thai, Vietnamese, Korean, Japanese, Chinese (Traditional & Simplified), Tibetan

## For New AI Assistants Picking Up This Work
1. Read this file first
2. Read COLLABORATION_GUIDE.md
3. Review Status.md for project history
4. Check RDGAsianMaster_structure.md for content structure
5. Read operations-guide.md for development guardrails
6. Always work on the designated branch: `claude/rdg-asian-master-setup-011CUtTgXHAgHdwcMFgSfCSA`
7. NEVER mark tasks complete without explicit user confirmation

## Key Contacts
- **Project Owner**: scott@farclass.com
- **Repository**: https://github.com/scott009/RDGBookAsian

## Important Notes
- Work should be done primarily in GitHub (online)
- Minimize local computer work
- Collaborators may use different AI assistants
- All collaborators must be trained before access
- Repository may become private for access control

## Next Steps Queue
1. Complete workflow documentation
2. Create ID specification document
3. Build reintegration script
4. Set up online markdown editing integration
5. Create collaborator onboarding process
