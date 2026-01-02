
import os
import shutil
import json

base_dir = r'c:\Users\HomePC\Desktop\Laffata'
updates_dir = os.path.join(base_dir, 'UPDATESS')
assets_dir = os.path.join(base_dir, 'assets', 'products')

mappings = {
    'Lattafa Choco': 'choco-overdose',
    'Lattafa Berry': 'berry-on-top',
    'Lattafa Vanilla': 'vanilla-freak',
    'Lattafa Cookies': 'cookie-crave',
    'Lattafa Whipped': 'whipped-pleasure'
}

products_info = []

for src_name, slug in mappings.items():
    src_path = os.path.join(updates_dir, src_name)
    dest_path = os.path.join(assets_dir, slug)
    
    if not os.path.exists(dest_path):
        os.makedirs(dest_path)
        print(f"Created {dest_path}")
    
    if os.path.exists(src_path):
        files = [f for f in os.listdir(src_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        # Sort to ensure consistent ordering if needed, though random is fine for now
        files.sort()
        
        for i, filename in enumerate(files):
            # We want 0.jpg, 1.jpg etc.
            # Convert to jpg if it's not (though mostly just renaming extension is risky if format differs, but usually browsers handle renamed jpegs fine. WhatsApp images are jpegs).
            new_name = f"{i}.jpg"
            shutil.copy2(os.path.join(src_path, filename), os.path.join(dest_path, new_name))
            print(f"Copied {filename} to {slug}/{new_name}")
            
    # Prepare JSON data snippet
    products_info.append({
        "name": f"Lattafa {slug.replace('-', ' ').title()} Give me Gourmand collection EDP 75ml Spray",
        "url": f"/products/{slug}.html",
        "price": "45.00", # Discounted price
        "image": f"/assets/products/{slug}/0.jpg",
        "description_file": "TODO" 
    })

print("JSON Snippet:")
print(json.dumps(products_info, indent=2))
