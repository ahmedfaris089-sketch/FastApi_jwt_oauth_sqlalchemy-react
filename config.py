import os
from typing import List

# ==========================================
# OAuth Configuration
# ==========================================
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8000/api/auth/google/callback")

# ==========================================
# Domain Configuration
# ==========================================
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# ==========================================
# Admin Configuration
# ==========================================
DEFAULT_ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_EMAIL = "admin@example.com"
DEFAULT_ADMIN_PASSWORD = "admin123"

DEFAULT_SUPPORT_USERNAME = "support"
DEFAULT_SUPPORT_EMAIL = "support@example.com"
DEFAULT_SUPPORT_PASSWORD = "support123"

DEFAULT_USER_USERNAME = "user"
DEFAULT_USER_EMAIL = "user@example.com"
DEFAULT_USER_PASSWORD = "user123"

# ==========================================
# Telegram Bot Configuration
# ==========================================
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# ==========================================
# Email Configuration
# ==========================================
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")

# ==========================================
# WhatsApp Configuration
# ==========================================
WHATSAPP_API_URL = os.getenv("WHATSAPP_API_URL", "")
WHATSAPP_API_KEY = os.getenv("WHATSAPP_API_KEY", "")

# ==========================================
# Security Configuration
# ==========================================
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# ==========================================
# CORS Configuration
# ==========================================
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:3001",
    FRONTEND_URL,
]

# ==========================================
# Application Configuration
# ==========================================
APP_TITLE = "Pro JWT Auth System"
APP_VERSION = "4.0.0"
APP_DESCRIPTION = "Advanced authentication system with analytics, notifications, and OAuth"
