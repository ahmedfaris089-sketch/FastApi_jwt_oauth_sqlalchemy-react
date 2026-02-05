from sqlalchemy import Boolean, Column, Integer, String, Enum, DateTime, ForeignKey, JSON, Text, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import enum
from datetime import datetime

Base = declarative_base()

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    SUPPORT = "support"
    USER = "user"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True, nullable=True)
    full_name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=True)  # Nullable for OAuth users
    role = Column(Enum(UserRole), default=UserRole.USER)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Profile fields
    profile_image_url = Column(String, nullable=True)
    last_active = Column(DateTime, nullable=True)
    phone_number = Column(String, nullable=True)
    telegram_id = Column(String, nullable=True)
    
    # Password reset
    reset_token = Column(String, nullable=True)
    reset_token_expires = Column(DateTime, nullable=True)
    
    # OAuth fields
    oauth_provider = Column(String, nullable=True)  # 'google', etc.
    oauth_id = Column(String, nullable=True)        # Provider's user ID
    
    # Granular permissions (JSON)
    permissions = Column(JSON, nullable=True, default=lambda: {
        "can_view_users": False,
        "can_edit_users": False,
        "can_delete_users": False,
        "can_manage_roles": False
    })

    # Relationships
    sessions = relationship("UserSession", back_populates="user", cascade="all, delete-orphan")
    notifications_read = relationship("NotificationRead", back_populates="user", cascade="all, delete-orphan")


class UserSession(Base):
    """Track user login sessions for analytics"""
    __tablename__ = "user_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    session_date = Column(DateTime, default=datetime.utcnow)  # Date of the session
    login_time = Column(DateTime, default=datetime.utcnow)
    logout_time = Column(DateTime, nullable=True)
    duration_minutes = Column(Float, default=0.0)  # Calculated on logout
    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    
    user = relationship("User", back_populates="sessions")


class ErrorLog(Base):
    """Store application errors and bugs"""
    __tablename__ = "error_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    level = Column(String, default="ERROR")  # ERROR, WARNING, INFO
    message = Column(String, nullable=False)
    stack_trace = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    endpoint = Column(String, nullable=True)
    request_body = Column(Text, nullable=True)
    resolved = Column(Boolean, default=False)
    resolved_at = Column(DateTime, nullable=True)
    resolved_by = Column(Integer, ForeignKey("users.id"), nullable=True)


class NotificationType(str, enum.Enum):
    INFO = "info"
    WARNING = "warning"
    UPDATE = "update"
    NEWS = "news"
    MESSAGE = "message"


class Notification(Base):
    """Admin notifications/messages to users"""
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    type = Column(Enum(NotificationType), default=NotificationType.INFO)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Target audience
    target_role = Column(Enum(UserRole), nullable=True)  # None = all users
    target_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # For direct messages
    
    # Relationships
    reads = relationship("NotificationRead", back_populates="notification", cascade="all, delete-orphan")


class NotificationRead(Base):
    """Track which users have read which notifications"""
    __tablename__ = "notification_reads"

    id = Column(Integer, primary_key=True, index=True)
    notification_id = Column(Integer, ForeignKey("notifications.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    read_at = Column(DateTime, default=datetime.utcnow)
    
    notification = relationship("Notification", back_populates="reads")
    user = relationship("User", back_populates="notifications_read")
