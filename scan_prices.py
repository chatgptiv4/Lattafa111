
encoding = 'utf-8'
filepath = r'c:\Users\HomePC\Desktop\Laffata\shop-all.html'
products = [
    "Asad",
    "Yara",
    "Qaed Al Fursan",
    "Badee Al Oud Noble Blush",
    "Khamrah"
]

found_products = {}

with open(filepath, 'r', encoding=encoding, errors='ignore') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    for p in products:
        # Check specifically for product title context to avoid menu links
        # e.g. <a ...>Asad</a> or similar, or just distinct matches
        # The file showed: <a class="reversed-link" href="/products/khamrah.html">Khamrah</a>
        if p in line and "reversed-link" in line:
            # We found a product title card
            found_products[p] = i
            print(f"Found {p} at line {i+1}")

            # Now look ahead for price
            for j in range(i, i + 50):
                if j < len(lines) and 'class="f-price-item f-price-item--regular"' in lines[j]:
                    # This is the price line (or close to it)
                    print(f"  Price for {p} starts around line {j+1}")
                    print(f"  Content: {lines[j+1].strip()}")
                    break
