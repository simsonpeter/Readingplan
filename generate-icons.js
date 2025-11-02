// Run this in Node.js with canvas package installed
// npm install canvas (requires node-canvas dependencies)

const { createCanvas } = require('canvas');
const fs = require('fs');

function createIcon(size) {
  const canvas = createCanvas(size, size);
  const ctx = canvas.getContext('2d');
  
  // Create gradient background
  const gradient = ctx.createLinearGradient(0, 0, size, size);
  gradient.addColorStop(0, '#667eea');
  gradient.addColorStop(1, '#764ba2');
  ctx.fillStyle = gradient;
  ctx.fillRect(0, 0, size, size);
  
  // Draw cross symbol (white)
  ctx.fillStyle = '#ffffff';
  ctx.font = `bold ${Math.floor(size * 0.6)}px Arial`;
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillText('✝', size / 2, size / 2);
  
  return canvas.toBuffer('image/png');
}

// Generate icons
fs.writeFileSync('icon-192.png', createIcon(192));
fs.writeFileSync('icon-512.png', createIcon(512));
console.log('Icons generated successfully!');

