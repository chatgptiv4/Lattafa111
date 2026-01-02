
import re

def search_text():
    file = "index.html"
    try:
        with open(file, 'rb') as f:
            content = f.read().decode('utf-8', errors='ignore')
            
            # Regex for Shop All with whitespace flexibility
            pattern = re.compile(r'>\s*Shop\s+All\s*<', re.IGNORECASE)
            
            matches = pattern.finditer(content)
            found = False
            for m in matches:
                found = True
                print(f"Found '{m.group()}' at index {m.start()}")
                start = max(0, m.start() - 100)
                end = min(len(content), m.end() + 100)
                print(f"pContext: ...{content[start:end]}...")
                print("-" * 20)
                
            if not found:
                print("No 'Shop All' found. Trying just 'Shop'...")
                pattern = re.compile(r'>\s*Shop\s*<', re.IGNORECASE)
                matches = pattern.finditer(content)
                for m in matches:
                    print(f"Found '{m.group()}' at index {m.start()}")
                    start = max(0, m.start() - 100)
                    end = min(len(content), m.end() + 100)
                    print(f"Context: ...{content[start:end]}...")
                    print("-" * 20)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    search_text()
