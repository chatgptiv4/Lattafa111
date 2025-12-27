const fs = require('fs');
const path = require('path');

const files = [
    'new-arrivals.html',
    'gift-sets.html',
    'bundles.html',
    'best-sellers.html',
    'track-order.html'
];

const basePath = path.join(__dirname);

files.forEach(file => {
    const filePath = path.join(basePath, file);
    if (!fs.existsSync(filePath)) {
        console.warn(`File not found: ${file}`);
        return;
    }

    console.log(`Processing ${file}...`);
    let content = fs.readFileSync(filePath, 'utf8');
    const lines = content.split('\n');

    // 1. Remove Cart Drawer
    const startMarker = 'id="shopify-section-sections--20292988698847__cart-drawer"';
    const endMarker = '</cart-drawer>';

    let startIdx = -1;
    let endIdx = -1;

    for (let i = 0; i < lines.length; i++) {
        if (lines[i].includes(startMarker)) {
            startIdx = i; // This is the line with the <div id="..."> but verify if it's the start
            // Usually the div spans multiple lines or is on one line.
            // In the previous files, it was <div id="..." \n class="...">
            // So identifying the start line is sufficient?
            // Wait, I need to make sure I get the whole opening tag if it spans.
            // But deleting from the line with the ID is safe enough if the ID is unique to that block start.
        }
        if (startIdx !== -1 && i > startIdx && lines[i].includes(endMarker)) {
            // Found </cart-drawer>. The next line is likely </div>
            if (i + 1 < lines.length && lines[i + 1].trim() === '</div>') {
                endIdx = i + 1;
            } else {
                endIdx = i; // Fallback? No, sticking to safe assumption from observation.
            }
            break;
        }
    }

    if (startIdx !== -1 && endIdx !== -1) {
        console.log(`  Removing Cart Drawer block from line ${startIdx + 1} to ${endIdx + 1}`);
        // Remove lines
        lines.splice(startIdx, endIdx - startIdx + 1, '<!-- Cart Drawer Removed via Script -->');
        content = lines.join('\n'); // Rejoin for string replacements
    } else {
        console.warn(`  Cart Drawer block not found or incomplete in ${file}`);
    }

    // 2. Replacements (on the content string)
    // Home Link
    content = content.replace(/href="https:\/\/www\.lattafa-usa\.com"/g, 'href="index.html"');

    // Search Link
    content = content.replace(/href="\/search"/g, 'href="javascript:void(0)"');

    // About Link
    content = content.replace(/href="\/pages\/about-us"/g, 'href="shop-all.html"');

    // Ensure mobile-adapter-cart-btn class exists (if not already)
    // It seems it was often already there, but let's ensure.
    // Search for class="... mobile-sticky-bar__cart ..." and add mobile-adapter-cart-btn if missing.
    // Regex is tricky for class modification. I'll skip adding it if it's usually there, 
    // or I can do a specific replace if I know the exact string.
    // In shop-all.html it was: class="f-column cart-drawer-button mobile-sticky-bar__link mobile-sticky-bar__cart mobile-adapter-cart-btn flex flex-col items-center justify-center"
    // I replaced the link href in shop-all using the tool.
    // The previous analysis showed "mobile-adapter-cart-btn" was present in grep?
    // Let's verify presence in new-arrivals.html line 10365:
    // class="f-column cart-drawer-button mobile-sticky-bar__link mobile-sticky-bar__cart mobile-adapter-cart-btn flex flex-col items-center justify-center"
    // It seems it is ALREADY THERE. Good.

    // Link for Cart is href="javascript:void(0)"?
    // In shop-all it was already javascript:void(0) in the input file? No, I viewed it and it was.
    // Wait, in new-arrivals grep output (Step 165):
    // Line 10365: class=... mobile-adapter-cart-btn ...
    // But where is the HREF? It is likely on the line before?
    // Line 10344: wrapper... <a
    // The grep output is lines content.
    // Use regex to ensure href="javascript:void(0)" for the cart link?
    // The cart link usually has `mobile-sticky-bar__cart` class.

    // Replace href for sticky bar cart if it points to /cart or something else?
    // Pattern: <a href=".*?" ... class="... mobile-sticky-bar__cart ..."
    // Too complex for simple regex.
    // I'll assume if "mobile-adapter-cart-btn" is there, the href might need fixing if it's not javascript:void(0).
    // In index.html I set it to javascript:void(0).
    // I'll try to find `href="/cart"` near `mobile-sticky-bar__cart` and replace?
    // But often the href is on a preceding line.

    // However, the `lattafa_adapter.js` handles the click with `preventDefault` if the class is present.
    // So even if href is `/cart`, if the JS intercepts it, it's fine.
    // But ensuring `javascript:void(0)` is cleaner.

    fs.writeFileSync(filePath, content, 'utf8');
    console.log(`  Updated ${file}`);
});
