# Catalog Feature - Quick Start Guide

## 🚀 Getting Started

### Step 1: Verify Installation
Your catalog page is ready to use! The following components have been added:

- ✅ Backend route at `/catalog`
- ✅ Image upload handler (16MB max, multiple formats supported)
- ✅ Responsive catalog page with image display
- ✅ Sample data with 5 demo parts
- ✅ Auto-created uploads folder

### Step 2: Access the Catalog
1. Run your Flask app: `python app.py`
2. Click "📦 Parts Catalog" in the navigation menu
3. Or visit: `http://localhost:5000/catalog`

### Step 3: Add Your First Part

#### With Image:
1. Fill in the part details:
   - Part ID: `P006`
   - Part Name: `Transmission Fluid`
   - Category: `Fluids`
   - Price: `15.99`
   - Stock: `25`
   - Description: `Synthetic transmission fluid`

2. Click in the upload area or **drag & drop** an image file
3. Click "Add Part"
4. ✅ Your part now appears with an image!

#### Without Image:
1. Fill in the same details as above
2. Skip the image upload (optional)
3. Click "Add Part"
4. ✅ Part appears with a placeholder 📦 icon

## 📸 Working with Images

### Supported Formats
- PNG (.png)
- JPEG (.jpg, .jpeg)
- GIF (.gif)
- WebP (.webp)

### File Size Limits
- **Maximum**: 16 MB per image
- **Recommended**: 600x600px or larger for best display

### Upload Methods

**Method 1: Click Upload**
```
1. Click on the dotted upload area
2. Select image from your computer
3. Image displays in file input area
```

**Method 2: Drag & Drop**
```
1. Drag image file from your computer
2. Drop it on the upload area
3. Area highlights to show drop zone
4. Image displays in file input area
```

## 🛍️ Catalog Features

### Search
- Type in the "Search Parts" field
- Finds matches in: Part ID, Name, Category, Description
- Real-time search results

### Filter by Category
- Use the "Category" dropdown
- Shows all unique categories from your parts
- Click "Search" to apply filter

### Inventory Management

**View Stock:**
- Color-coded stock badges:
  - 🟢 Green: In Stock (5+ units)
  - 🟠 Orange: Low Stock (1-4 units)
  - 🔴 Red: Out of Stock (0 units)

**Update Stock:**
1. Enter new quantity in the stock input field
2. Click "Update Stock"
3. Quantity updates immediately

**Add to Cart:**
1. Enter desired quantity
2. Click "Add to Cart"
3. Item added to shopping cart (available in Orders section)

### Delete Part
1. Click "Delete" button on the part card
2. Confirm deletion in the dialog
3. Part is removed from catalog

## 📊 Data Storage

### Catalog Data File: `catalog_data.json`
```json
{
  "part_id": "P001",
  "name": "Brake Disc",
  "category": "Brakes",
  "price": 45.99,
  "stock": 15,
  "description": "Premium brake disc for front axle",
  "image": "/static/uploads/P001_brake_disc.jpg"
}
```

### Image Storage: `static/uploads/`
- All images saved here automatically
- Organized by part ID
- Format: `{PART_ID}_{original_filename}`

## 💡 Example Workflow

### Scenario: Adding an Engine Oil Filter with Image

1. **Navigate to Catalog**
   - Click "📦 Parts Catalog" link

2. **Prepare Image**
   - Have an image of the oil filter ready (JPG/PNG)

3. **Fill Form**
   ```
   Part ID:     P010
   Name:        Engine Oil Filter 5W-30
   Category:    Filters
   Price:       $12.50
   Stock:       40
   Description: Premium synthetic engine oil filter
   ```

4. **Upload Image**
   - Drag image to upload area, or
   - Click area and select from computer

5. **Submit**
   - Click "Add Part"
   - Image saves to `static/uploads/P010_engine_oil_filter.jpg`
   - Part displays in catalog with image

6. **Verify**
   - Image appears in product card
   - All details display correctly
   - Can now add to cart or manage stock

## ⚙️ Configuration

### Change Upload Folder
Edit in `app.py` (line ~10):
```python
UPLOAD_FOLDER = os.path.join('static', 'uploads')
```

### Add/Remove Image Formats
Edit in `app.py` (line ~11):
```python
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'svg'}
```

### Change Max File Size
Edit in `app.py` (line ~12):
```python
MAX_CONTENT_LENGTH = 32 * 1024 * 1024  # 32MB instead of 16MB
```

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| Image won't upload | Check file format (.png, .jpg, .gif, .webp only) |
| "File not allowed" error | Verify file extension; rename if needed |
| Image doesn't display | Check if file exists in `static/uploads/` |
| Upload very slow | File might be too large; compress before upload |
| Part not appearing | Try refreshing the page |

## 🔒 Security Features

- ✅ File type validation (only image formats)
- ✅ File size limits (16MB max)
- ✅ Secure filename handling (prevents path traversal)
- ✅ Automatic filename sanitization
- ✅ Part ID prevents duplicate entries

## 📝 Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Search | Start typing in search field |
| Add Part | Fill form and press Enter |
| Submit Form | Click button or Ctrl+Enter |

## 🎨 UI Elements

### Visual Feedback
- **File Upload**: Highlights on hover/drag
- **Part Cards**: Lift effect on hover
- **Buttons**: Color-coded (Primary, Success, Danger)
- **Stock Status**: Color-coded badges

### Responsive Design
- **Desktop**: Multi-column grid layout
- **Tablet**: 2-3 column layout
- **Mobile**: Single column with full-width cards

## 🔄 Integration with Other Sections

The catalog integrates with:

1. **Shopping Cart** (`/orders`)
   - Add parts to cart from catalog
   - Cart updates in real-time

2. **Inventory Management**
   - Stock quantities track availability
   - Can't add out-of-stock items

3. **Navigation Menu**
   - Link in main menu
   - Accessible from all pages

## 📞 Support

For issues or questions, check:
1. **CATALOG_GUIDE.md** - Detailed documentation
2. **IMPLEMENTATION_SUMMARY.md** - Technical details
3. **Sample Data** - In `catalog_data.json`

---

**Enjoy your enhanced catalog with image upload! 🎉**
