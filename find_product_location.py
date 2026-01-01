
filepath = r'c:\Users\HomePC\Desktop\Laffata\shop-all.html'
with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")
for i, line in enumerate(lines):
    if '24 Carat White Gold' in line:
        print(f"Match at line {i+1}: {line.strip()[:100]}...")
        # Look around for context
        for j in range(max(0, i-20), min(len(lines), i+10)):
            print(f"{j+1}: {lines[j].strip()[:100]}")
        break
