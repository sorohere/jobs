const fs = require('fs');
const path = require('path');

const dataDir = '/Users/soro/Documents/projects/rough-work/soro-ass/data/divide_02/';
const outputFile = 'jobs.json';
let merged = [];

fs.readdirSync(dataDir).forEach(file => {
  if (file.endsWith('.json')) {
    const filePath = path.join(dataDir, file);
    try {
      const content = JSON.parse(fs.readFileSync(filePath, 'utf8'));
      if (Array.isArray(content)) {
        merged.push(...content);
      }
    } catch (e) {
      console.log(`⚠️ Skipping malformed file: ${file}`);
    }
  }
});

console.log(`✅ Merged ${merged.length} job entries`);
fs.writeFileSync(outputFile, JSON.stringify(merged, null, 2));
console.log(`📁 Final dataset saved to ${outputFile}`);
