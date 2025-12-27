import os

# Root files
files = [
    "index.html",
    "best-sellers.html",
    "bundles.html",
    "gift-sets.html",
    "new-arrivals.html",
    "shop-all.html",
    "track-order.html"
]

script_tag = '<script src="js/lattafa_search.js"></script>'
base_dir = r"c:\Users\HomePC\Desktop\Laffata"

def inject_script(filepath, relative_js_path="js/lattafa_search.js"):
    if not os.path.exists(filepath):
        print(f"Skipping {filepath}, not found")
        return

    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # check if already exists
    if "lattafa_search.js" in content:
        print(f"Already injected in {filepath}")
        return

    # Injection logic: Before </body>
    if "</body>" in content:
        # Use exact tag to inject script
        # Adjusted for relative path
        tag_to_insert = f'<script src="{relative_js_path}"></script>\n'
        new_content = content.replace("</body>", tag_to_insert + "</body>")
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Injected into {filepath}")
    else:
        print(f"No body tag in {filepath}")

# Process root files
for file in files:
    inject_script(os.path.join(base_dir, file), "js/lattafa_search.js")

# Process product pages
products_dir = os.path.join(base_dir, "products")
if os.path.exists(products_dir):
    for filename in os.listdir(products_dir):
        if filename.endswith(".html"):
             # For products in subfolder, path to js is ../js/lattafa_search.js
             inject_script(os.path.join(products_dir, filename), "../js/lattafa_search.js")
