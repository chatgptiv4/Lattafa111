$products = Get-Content "c:\Users\HomePC\Desktop\Laffata\products-list.json" | ConvertFrom-Json
$generated = Get-ChildItem "c:\Users\HomePC\Desktop\Laffata\products\*.html" | Select-Object -ExpandProperty BaseName

$missing = $products | Where-Object { $generated -notcontains $_ }

Write-Host "Missing Products ($($missing.Count)):"
$missing
