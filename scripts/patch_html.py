
filepath = r'c:\Users\HomePC\Desktop\Laffata\shop-all.html'
with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Replace <div</div> with nothing?
# Or maybe it should be </div>?
# Verification:
# If current state is balanced (using loose counting), then removing it makes it balanced (using strict counting).
# Loose: 15 Opens, 15 Closes.
# Strict: 14 Opens, 15 Closes. (Excess Close)
# Removing "<div</div>": 14 Opens, 14 Closes. (Balanced)
# Correct!

new_content = content.replace('<div</div>', '')

# Also check for space
new_content = new_content.replace('<div </div>', '')

if content != new_content:
    print("Patched malformed tags.")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
else:
    print("No malformed tags found to patch.")
