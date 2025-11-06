const fs = require('fs');
const path = require('path');

// Read the master JSON file
const masterFile = path.join(__dirname, 'RDGAsianMaster.json');
const data = JSON.parse(fs.readFileSync(masterFile, 'utf8'));

// Function to convert title to filename
function titleToFilename(title) {
  return title
    .trim()
    .replace(/\s+/g, '_')  // Replace spaces with underscores
    .replace(/[^a-zA-Z0-9_-]/g, '')  // Remove special characters
    .replace(/_+/g, '_');  // Replace multiple underscores with single
}

// Extract metadata
const metadata = data.metadata;

// Create output directory for sections
const outputDir = path.join(__dirname, 'sections');
if (!fs.existsSync(outputDir)) {
  fs.mkdirSync(outputDir);
}

// Process each top-level section
data.content.forEach((section) => {
  if (section.type === 'section' && section.title) {
    // Create a new JSON object for this section
    const sectionData = {
      metadata: {
        ...metadata,
        section_id: section.id,
        section_title: section.title,
        extracted_from: 'RDGAsianMaster.json',
        extraction_date: new Date().toISOString().split('T')[0]
      },
      section: section
    };

    // Generate filename
    const filename = titleToFilename(section.title) + '.json';
    const filepath = path.join(outputDir, filename);

    // Write the file
    fs.writeFileSync(filepath, JSON.stringify(sectionData, null, 2), 'utf8');
    console.log(`Created: ${filename} (Section ID: ${section.id})`);
  }
});

console.log('\nAll sections have been split successfully!');
console.log(`Output directory: ${outputDir}`);
