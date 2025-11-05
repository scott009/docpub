# RDG Thai Project  
## Document Production Description — Initial Refinement  
*(Draft v1 — 2025-10-16)*

---

### 1. Cleaning Up the Word Document

**Goal:** Create a clean, machine-readable English base text suitable for structured export.

**Steps:**
- Open the master Word (.docx) file of the book.
- Remove:
  - Extra styles, fonts, and inconsistent paragraph formatting.
  - Headers, footers, and page numbers.
  - Manual line breaks or double spaces within paragraphs.
- Standardize:
  - Section headers (H1, H2, H3) using consistent Word styles.
  - Bullet and numbered lists with Word’s built-in list formatting.
  - Paragraph text as plain “Normal” style.
- Confirm:
  - No hidden tracked changes or comments.
  - Logical order matches the printed sequence.
  - Each chapter and subheading uses consistent heading levels.

This ensures that when exported, the document’s structure can be correctly interpreted by parsers.

---

### 2. Producing Clean, Usable JSON (English)

**Goal:** Convert the cleaned Word document into structured JSON that preserves hierarchy and meaning.

**Method:**
1. Export the Word file to Markdown or HTML as an intermediate step.
2. Use a tool like `python-docx`, `mammoth`, or `pandoc` to parse and structure the content.
3. Define a simple JSON schema, for example:

```json
{
  "metadata": {
    "title": "Recovery Dharma",
    "edition": "English Original",
    "license": "CC BY-SA 4.0",
    "source": "Recovery Dharma Global"
  },
  "chapters": [
    {
      "id": 1,
      "title": "Introduction",
      "sections": [
        {
          "id": 1,
          "heading": "What is Recovery Dharma?",
          "paragraphs": [
            "Recovery Dharma is a community of people who are using Buddhist practices and principles to heal the suffering of addiction."
          ]
        }
      ]
    }
  ]
}
```

**Guidelines:**
- Each paragraph becomes an array element.
- Use plain UTF-8 text with minimal formatting.
- Preserve chapter and section order exactly.
- Validate the JSON with a linter before translation.

---

### 3. Translating English to Thai with Claude Sonnet

**Goal:** Translate the English JSON to Thai while keeping the structure identical.

**Method:**
- Send one chapter at a time to Claude 4.5 Sonnet.
- Use a JSON-preserving prompt such as:  
  *“Translate the English values in this JSON into Thai. Keep the same structure. Return valid JSON.”*

**Recommendation:**  
Include both English and Thai in the same JSON file for clarity and review.

**Example Bilingual JSON:**

```json
{
  "metadata": {
    "title": "Recovery Dharma",
    "edition": "Bilingual EN/TH",
    "license": "CC BY-SA 4.0"
  },
  "chapters": [
    {
      "id": 1,
      "title_en": "Introduction",
      "title_th": "บทนำ",
      "sections": [
        {
          "id": 1,
          "heading_en": "What is Recovery Dharma?",
          "heading_th": "อะไรคือการฟื้นฟูตามหลักธรรมะ",
          "paragraphs": [
            {
              "en": "Recovery Dharma is a community of people who are using Buddhist practices and principles to heal the suffering of addiction.",
              "th": "รีคัฟเวอรีธรรมะคือชุมชนของผู้คนที่ใช้หลักธรรมะและการปฏิบัติแบบพุทธเพื่อเยียวยาความทุกข์จากการเสพติด"
            }
          ]
        }
      ]
    }
  ]
}
```

This bilingual structure allows easy comparison and selective export to Thai-only formats later.

---

### 4. Markdown as a Handoff Format

**Goal:** Provide a readable, editable format for human refinement.

**Why Markdown:**
- Lightweight and easy to read.
- Works with version control (Git, VNote, etc.).
- Maintains section hierarchy with simple syntax.

**Conversion Plan:**
- Export each chapter from JSON to Markdown.
- Include YAML front matter with metadata.
- Present English and Thai sequentially or side-by-side.

**Example Markdown Output:**

```markdown
---
chapter: 1
title_en: "Introduction"
title_th: "บทนำ"
---

## What is Recovery Dharma?
### อะไรคือการฟื้นฟูตามหลักธรรมะ

Recovery Dharma is a community of people who are using Buddhist practices and principles to heal the suffering of addiction.  
รีคัฟเวอรีธรรมะคือชุมชนของผู้คนที่ใช้หลักธรรมะและการปฏิบัติแบบพุทธเพื่อเยียวยาความทุกข์จากการเสพติด
```

**Advantages:**
- Easy to review and edit.
- Compatible with publishing pipelines.
- Simple to convert back to JSON or PDF.

---

*End of Document*
