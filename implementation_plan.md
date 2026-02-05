# Backend Refactoring Plan

## Goal
Refactor the monolithic `main.py` into a clean, modular structure with separate files for routes, and create a centralized configuration file for all settings.

## Current Structure Issues
- `main.py` is 900+ lines (too large)
- All routes in one file
- Configuration scattered across files
- Hard to maintain and navigate

## Proposed Structure

```
files/
├── config.py                 # All configuration (OAuth, domains, admin, Telegram)
├── database.py               # ✅ Already exists
├── models.py                 # ✅ Already exists
├── schemas.py                # ✅ Already exists
├── utils.py                  # ✅ Already exists
├── email_service.py          # ✅ Already exists
├── main.py                   # FastAPI app + route imports
├── routes/
│   ├── __init__.py
│   ├── auth.py               # Login, signup, logout, verify
│   ├── oauth.py              # Google OAuth routes
│   ├── profile.py            # User profile management
│   ├── password.py           # Forgot/reset password
│   ├── admin.py              # Admin user management
│   ├── analytics.py          # Session analytics
│   ├── notifications.py      # Notification system
│   └── logs.py               # Error logging
└── .env                      # ✅ Already exists (secrets)
```

---

## Proposed Changes

### 1. Create `config.py`
Centralized configuration file for all non-secret settings.

**Contents:**
```python
# OAuth Configuration
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8000/api/auth/google/callback")

# Domain Configuration
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# Admin Configuration
DEFAULT_ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_EMAIL = "admin@example.com"
DEFAULT_ADMIN_PASSWORD = "admin123"

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# Email Configuration (already in .env, just reference)
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")

# WhatsApp Configuration
WHATSAPP_API_URL = os.getenv("WHATSAPP_API_URL", "")
WHATSAPP_API_KEY = os.getenv("WHATSAPP_API_KEY", "")

# Security
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# CORS
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:3001",
    FRONTEND_URL
]
```

---

### 2. Create Route Files

#### [NEW] `routes/__init__.py`
Empty file to make routes a package.

#### [NEW] `routes/auth.py`
**Routes:**
- `POST /api/signup` - User registration
- `POST /api/login` - User login
- `GET /api/verify` - Token verification
- `POST /api/session/end` - End session

#### [NEW] `routes/oauth.py`
**Routes:**
- `GET /api/auth/google` - Redirect to Google
- `GET /api/auth/google/callback` - Handle OAuth callback

#### [NEW] `routes/profile.py`
**Routes:**
- `GET /api/profile` - Get user profile
- `PUT /api/profile` - Update profile

#### [NEW] `routes/password.py`
**Routes:**
- `PUT /api/profile/password` - Change password
- `POST /api/forgot-password` - Request reset
- `POST /api/reset-password` - Reset password

#### [NEW] `routes/admin.py`
**Routes:**
- `GET /api/admin` - Admin dashboard
- `GET /api/admin/users` - List users
- `GET /api/admin/users/active` - Active users
- `PUT /api/admin/users/{id}` - Update user
- `DELETE /api/admin/users/{id}` - Delete user
- `PUT /api/admin/users/{id}/permissions` - Update permissions
- `PUT /api/admin/users/{id}/role` - Update role
- `PUT /api/admin/users/{id}/toggle-status` - Enable/disable

#### [NEW] `routes/analytics.py`
**Routes:**
- `GET /api/admin/analytics` - Overall analytics
- `GET /api/admin/analytics/{user_id}` - User analytics

#### [NEW] `routes/notifications.py`
**Routes:**
- `POST /api/admin/notifications` - Create notification
- `GET /api/notifications` - Get my notifications
- `PUT /api/notifications/{id}/read` - Mark as read
- `GET /api/admin/notifications` - List all notifications

#### [NEW] `routes/logs.py`
**Routes:**
- `POST /api/log/error` - Log error
- `GET /api/admin/logs` - Get error logs
- `PUT /api/admin/logs/{id}/resolve` - Resolve error

---

### 3. Update `main.py`
Simplified main file that imports all routes.

**Structure:**
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, SessionLocal
from models import Base
import config

# Create tables
Base.metadata.create_all(bind=engine)

# Initialize app
app = FastAPI(title="Pro JWT Auth System", version="4.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and include routers
from routes import auth, oauth, profile, password, admin, analytics, notifications, logs

app.include_router(auth.router, tags=["Authentication"])
app.include_router(oauth.router, tags=["OAuth"])
app.include_router(profile.router, tags=["Profile"])
app.include_router(password.router, tags=["Password"])
app.include_router(admin.router, tags=["Admin"])
app.include_router(analytics.router, tags=["Analytics"])
app.include_router(notifications.router, tags=["Notifications"])
app.include_router(logs.router, tags=["Logs"])

# Root endpoint
@app.get("/")
def root():
    return {...}

# Initialize default users
@app.on_event("startup")
def startup():
    init_default_users()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

### 4. Update `.env` File
Add all new configuration variables:

```env
# Existing
SECRET_KEY=your-secret-key-here
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Google OAuth
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret
GOOGLE_REDIRECT_URI=http://localhost:8000/api/auth/google/callback

# Domains
FRONTEND_URL=http://localhost:3000
BACKEND_URL=http://localhost:8000

# Telegram Bot
TELEGRAM_BOT_TOKEN=your-bot-token
TELEGRAM_CHAT_ID=your-chat-id

# WhatsApp (optional)
WHATSAPP_API_URL=
WHATSAPP_API_KEY=
```

---

## Verification Plan

### 1. Code Organization
- [ ] All route files created in `routes/` folder
- [ ] `config.py` created with all settings
- [ ] `main.py` simplified to ~100 lines
- [ ] All imports working correctly

### 2. Functionality Testing
- [ ] Login/signup still works
- [ ] Google OAuth still works
- [ ] Admin panel accessible
- [ ] Analytics endpoints work
- [ ] Notifications work
- [ ] Error logging works
- [ ] Profile updates work
- [ ] Password reset works

### 3. Configuration
- [ ] `.env` file updated with all variables
- [ ] `config.py` loads all settings correctly
- [ ] No hardcoded values in route files

---

## Benefits

1. **Maintainability**: Each file has a single responsibility
2. **Readability**: Easy to find specific routes
3. **Scalability**: Easy to add new routes
4. **Configuration**: All settings in one place
5. **Testing**: Easier to test individual route modules
6. **Collaboration**: Multiple developers can work on different route files
