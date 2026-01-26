# User Access Control Matrix

## Route Access Permissions

| Feature | Route | Admin | User | Unauthenticated |
|---------|-------|:-----:|:----:|:---------------:|
| **Job Cards** |  |  |  |  |
| View Job Cards | `/` | ✅ VIEW, EDIT, DELETE | ✅ VIEW ONLY | ❌ REDIRECT |
| Edit Job Card | `/update/<id>` | ✅ ALLOWED | ❌ DENIED | ❌ REDIRECT |
| Delete Job Card | `/delete/<id>` | ✅ ALLOWED | ❌ DENIED | ❌ REDIRECT |
| **Rewards Management** |  |  |  |  |
| View Rewards | `/rewards` | ✅ ALLOWED | ❌ DENIED | ❌ REDIRECT |
| Redeem Reward | `/rewards/redeem/<id>` | ✅ ALLOWED | ❌ DENIED | ❌ REDIRECT |
| **Parts Catalogue** |  |  |  |  |
| View Catalogue | `/catalogue` | ✅ VIEW & EDIT | ✅ VIEW ONLY | ❌ REDIRECT |
| Add Part | `/catalogue` (POST) | ✅ ALLOWED | ❌ DENIED | ❌ REDIRECT |
| Edit Part | `/catalogue/edit/<id>` | ✅ ALLOWED | ❌ DENIED | ❌ REDIRECT |
| Delete Part | `/catalogue` (POST) | ✅ ALLOWED | ❌ DENIED | ❌ REDIRECT |
| Export Catalogue | `/catalogue/export` | ✅ ALLOWED | ❌ DENIED | ❌ REDIRECT |
| Import Catalogue | `/catalogue/import` | ✅ ALLOWED | ❌ DENIED | ❌ REDIRECT |
| **Orders** |  |  |  |  |
| View Orders | `/orders` | ✅ ALLOWED | ❌ DENIED | ❌ REDIRECT |
| Edit Order | `/orders/edit/<id>` | ✅ ALLOWED | ❌ DENIED | ❌ REDIRECT |
| Delete Order | `/orders/delete/<id>` | ✅ ALLOWED | ❌ DENIED | ❌ REDIRECT |
| **Authentication** |  |  |  |  |
| Login | `/login` | ✅ ALLOWED | ✅ ALLOWED | ✅ ALLOWED |
| Register | `/register` | ✅ ALLOWED | ✅ ALLOWED | ✅ ALLOWED |
| Profile | `/profile` | ✅ ALLOWED | ✅ ALLOWED | ❌ REDIRECT |
| Logout | `/logout` | ✅ ALLOWED | ✅ ALLOWED | ✅ REDIRECT |

---

## Navigation Menu Visibility

### When Logged Out
- Login
- Register

### When Logged In as User
- Home (View job cards)
- Catalogue (View only)
- Profile
- Logout

### When Logged In as Admin
- Home (Full control)
- Rewards (Full control)
- Catalogue (Full control)
- Orders (Full control)
- Profile
- Logout

---

## Decorators Applied

```python
@login_required      # User must be logged in
@admin_required      # User must be logged in AND have admin role
@user_required       # User must be logged in AND NOT be admin
```

### Route Decorators:

```
/ (home)                     → @login_required
/update/<job_id>             → @admin_required
/delete/<job_id>             → @admin_required
/rewards                     → @admin_required
/rewards/redeem/<customer>   → @admin_required
/catalogue                   → @login_required
/catalogue/edit/<part_id>    → @admin_required
/catalogue/export            → @admin_required
/catalogue/import            → @admin_required
/orders                      → @admin_required
/orders/delete/<order_id>    → @admin_required
/orders/edit/<order_id>      → @admin_required

/login                       → (No decorator)
/register                    → (No decorator)
/profile                     → (No decorator, but checks session)
/logout                      → (No decorator)
```

---

## Session Data

When user logs in, these values are stored in `session`:

```python
session['user_id']    # User ID (int)
session['username']   # Username (string)
session['role']       # Role: 'admin' or 'user' (string)
```

---

## Error Handling

| Scenario | Behavior |
|----------|----------|
| Access restricted route without login | Redirect to `/login` with "Please login first" message |
| User tries admin-only route | Redirect to `/` with "Admin privileges required" message |
| Invalid login credentials | Stay on `/login` with "Invalid username or password" message |
| Empty registration fields | Stay on `/register` with validation message |
| Duplicate username on register | Stay on `/register` with "Username already exists" message |

---

## Security Features

✅ Password hashing (werkzeug.security)
✅ Session-based authentication
✅ Role-based authorization
✅ CSRF token ready (Flask-WTF compatible)
✅ Secure logout (session clearing)
✅ Input validation
✅ Email validation on registration
✅ Password confirmation on registration
✅ Minimum password length (6 characters)

---

## Demo Accounts for Testing

### Admin Account
- Username: `admin`
- Password: `admin123`
- Email: `admin@example.com`
- Role: `admin`

### Regular User Account
- Username: `testuser`
- Password: `password123`
- Email: `testuser@example.com`
- Role: `user`

---

## Creating New Users

Users can self-register at `/register` or can be added to `users_data.json` manually:

```json
{
  "id": 3,
  "username": "newuser",
  "email": "newuser@example.com",
  "password": "[hashed_password]",
  "role": "user",
  "created_at": "2026-01-27T12:00:00"
}
```

Use Python to generate hashed passwords:
```python
from werkzeug.security import generate_password_hash
hashed = generate_password_hash("password123")
print(hashed)
```
