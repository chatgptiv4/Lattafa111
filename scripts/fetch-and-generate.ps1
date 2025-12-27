# fetch-and-generate.ps1

# Configuration
$productsListPath = "c:\Users\HomePC\Desktop\Laffata\products-list.json"
$templatePath = "c:\Users\HomePC\Desktop\Laffata\product-template.html"
$outputProductsDir = "c:\Users\HomePC\Desktop\Laffata\products"
$assetsDir = "c:\Users\HomePC\Desktop\Laffata\assets\products"

# Create directories
if (-not (Test-Path $outputProductsDir)) { New-Item -ItemType Directory -Path $outputProductsDir | Out-Null }
if (-not (Test-Path $assetsDir)) { New-Item -ItemType Directory -Path $assetsDir | Out-Null }

# Load data
$products = Get-Content $productsListPath | ConvertFrom-Json
$template = Get-Content $templatePath -Raw

Write-Host "Starting extraction for $($products.Count) products..."
$count = 0
$skipped = 0

foreach ($slug in $products) {
    $outputPath = Join-Path $outputProductsDir "$slug.html"
    
    # Resuming logic disabled to force template update
    # if (Test-Path $outputPath) { ... }

    Write-Host "Processing [$count/$($products.Count)]: $slug"
    
    # 1. Fetch HTML
    $url = "https://www.lattafa-usa.com/products/$slug"
    try {
        $html = Invoke-WebRequest -Uri $url -UseBasicParsing
        $content = $html.Content
    } catch {
        Write-Warning "Failed to fetch $url : $_"
        $count++
        continue
    }

    # 2. Extract JSON data
    # Patterns to look for: _BISConfig.product = {...} or just var meta = {...}
    
    $jsonMatch = [regex]::Match($content, '_BISConfig\.product\s*=\s*(\{.*?\});', [System.Text.RegularExpressions.RegexOptions]::Singleline)
    
    if (-not $jsonMatch.Success) {
        Write-Warning "Could not find product JSON for $slug"
        $count++
        continue
    }
    
    $jsonStr = $jsonMatch.Groups[1].Value
    try {
        $productData = $jsonStr | ConvertFrom-Json
    } catch {
        Write-Warning "Failed to parse JSON for $slug"
        $count++
        continue
    }

    # 3. Prepare Data
    $title = $productData.title
    $description = $productData.description
    
    # Fix for proper USD formatting with escaped dollar sign
    $price = [math]::Round($productData.price / 100, 2)
    $priceStr = "`$$price USD" 
    
    $variantId = $productData.variants[0].id
    
    # 4. Handle Images
    $productAssetsDir = Join-Path $assetsDir $slug
    if (-not (Test-Path $productAssetsDir)) { New-Item -ItemType Directory -Path $productAssetsDir | Out-Null }

    $images = $productData.images
    $localImagePaths = @()
    
    $imgCount = 0
    foreach ($imgUrl in $images) {
        # Clean URL (remove query params for filename)
        if ($imgUrl -match "^//") { $imgUrl = "https:$imgUrl" }
        
        $filename = "$imgCount.jpg" # Simplify filenames to avoid long paths/chars
        $localPath = Join-Path $productAssetsDir $filename
        $relPath = "/assets/products/$slug/$filename"
        
        # Download if not exists
        if (-not (Test-Path $localPath)) {
            try {
                # Add slight delay to be polite
                Start-Sleep -Milliseconds 100
                Invoke-WebRequest -Uri $imgUrl -OutFile $localPath
            } catch {
                Write-Warning "Failed to download image $imgUrl"
            }
        }
        
        if (Test-Path $localPath) {
            $localImagePaths += $relPath
            $imgCount++
        }
    }

    # 5. Generate HTML
    $mainImage = if ($localImagePaths.Count -gt 0) { $localImagePaths[0] } else { "/assets/placeholder.jpg" }
    
    # Generate thumbnails HTML
    $thumbnailsHtml = ""
    $i = 0
    foreach ($img in $localImagePaths) {
        $activeClass = if ($i -eq 0) { "active" } else { "" }
        $thumbnailsHtml += "<div class='thumbnail $activeClass' onclick='changeImage(`"$img`", this)'><img src='$img' alt='$title'></div>"
        $i++
    }

    # Replace placeholders
    # Use explicit string replacement to avoid regex special char issues with content
    $pageContent = $template.Replace('{{PRODUCT_TITLE}}', $title)
    $pageContent = $pageContent.Replace('{{PRODUCT_PRICE}}', $priceStr)
    $pageContent = $pageContent.Replace('{{PRODUCT_DESCRIPTION_HTML}}', $description)
    $pageContent = $pageContent.Replace('{{MAIN_IMAGE}}', $mainImage)
    $pageContent = $pageContent.Replace('{{THUMBNAILS_HTML}}', $thumbnailsHtml)
    $pageContent = $pageContent.Replace('{{VARIANT_ID}}', $variantId)
    
    # Save file
    Set-Content -Path $outputPath -Value $pageContent -Force

    $count++
}

Write-Host "Completed. Processed $count products ($skipped skipped)."
