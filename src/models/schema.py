from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
from enum import Enum


class UserRole(str, Enum):
    PARENT = "parent"
    STUDENT = "student"


class User(SQLModel, table=True):
    """User model for storing parent and student information."""
    
    id: Optional[int] = Field(default=None, primary_key=True)
    telegram_id: int = Field(index=True, unique=True)
    role: UserRole
    full_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    notifications: list["Notification"] = Relationship(back_populates="user")
    schedules: list["Schedule"] = Relationship(back_populates="user")


class Schedule(SQLModel, table=True):
    """Schedule model for storing school timetables."""
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    subject: str
    teacher: str
    classroom: str
    start_time: datetime
    end_time: datetime
    day_of_week: int  # 0-6 for Monday-Sunday
    is_active: bool = Field(default=True)
    
    # Relationships
    user: User = Relationship(back_populates="schedules")


class NotificationType(str, Enum):
    SCHEDULE = "schedule"
    EMAIL = "email"
    REMINDER = "reminder"
    ANNOUNCEMENT = "announcement"


class Notification(SQLModel, table=True):
    """Notification model for tracking sent messages."""
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    type: NotificationType
    title: str
    content: str
    sent_at: datetime = Field(default_factory=datetime.utcnow)
    is_read: bool = Field(default=False)
    
    # Relationships
    user: User = Relationship(back_populates="notifications")


class EmailMessage(SQLModel, table=True):
    """Email message model for storing school communications."""
    
    id: Optional[int] = Field(default=None, primary_key=True)
    sender: str
    recipient: str
    subject: str
    content: str
    received_at: datetime = Field(default_factory=datetime.utcnow)
    processed: bool = Field(default=False)
    notification_sent: bool = Field(default=False)
    
    class Config:
        schema_extra = {
            "example": {
                "sender": "teacher@school.com",
                "recipient": "parent@example.com",
                "subject": "Homework Assignment",
                "content": "Please complete pages 10-12 for tomorrow.",
                "received_at": "2024-01-20T10:00:00",
                "processed": True,
                "notification_sent": True
            }
        }
