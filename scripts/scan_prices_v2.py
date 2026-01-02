
import os

filepath = r'c:\Users\HomePC\Desktop\Laffata\shop-all.html'
targets = {
    "asad.html": "Asad",
    "yara.html": "Yara",
    "qaed-al-fursan-unlimited.html": "Qaed Al Fursan",
    "badee-al-oud-noble-blush.html": "Badee Al Oud",
    "khamrah.html": "Khamrah"
}

with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    for url_part, name in targets.items():
        if url_part in line:
            print(f"MATCH: {name} at line {i+1}")
            # Look ahead for price
            found_price = False
            for j in range(i, i + 40):
                if j < len(lines):
                    # Check for price class
                    if 'f-price-item--regular' in lines[j]:
                         # The price is usually on the NEXT line or inside this line
                         # In the file viewed:
                         # <span class="f-price-item f-price-item--regular">
                         #   $49.99 USD
                         # </span>
                         # So lines[j] is the span tag, lines[j+1] is the price.
                         price_line_idx = j + 1
                         price_value = lines[price_line_idx].strip()
                         print(f"  PRICE_LINE_INDEX: {price_line_idx + 1}") # 1-based
                         print(f"  PRICE_VALUE: {price_value}")
                         found_price = True
                         break
            if not found_price:
                print("  Price not found in next 40 lines.")
