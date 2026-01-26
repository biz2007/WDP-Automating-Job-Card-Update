# WDP Job Card Management System - Authentication & Role-Based Access Setup

## Overview
The system now has a complete authentication and authorization layer with two user roles: **Admin** and **User**. The UI is consistent across all pages using the dark theme design system.

---

## Authentication Implementation

### Files Created/Modified:

#### 1. **auth.py** (New)
Simplified authentication module with:
- User registration with validation
- User login with password hashing
- User logout
- User profile view
- JSON-based user storage (users_data.json)

**Demo Credentials:**
- Admin: `admin` / `admin123` (Role: admin)
- User: `testuser` / `password123` (Role: user)

#### 2. **decorators.py** (New)
Role-based access control decorators:
- `@login_required` - Requires user to be logged in
- `@admin_required` - Requires admin privileges
- `@user_required` - Restricts to regular users only

#### 3. **app.py** (Updated)
- Imports auth blueprint and decorators
- Registers auth blueprint for `/login`, `/register`, `/logout`, `/profile` routes
- Applied decorators to all routes based on role requirements

---

## Role-Based Access Control

### Admin Capabilities ✅
- ✅ View all job cards
- ✅ Create new job cards
- ✅ Update/edit job cards
- ✅ Delete job cards
- ✅ View parts catalogue
- ✅ Add/edit/delete parts from catalogue
- ✅ Update stock levels
- ✅ View rewards and redemptions
- ✅ Manage orders (view, edit, delete, change status)
- ✅ Access admin panel in navigation

### User Capabilities ✅
- ✅ View job cards (read-only)
- ✅ View parts catalogue
- ✅ Login with personal account
- ✅ View profile information
- ✅ Logout

### Routes & Decorators Applied:

| Route | Decorator | Access |
|-------|-----------|--------|
| `/` (home) | `@login_required` | View job cards (Create/Update/Delete restricted to admin) |
| `/update/<job_id>` | `@admin_required` | Admin only |
| `/delete/<job_id>` | `@admin_required` | Admin only |
| `/rewards` | `@admin_required` | Admin only |
| `/rewards/redeem/<customer_id>` | `@admin_required` | Admin only |
| `/catalogue` | `@login_required` | All logged-in users can view |
| `/catalogue/edit/<part_id>` | `@admin_required` | Admin only |
| `/catalogue/export` | `@admin_required` | Admin only |
| `/catalogue/import` | `@admin_required` | Admin only |
| `/orders` | `@admin_required` | Admin only |
| `/orders/edit/<order_id>` | `@admin_required` | Admin only |
| `/orders/delete/<order_id>` | `@admin_required` | Admin only |

---

## Templates Updated

### 1. **base.html**
- Added responsive navbar with user session display
- Role-based navigation items (Rewards & Orders only show for admins)
- Flash message system for notifications
- Consistent dark theme styling (CSS variables)

### 2. **login.html**
- Clean login form
- Link to registration page
- Demo credentials displayed for testing

### 3. **register.html**
- User registration form
- Email validation
- Password confirmation
- Link back to login

### 4. **profile.html**
- User profile information display
- Role badge (ADMIN/USER)
- Member since date
- Profile and logout buttons

### 5. **index.html**
- Job card management interface
- Role-aware UI:
  - Admins see: Create form, Edit, Delete buttons
  - Users see: View-only job cards (read-only)
- Search functionality
- Status badges with color coding

---

## User Data Storage

### users_data.json
Stores user accounts with encrypted passwords:
```json
[
  {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "password": "[hashed]",
    "role": "admin",
    "created_at": "ISO-8601 timestamp"
  },
  ...
]
```

---

## Session Management

Session variables stored:
- `session['user_id']` - User ID
- `session['username']` - Username
- `session['role']` - User role (admin/user)

---

## UI Consistency

All pages use the same design system:
- **Primary Background**: `#1a2238`
- **Secondary Background**: `#232946`
- **Accent Color**: `#ff6a3d` (Orange)
- **Action Color**: `#4dd4fa` (Cyan)
- **Danger Color**: `#ea445a` (Red)
- **Success Color**: `#19a974` (Green)

---

## Testing Guide

### Test Admin Account:
1. Go to `http://localhost:5000/login`
2. Username: `admin`
3. Password: `admin123`
4. You'll have full access to all admin features

### Test Regular User Account:
1. Go to `http://localhost:5000/login`
2. Username: `testuser`
3. Password: `password123`
4. You'll only see job cards and catalogue (read-only)

### Redirection Logic:
- ✅ Unlogged users → Redirected to login page
- ✅ Users without permissions → Redirected to home with danger message
- ✅ On login → Redirected to home page
- ✅ On logout → Redirected to login page

---

## Security Features

- ✅ Password hashing using werkzeug.security
- ✅ Session-based authentication
- ✅ Role-based authorization decorators
- ✅ CSRF protection ready (Flask-WTF compatible)
- ✅ Input validation on registration
- ✅ Secure logout with session clearing

---

## Requirements

```
Flask==3.1.2
Werkzeug==3.1.4
Jinja2==3.1.6
openpyxl (for Excel export/import)
```

---

## How to Run

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py

# Application will be available at http://localhost:5000
```

---

## Additional Features

- ✅ User registration system
- ✅ Profile viewing
- ✅ Session timeout handling
- ✅ Flash messages for user feedback
- ✅ Mobile-responsive design
- ✅ Dark theme UI
- ✅ Role badges in navigation

---

## Next Steps (Optional Enhancements)

- [ ] Add email verification for registration
- [ ] Add password reset functionality
- [ ] Add user activity logging
- [ ] Add admin user management panel
- [ ] Add two-factor authentication
- [ ] Database migration (SQLite → PostgreSQL)

---

Generated: 2026-01-27
