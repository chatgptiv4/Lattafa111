import os
import re
import json

if __name__ == "__main__":
    base_dir = r"c:\Users\HomePC\Desktop\Laffata"
    
    products = []
    seen_urls = set()
    
    # We want to scan all HTML files that are likely product pages.
    # Product pages usually have specific structure. 
    # Valid product pages in this dir seem to be named like 'some-product.html'
    # We exclude known non-product pages.
    
    excluded_files = [
        "index.html", 
        "shop-all.html", 
        "best-sellers.html", 
        "bundles.html", 
        "gift-sets.html", 
        "new-arrivals.html", 
        "track-order.html", 
        "temp_product_analysis.html",
        "product-template.html"
    ]

    print("Scanning directory for product pages...")

    print("Scanning directory for product pages...")
    
    products_dir = os.path.join(base_dir, "products")
    if not os.path.exists(products_dir):
        print(f"Products directory not found: {products_dir}")
        exit(1)

    for filename in os.listdir(products_dir):
        if filename.endswith(".html"):
             filepath = os.path.join(products_dir, filename)
             try:
                 with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                     content = f.read()

                 # Heuristic: Valid product pages usually have a configured product title H1
                 # Regex for Title: <h1 ... class="product__title" ... > Title </h1>
                 
                 title_match = re.search(r'<h1[^>]*class=["\']?product__title["\']?[^>]*>(.*?)</h1>', content, re.DOTALL | re.IGNORECASE)
                 
                 if title_match:
                     title = title_match.group(1).strip()
                     
                     # Simple html tag stripper for title just in case
                     title = re.sub('<[^<]+?>', '', title)
                     
                     # Regex for Price
                     # Looking for <span class="price-item price-item--regular"> ... </span>
                     price_match = re.search(r'class=["\']?price-item[^>]*price-item--regular["\']?[^>]*>\s*([^\s<]+)', content, re.DOTALL | re.IGNORECASE)
                     
                     # Fallback price regex
                     if not price_match:
                         # Look for simple $XX.XX pattern
                         price_match = re.search(r'\$([\d\.]+)', content)
                     
                     price_text = price_match.group(1).strip() if price_match else "0.00"
                     # Clean non-numeric except dot
                     price = re.sub(r'[^0-9.]', '', price_text)
                     if not price: price = "0.00"

                     # Regex for Image
                     # id="mainImage" src="..."
                     img_match = re.search(r'id=["\']?mainImage["\']?[^>]*src=["\']?([^"\'>\s]+)', content, re.IGNORECASE)
                     
                     img_src = ""
                     if img_match:
                         img_src = img_match.group(1).strip()
                         if img_src.startswith('//'):
                             img_src = 'https:' + img_src
                     
                     url = f"/products/{filename}"
                     if url in seen_urls: continue
                     
                     products.append({
                         'name': title,
                         'url': url,
                         'price': price,
                         'image': img_src
                     })
                     seen_urls.add(url)
                     print(f"Indexed: {title} ({price})")
             except Exception as e:
                 print(f"Skipping {filename}: {e}")

    output_path = os.path.join(base_dir, 'products.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=2)
    print(f"Done. Indexed {len(products)} items to products.json.")
