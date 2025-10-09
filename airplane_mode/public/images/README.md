# Images Directory

This directory contains image assets for the Airplane Mode application.

## Files Structure

- `favicon.ico` - Website favicon
- `logo.png` - Application logo
- `splash.png` - Splash screen image
- `icons/` - Various icon files

## Usage

Images are served from `/assets/airplane_mode/images/` path.

## Adding New Images

1. Add image files to this directory
2. Reference them in templates using: `/assets/airplane_mode/images/filename.ext`
3. Run `bench build --app airplane_mode` to update assets
