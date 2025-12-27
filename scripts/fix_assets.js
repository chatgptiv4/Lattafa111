const fs = require('fs');
const path = require('path');

const files = ["shop-all.html", "new-arrivals.html", "best-sellers.html", "gift-sets.html", "bundles.html", "track-order.html", "index.html"];

files.forEach(file => {
    const filePath = path.join(__dirname, file);
    if (!fs.existsSync(filePath)) return;

    let content = fs.readFileSync(filePath, 'utf8');

    // 1. Remove duplicate adapter.css (keep the first one in <head>, remove any others)
    const cssRegex = /<link rel="stylesheet" href="css\/adapter.css">/g;
    let matchCount = 0;
    content = content.replace(cssRegex, (match) => {
        matchCount++;
        return matchCount === 1 ? match : '';
    });

    // 2. Ensure Stripe.js is present exactly once before lattafa_adapter.js
    const stripeScript = '<script src="https://js.stripe.com/v3/"></script>';
    const adapterScript = '<script src="js/lattafa_adapter.js"></script>';

    // Remove all existing Stripe scripts to avoid duplicates
    content = content.replace(/<script src="https:\/\/js\.stripe\.com\/v3\/"><\/script>/g, '');

    // Insert it before adapter script
    content = content.replace(adapterScript, stripeScript + '\n  ' + adapterScript);

    fs.writeFileSync(filePath, content, 'utf8');
    console.log(`Updated ${file}`);
});
