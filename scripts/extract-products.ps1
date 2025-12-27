# Extract all unique product URLs from HTML files
$htmlFiles = Get-ChildItem "c:\Users\HomePC\Desktop\Laffata\*.html"
$productUrls = @{}

foreach ($file in $htmlFiles) {
    $content = Get-Content $file.FullName -Raw
    # We normalized links to /products/slug.html in the previous step
    $matches = [regex]::Matches($content, '/products/([a-z0-9\-]+)\.html')
    
    foreach ($match in $matches) {
        $productSlug = $match.Groups[1].Value
        if ($productSlug -and -not $productUrls.ContainsKey($productSlug)) {
            $productUrls[$productSlug] = $true
        }
    }
}

# Save to JSON
$productUrls.Keys | Sort-Object | ConvertTo-Json | Out-File "c:\Users\HomePC\Desktop\Laffata\products-list.json"
Write-Host "Found $($productUrls.Count) unique products."
