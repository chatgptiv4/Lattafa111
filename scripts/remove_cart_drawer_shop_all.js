const fs = require('fs');
const path = require('path');

const filePath = path.join(__dirname, 'shop-all.html');
const startLine = 11369; // 1-based
const endLine = 11641;   // 1-based

fs.readFile(filePath, 'utf8', (err, data) => {
    if (err) {
        console.error('Error reading file:', err);
        return;
    }

    const lines = data.split('\n');
    const before = lines.slice(0, startLine - 1);
    const after = lines.slice(endLine);

    const newContent = [...before, '<!-- Cart Drawer Removed via Script -->', ...after].join('\n');

    fs.writeFile(filePath, newContent, 'utf8', (err) => {
        if (err) {
            console.error('Error writing file:', err);
        } else {
            console.log('Successfully removed Cart Drawer section from shop-all.html');
        }
    });
});
