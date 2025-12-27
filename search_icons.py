
keywords = ["/account/login", "icon-user", "header__icon--account", "fa-user", "account", "Login", "svg", "href="]
files = ["index.html"]

for file in files:
    try:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read() # Read as whole string
            
            for kw in keywords:
                idx = content.find(kw)
                if idx != -1: # Only print if found
                    print(f"Found '{kw}' at index {idx}")
                    # Print surrounding chars
                    start = max(0, idx - 100)
                    end = min(len(content), idx + 300)
                    print(f"Context: ...{content[start:end]}...")
                    print("-" * 20)
    except Exception as e:
        print(f"Error: {e}")
