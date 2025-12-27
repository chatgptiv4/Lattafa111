# update-links.ps1
$htmlFiles = Get-ChildItem "c:\Users\HomePC\Desktop\Laffata" -Filter "*.html" -Recurse | Where-Object { $_.FullName -notmatch "\\products\\" }

Write-Host "Updating links in $($htmlFiles.Count) files..."

foreach ($file in $htmlFiles) {
    $content = Get-Content $file.FullName -Raw
    
    # 1. Replace full external URLs: https://www.lattafa-usa.com/products/slug -> /products/slug.html
    # We use a regex to capture the slug and ensure we append .html
    $content = [regex]::Replace($content, 'https://www\.lattafa-usa\.com/products/([a-zA-Z0-9-]+)', '/products/$1.html')
    
    # 2. Replace relative URLs that might miss .html: /products/slug -> /products/slug.html
    # Negative lookahead to avoid replacing if it already ends in .html or " (quote ending)
    # This is tricky. Safer to just replace all /products/slug with /products/slug.html and then fix double .html
    $content = [regex]::Replace($content, 'href="/products/([a-zA-Z0-9-]+)"', 'href="/products/$1.html"')
    
    # 3. Clean up any accidental double extensions from previous regexes if they overlapped
    $content = $content.Replace('.html.html', '.html')
    
    # 4. Also replace the collections/all link to local shop-all.html
    $content = $content.Replace('https://www.lattafa-usa.com/collections/all', '/shop-all.html')
    
    Set-Content -Path $file.FullName -Value $content -Force
}

Write-Host "Link update complete."
