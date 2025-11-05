const fs = require('fs');
const path = require('path');

// Read the original JSON file
const inq13 = JSON.parse(fs.readFileSync('inq13.json', 'utf8'));

// Find the Weeks section
const weeksSection = inq13.sections.find(section => section.heading === 'Weeks');

// Create a new object with the same structure but only containing the Weeks section
const weeksData = {
  title: inq13.title,
  sections: [weeksSection],
  footnotes: []
};

// Write to weeks13.json
fs.writeFileSync(
  'weeks13.json', 
  JSON.stringify(weeksData, null, 2),
  'utf8'
);

console.log('Successfully created weeks13.json');
