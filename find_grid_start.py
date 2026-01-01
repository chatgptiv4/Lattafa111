
filepath = r'c:\Users\HomePC\Desktop\Laffata\shop-all.html'
with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if '24 Carat White Gold' in line:
        print(f"First product found at line {i+1}")
        # Look backwards for the UL or DIV container
        for j in range(i, i-50, -1):
            if '<ul' in lines[j] or '<div class="grid' in lines[j]:
                print(f"Possible container start at line {j+1}: {lines[j].strip()}")
        break
