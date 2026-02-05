from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, List
from datetime import datetime
from models import UserRole, NotificationType

class UserBase(BaseModel):
    username: str

class UserSignup(UserBase):
    password: str
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    role: Optional[UserRole] = UserRole.USER

class UserLogin(BaseModel):
    username: str
    password: str

class PasswordUpdate(BaseModel):
    old_password: str
    new_password: str

# Forgot Password Schemas
class ForgotPasswordRequest(BaseModel):
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    channel: str = "email"  # email, whatsapp, telegram

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

# User Update (Admin)
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    telegram_id: Optional[str] = None
    profile_image_url: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None

# Permissions Update
class PermissionsUpdate(BaseModel):
    can_view_users: bool = False
    can_edit_users: bool = False
    can_delete_users: bool = False
    can_manage_roles: bool = False

class UserResponse(UserBase):
    id: int
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    role: UserRole
    is_active: bool
    created_at: datetime
    profile_image_url: Optional[str] = None
    last_active: Optional[datetime] = None
    phone_number: Optional[str] = None
    telegram_id: Optional[str] = None
    permissions: Optional[Dict] = None
    oauth_provider: Optional[str] = None

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[UserRole] = None

# ==========================================
# Session Tracking Schemas
# ==========================================

class SessionStart(BaseModel):
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None

class SessionResponse(BaseModel):
    id: int
    user_id: int
    session_date: datetime
    login_time: datetime
    logout_time: Optional[datetime] = None
    duration_minutes: float
    
    class Config:
        from_attributes = True

class UserAnalytics(BaseModel):
    user_id: int
    username: str
    total_sessions: int
    total_time_minutes: float
    average_session_minutes: float
    sessions_by_date: Dict[str, float]  # date -> total minutes

# ==========================================
# Error Log Schemas
# ==========================================

class ErrorLogCreate(BaseModel):
    level: str = "ERROR"
    message: str
    stack_trace: Optional[str] = None
    endpoint: Optional[str] = None
    request_body: Optional[str] = None

class ErrorLogResponse(BaseModel):
    id: int
    timestamp: datetime
    level: str
    message: str
    stack_trace: Optional[str] = None
    user_id: Optional[int] = None
    endpoint: Optional[str] = None
    resolved: bool
    resolved_at: Optional[datetime] = None
    resolved_by: Optional[int] = None
    
    class Config:
        from_attributes = True

# ==========================================
# Notification Schemas
# ==========================================

class NotificationCreate(BaseModel):
    title: str
    message: str
    type: NotificationType = NotificationType.INFO
    target_role: Optional[UserRole] = None  # None = all users
    target_user_id: Optional[int] = None    # For direct messages

class NotificationResponse(BaseModel):
    id: int
    title: str
    message: str
    type: NotificationType
    created_by: int
    created_at: datetime
    target_role: Optional[UserRole] = None
    target_user_id: Optional[int] = None
    is_read: bool = False
    
    class Config:
        from_attributes = True

class NotificationWithCreator(NotificationResponse):
    creator_name: Optional[str] = None

# ==========================================
# Plant Schemas (legacy)
# ==========================================

class PlantBase(BaseModel):
    name: str
    species: Optional[str] = None
    image_url: Optional[str] = None
    watering_frequency_days: int = 7

class PlantCreate(PlantBase):
    pass

class PlantResponse(PlantBase):
    id: int
    last_watered_date: datetime
    owner_id: int

    class Config:
        from_attributes = True
