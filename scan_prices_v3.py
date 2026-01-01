
import os

filepath = r'c:\Users\HomePC\Desktop\Laffata\best-sellers.html'
targets = {
    "asad.html": "Asad",
    "yara.html": "Yara",
    "qaed-al-fursan-unlimited.html": "Qaed Al Fursan",
    "badee-al-oud-noble-blush.html": "Badee Al Oud",
    "khamrah.html": "Khamrah"
}

with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

with open(r'c:\Users\HomePC\Desktop\Laffata\matches_utf8.txt', 'w', encoding='utf-8') as out:
    for i, line in enumerate(lines):
        for url_part, name in targets.items():
            if url_part in line:
                out.write(f"MATCH: {name} at line {i+1}\n")
                # Look ahead for price
                found_price = False
                for j in range(i, i + 100): # Increased lookahead
                    if j < len(lines):
                        if 'f-price-item--regular' in lines[j]:
                             price_line_idx = j + 1
                             if price_line_idx < len(lines):
                                 price_value = lines[price_line_idx].strip()
                                 out.write(f"  PRICE_LINE_INDEX: {price_line_idx + 1}\n")
                                 out.write(f"  PRICE_VALUE: {price_value}\n")
                                 found_price = True
                                 break
                if not found_price:
                    out.write("  Price not found in next 100 lines.\n")
