#!/bin/bash

# Create missing image assets for Airplane Mode
# Run this script to generate placeholder images and icons

echo "🎨 Creating missing image assets for Airplane Mode..."
echo "=================================================="

# Check if we're in the right directory
if [ ! -d "airplane_mode/public/images" ]; then
    echo "❌ Error: Please run this script from the frappe app root directory"
    echo "   Expected: airplane_mode/public/images directory"
    exit 1
fi

# Create images directory if it doesn't exist
mkdir -p airplane_mode/public/images/icons

echo "📁 Creating image directory structure..."

# Create a simple favicon using SVG (since we can't upload binary files via GitHub)
cat > airplane_mode/public/images/favicon.svg << 'EOF'
<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">
  <rect width="32" height="32" fill="#007bff"/>
  <path d="M8 16 L16 8 L24 16 L20 16 L20 24 L12 24 L12 16 Z" fill="white"/>
  <circle cx="16" cy="20" r="2" fill="#007bff"/>
</svg>
EOF

# Create logo SVG
cat > airplane_mode/public/images/logo.svg << 'EOF'
<svg xmlns="http://www.w3.org/2000/svg" width="200" height="60" viewBox="0 0 200 60">
  <rect width="200" height="60" fill="#2c3e50" rx="5"/>
  <text x="10" y="35" font-family="Arial, sans-serif" font-size="24" font-weight="bold" fill="white">✈️ Airport</text>
  <text x="10" y="50" font-family="Arial, sans-serif" font-size="12" fill="#bdc3c7">Management System</text>
</svg>
EOF

# Create splash image SVG
cat > airplane_mode/public/images/splash.svg << 'EOF'
<svg xmlns="http://www.w3.org/2000/svg" width="400" height="300" viewBox="0 0 400 300">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#667eea;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#764ba2;stop-opacity:1" />
    </linearGradient>
  </defs>
  <rect width="400" height="300" fill="url(#bgGrad)"/>
  <text x="200" y="120" text-anchor="middle" font-family="Arial, sans-serif" font-size="36" font-weight="bold" fill="white">✈️ Airplane Mode</text>
  <text x="200" y="160" text-anchor="middle" font-family="Arial, sans-serif" font-size="18" fill="white" opacity="0.9">Airport Management System</text>
  <text x="200" y="200" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" fill="white" opacity="0.7">Streamlined operations for modern airports</text>
</svg>
EOF

# Instructions for favicon.ico
cat > airplane_mode/public/images/FAVICON_INSTRUCTIONS.md << 'EOF'
# Favicon Instructions

## Converting SVG to ICO

The favicon.svg file has been created as a placeholder. To create a proper favicon.ico file:

### Method 1: Online Converter
1. Go to https://favicon.io/favicon-converter/
2. Upload the `favicon.svg` file
3. Download the generated `favicon.ico`
4. Replace `favicon.svg` with `favicon.ico`

### Method 2: Using ImageMagick (if installed)
```bash
# Convert SVG to ICO (requires ImageMagick)
convert airplane_mode/public/images/favicon.svg airplane_mode/public/images/favicon.ico
```

### Method 3: Using Online Tools
- https://convertio.co/svg-ico/
- https://cloudconvert.com/svg-to-ico
- https://www.icoconverter.com/

## PNG Logos

Similarly, you can convert the SVG logos to PNG:

```bash
# Convert to PNG (requires ImageMagick)
convert airplane_mode/public/images/logo.svg airplane_mode/public/images/logo.png
convert airplane_mode/public/images/splash.svg airplane_mode/public/images/splash.png
```

## Custom Images

Replace these placeholder images with your custom designs:
- Use your airport's logo for `logo.svg/png`
- Create a branded favicon that matches your theme
- Design a splash screen that represents your application

## Image Specifications

- **Favicon**: 32x32px or 16x16px, ICO format preferred
- **Logo**: 200x60px recommended, PNG format
- **Splash**: 400x300px recommended, PNG/JPG format
EOF

echo "✅ Created SVG placeholders:"
echo "   - favicon.svg"
echo "   - logo.svg" 
echo "   - splash.svg"
echo ""
echo "📖 See FAVICON_INSTRUCTIONS.md for converting to proper formats"
echo ""

# Update hooks.py to handle missing files gracefully
echo "🔧 Updating asset references..."

# Create a .gitkeep file for the icons directory
touch airplane_mode/public/images/icons/.gitkeep

echo "✅ Asset creation completed!"
echo ""
echo "🎯 Next steps:"
echo "1. Convert SVG files to appropriate formats (PNG, ICO)"
echo "2. Run: bench build --app airplane_mode --force"
echo "3. Run: bench clear-cache && bench restart"
echo "4. Test asset loading on your website"
echo ""
echo "💡 Tip: Use the favicon converter at https://favicon.io for best results"
