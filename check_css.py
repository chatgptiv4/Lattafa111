
filepath = r'c:\Users\HomePC\Desktop\Laffata\css\style.css'
with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

classes = ['.discount-badge', '.price-new', '.price-old', '.product-price-container']
for c in classes:
    if c in content:
        print(f"Found {c}")
    else:
        print(f"Missing {c}")
