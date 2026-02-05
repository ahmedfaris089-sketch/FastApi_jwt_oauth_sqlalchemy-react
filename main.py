from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, get_db, SessionLocal
from models import Base, User, UserRole
from utils import get_password_hash
import config

# ==========================================
# Initialize Database
# ==========================================
Base.metadata.create_all(bind=engine)

# ==========================================
# Initialize FastAPI App
# ==========================================
app = FastAPI(
    title=config.APP_TITLE,
    version=config.APP_VERSION,
    description=config.APP_DESCRIPTION
)

# ==========================================
# CORS Middleware
# ==========================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# Import and Include Routers
# ==========================================
from routes import auth, oauth, profile, password, admin, analytics, notifications, logs

app.include_router(auth.router, tags=["Authentication"])
app.include_router(oauth.router, tags=["OAuth"])
app.include_router(profile.router, tags=["Profile"])
app.include_router(password.router, tags=["Password"])
app.include_router(admin.router, tags=["Admin"])
app.include_router(analytics.router, tags=["Analytics"])
app.include_router(notifications.router, tags=["Notifications"])
app.include_router(logs.router, tags=["Logs"])

# ==========================================
# Root Endpoint
# ==========================================
@app.get("/")
def root():
    return {
        "message": f"{config.APP_TITLE} v{config.APP_VERSION}",
        "docs": "/docs",
        "features": [
            "3 Roles: Admin, Support, User",
            "Granular Permissions",
            "Password Reset (Email/WhatsApp/Telegram)",
            "Google OAuth Login",
            "User Session Analytics",
            "Error Logging",
            "Notification System",
            "Account Enable/Disable"
        ],
        "endpoints": {
            "auth": {
                "signup": "POST /api/signup",
                "login": "POST /api/login",
                "google_login": "GET /api/auth/google",
                "forgot_password": "POST /api/forgot-password",
                "reset_password": "POST /api/reset-password"
            },
            "profile": {
                "get": "GET /api/profile",
                "update": "PUT /api/profile",
                "change_password": "PUT /api/profile/password"
            },
            "notifications": {
                "my_notifications": "GET /api/notifications",
                "mark_read": "PUT /api/notifications/{id}/read"
            },
            "admin": {
                "dashboard": "GET /api/admin",
                "users": "GET /api/admin/users",
                "analytics": "GET /api/admin/analytics",
                "logs": "GET /api/admin/logs",
                "notifications": "GET /api/admin/notifications",
                "toggle_user": "PUT /api/admin/users/{id}/toggle-status"
            }
        }
    }

# ==========================================
# Initialize Default Users
# ==========================================
def init_default_users():
    """Create default users if database is empty"""
    db = SessionLocal()
    try:
        if db.query(User).count() == 0:
            # Create admin with full permissions
            admin = User(
                username=config.DEFAULT_ADMIN_USERNAME,
                email=config.DEFAULT_ADMIN_EMAIL,
                full_name="Administrator",
                hashed_password=get_password_hash(config.DEFAULT_ADMIN_PASSWORD),
                role=UserRole.ADMIN,
                permissions={
                    "can_view_users": True,
                    "can_edit_users": True,
                    "can_delete_users": True,
                    "can_manage_roles": True
                }
            )
            db.add(admin)
            
            # Create support user with limited permissions
            support = User(
                username=config.DEFAULT_SUPPORT_USERNAME,
                email=config.DEFAULT_SUPPORT_EMAIL,
                full_name="Support Agent",
                hashed_password=get_password_hash(config.DEFAULT_SUPPORT_PASSWORD),
                role=UserRole.SUPPORT,
                permissions={
                    "can_view_users": True,
                    "can_edit_users": True,
                    "can_delete_users": False,
                    "can_manage_roles": False
                }
            )
            db.add(support)
            
            # Create regular user
            user = User(
                username=config.DEFAULT_USER_USERNAME,
                email=config.DEFAULT_USER_EMAIL,
                full_name="Regular User",
                hashed_password=get_password_hash(config.DEFAULT_USER_PASSWORD),
                role=UserRole.USER,
                permissions={
                    "can_view_users": False,
                    "can_edit_users": False,
                    "can_delete_users": False,
                    "can_manage_roles": False
                }
            )
            db.add(user)
            
            db.commit()
            print("✅ Default users created:")
            print(f"   - {config.DEFAULT_ADMIN_USERNAME}/{config.DEFAULT_ADMIN_PASSWORD} (Admin)")
            print(f"   - {config.DEFAULT_SUPPORT_USERNAME}/{config.DEFAULT_SUPPORT_PASSWORD} (Support)")
            print(f"   - {config.DEFAULT_USER_USERNAME}/{config.DEFAULT_USER_PASSWORD} (User)")
        else:
            print("✅ Database already initialized")
    finally:
        db.close()

# ==========================================
# Startup Event
# ==========================================
@app.on_event("startup")
def startup_event():
    """Initialize default users on startup"""
    init_default_users()

# ==========================================
# Run Server
# ==========================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)