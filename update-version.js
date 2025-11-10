#!/usr/bin/env node

/**
 * Helper script to update app-version.json when content files change
 * Usage: node update-version.js [version]
 * Example: node update-version.js 1.0.1
 */

const fs = require('fs');
const path = require('path');

// Get version from command line or increment patch version
const args = process.argv.slice(2);
let newVersion = args[0];

// Read current version
const versionFile = path.join(__dirname, 'app-version.json');
let versionData = {};

if (fs.existsSync(versionFile)) {
  versionData = JSON.parse(fs.readFileSync(versionFile, 'utf8'));
}

// If no version provided, increment patch version
if (!newVersion) {
  const currentVersion = versionData.version || '1.0.0';
  const parts = currentVersion.split('.');
  parts[2] = (parseInt(parts[2]) + 1).toString();
  newVersion = parts.join('.');
}

// Update version data
versionData.version = newVersion;
versionData.lastUpdated = new Date().toISOString();

// Update lastModified for each content file
const contentFiles = [
  'plan/njcplan.json',
  'bibles/tamilbible.json',
  'bibles/englishbible.json',
  'bibles/dutchbible.json',
  'bibles/tamilromanizedbible.json',
  'dictionary/TSVPA1975.dictionary.SQLite3'
];

contentFiles.forEach(file => {
  const filePath = path.join(__dirname, file);
  if (fs.existsSync(filePath)) {
    const stats = fs.statSync(filePath);
    if (!versionData.contentFiles) {
      versionData.contentFiles = {};
    }
    if (!versionData.contentFiles[file]) {
      versionData.contentFiles[file] = {};
    }
    versionData.contentFiles[file].lastModified = stats.mtime.toISOString();
    // Update version if not set
    if (!versionData.contentFiles[file].version) {
      versionData.contentFiles[file].version = newVersion;
    }
  }
});

// Write updated version file
fs.writeFileSync(versionFile, JSON.stringify(versionData, null, 2));

console.log(`✅ Updated app-version.json to version ${newVersion}`);
console.log(`📅 Last updated: ${versionData.lastUpdated}`);

