# Catalog Page with Image Upload Feature

## Overview
The enhanced catalog page now supports uploading and displaying images for each part in your inventory.

## Features

### 📷 Image Upload
- **Upload images** when adding new parts (PNG, JPG, GIF, WebP supported)
- **Drag & drop** support for easy file selection
- **Image validation** - ensures only valid image formats are accepted
- **Size limit** - maximum 16MB per image
- **Automatic organization** - images are saved with part IDs for easy tracking

### 📦 Part Management
- **Add new parts** with complete details including images
- **Update stock** quantities directly from catalog
- **Delete parts** with confirmation
- **Search functionality** across part names, IDs, categories, and descriptions
- **Filter by category** for easier browsing
- **Image display** in cards with fallback placeholder if no image

### 🛒 Shopping Integration
- **Add to cart** directly from catalog
- **Stock status indicators** (In Stock, Low Stock, Out of Stock)
- **Real-time stock display** and management

## How to Use

### Adding a Part with Image

1. Navigate to the **Parts Catalog** page
2. Fill in the part details:
   - **Part ID** (required) - e.g., P001
   - **Part Name** (required) - e.g., Brake Disc
   - **Category** (required) - e.g., Brakes
   - **Price** (required) - e.g., 45.99
   - **Stock** (required) - quantity available
   - **Description** (optional) - detailed info

3. **Upload an image**:
   - Click on the upload area or drag & drop an image
   - Supported formats: PNG, JPG, GIF, WebP
   - Maximum file size: 16MB

4. Click **Add Part** to save

### Managing Inventory

**Update Stock:**
- Enter new stock quantity and click "Update Stock"

**Delete Part:**
- Click "Delete" and confirm the action

**Search & Filter:**
- Use the search bar to find parts by name, ID, category, or description
- Filter by category using the dropdown menu

### Image Storage

Images are automatically saved to: `static/uploads/`

File naming convention: `{PART_ID}_{original_filename}`

Example: `P001_brake_disc.jpg`

## Data Structure

### Catalog Data File
Location: `catalog_data.json`

```json
[
  {
    "part_id": "P001",
    "name": "Brake Disc",
    "category": "Brakes",
    "price": 45.99,
    "stock": 15,
    "description": "Premium brake disc for front axle",
    "image": "/static/uploads/P001_brake_disc.jpg"
  }
]
```

## Technical Details

### Backend (app.py)
- New route: `/catalog` (GET and POST)
- Handles image uploads with file validation
- Stores images in `static/uploads/` folder
- Prevents duplicate part IDs
- Manages catalog CRUD operations

### Frontend (catalog.html)
- Responsive grid layout with image cards
- Drag & drop file upload interface
- Client-side file selection feedback
- Image display with fallback placeholder (📦)
- Integrated shopping cart functionality

### Allowed File Types
- PNG (.png)
- JPEG (.jpg, .jpeg)
- GIF (.gif)
- WebP (.webp)

## Configuration

### Upload Settings (in app.py)
- **UPLOAD_FOLDER**: `static/uploads/`
- **MAX_CONTENT_LENGTH**: 16 MB (16 * 1024 * 1024 bytes)
- **ALLOWED_EXTENSIONS**: png, jpg, jpeg, gif, webp

To modify these settings, edit the configuration at the top of `app.py`:

```python
UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
```

## Tips & Best Practices

1. **Image Quality**: Use appropriately sized images (recommended: 600x600px or larger)
2. **File Names**: Keep image file names simple without special characters
3. **Organization**: Images are automatically organized by part ID
4. **Backup**: Consider backing up the `static/uploads/` folder regularly
5. **Performance**: Large images may impact page load time; optimize before upload

## Troubleshooting

### Image not displaying
- Ensure the image file was successfully uploaded
- Check that the image format is supported
- Verify the file exists in `static/uploads/`

### Upload fails
- Check file size (must be under 16MB)
- Confirm file format is allowed
- Ensure `static/uploads/` folder exists and is writable

### "File not allowed" error
- Verify the file has a supported extension (.png, .jpg, .jpeg, .gif, .webp)
- Check filename doesn't contain special characters

## Future Enhancements

Potential improvements for the catalog:
- Image cropping/resizing before upload
- Multiple images per part
- Image gallery/lightbox view
- Image optimization and compression
- Bulk image upload
- Image editing tools
