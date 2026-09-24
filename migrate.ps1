$ErrorActionPreference = "Stop"

# Create directories
New-Item -ItemType Directory -Force -Path "frontend\pages"
New-Item -ItemType Directory -Force -Path "frontend\components"
New-Item -ItemType Directory -Force -Path "frontend\services"
New-Item -ItemType Directory -Force -Path "frontend\assets"
New-Item -ItemType Directory -Force -Path "frontend\styles"
New-Item -ItemType Directory -Force -Path "frontend\utils"
New-Item -ItemType Directory -Force -Path "frontend\config"

# Move files
Move-Item -Path "views\*" -Destination "frontend\pages\" -Force
Move-Item -Path "utils\*" -Destination "frontend\utils\" -Force
Move-Item -Path "app.py" -Destination "frontend\app.py" -Force

# Clean up old directories
Remove-Item -Path "views" -Recurse -Force
Remove-Item -Path "utils" -Recurse -Force
Remove-Item -Path "components" -Recurse -Force
