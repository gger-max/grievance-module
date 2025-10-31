# Typebot Avatar Setup Guide

## Problem
Typebot Builder is not accepting the Vaka Sosiale logo as an avatar upload.

## Solutions

### Solution 1: Resize the Logo (Recommended)

Typebot may have size/dimension restrictions for avatar images. Try these steps:

1. **Resize the logo** to avatar-friendly dimensions:
   - Recommended size: 200x200 pixels (square)
   - Max file size: 50KB or less
   - Format: PNG with transparency

2. **Tools to resize**:
   - Online: Use https://squoosh.app or https://tinypng.com
   - Or use an image editor like GIMP, Photoshop, or Paint.NET

3. **Upload steps**:
   - Go to http://localhost:8081
   - Open "Grievance Intake" bot
   - Click **Settings** → **Theme**
   - Under **Chat** section, find **Host avatar**
   - Upload the resized logo
   - Save and Publish

### Solution 2: Use a URL Instead of Upload

If upload fails, try providing a URL:

1. Upload the logo to MinIO manually:
   - Go to http://localhost:9001 (MinIO Console)
   - Login: minioadmin / minioadmin
   - Navigate to `grievance-attachments` bucket
   - Create a folder called `public`
   - Upload `vaka-sosiale-logo.png`
   - Make it public (set permissions)
   - Copy the public URL

2. In Typebot Theme settings:
   - Instead of uploading, paste the URL
   - Example: `http://localhost:9000/grievance-attachments/public/vaka-sosiale-logo.png`

### Solution 3: Convert to Smaller Format

Try converting to a smaller, optimized PNG:

```bash
# If you have ImageMagick installed:
magick convert vaka-sosiale-logo.png -resize 200x200 -quality 85 vaka-logo-small.png
```

Or use online tools:
- https://imageresizer.com
- https://compressor.io

### Solution 4: Use SVG Format

If Typebot accepts SVG:

1. Convert PNG to SVG using an online tool
2. Upload the SVG file instead

### Solution 5: Manual JSON Edit (Advanced)

If all else fails, you can edit the Typebot export JSON:

1. Upload logo to a publicly accessible URL
2. Edit `frontend-typebot/typebot-export-grievance-intake.json`
3. Find the `"theme":{}` section
4. Add avatar configuration:
   ```json
   "theme": {
     "chat": {
       "hostAvatar": {
         "url": "http://localhost:9000/grievance-attachments/public/vaka-logo-small.png"
       }
     }
   }
   ```
5. Re-import the bot or update via database

## Current Avatar Location

The logo file is located at:
- `backend/app/static/vaka-sosiale-logo.png` (102KB)
- Original: `docs/images/VAKA SOCIALE_final_NEW.png`

## Troubleshooting

**If Typebot shows an error:**
- File too large (reduce to <50KB)
- Wrong format (use PNG or JPG)
- Dimensions too large (resize to 200x200 or 300x300)
- CORS issues (ensure URL is accessible)

**If avatar doesn't appear:**
- Clear browser cache
- Re-publish the bot
- Check browser console for errors
- Verify image URL is accessible in browser

## Need Help?

If you continue to have issues, please provide:
1. The exact error message from Typebot
2. Screenshot of the upload interface
3. Browser console errors (F12 → Console tab)
