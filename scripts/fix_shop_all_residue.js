const fs = require('fs');
const path = require('path');

const filePath = path.join(__dirname, 'shop-all.html');
const startLine = 11370; // 1-based
const endLine = 11392;   // 1-based

fs.readFile(filePath, 'utf8', (err, data) => {
    if (err) {
        console.error('Error reading file:', err);
        return;
    }

    const lines = data.split('\n');
    const before = lines.slice(0, startLine - 1);
    const after = lines.slice(endLine);

    // We don't need a replacement comment, just remove it (maybe add a comment if needed, but we already have one above)
    const newContent = [...before, ...after].join('\n');

    fs.writeFile(filePath, newContent, 'utf8', (err) => {
        if (err) {
            console.error('Error writing file:', err);
        } else {
            console.log('Successfully removed residual Cart Drawer section from shop-all.html');
        }
    });
});
