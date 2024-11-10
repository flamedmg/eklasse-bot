from collections.abc import Sequence
from datetime import datetime
from enum import Enum

from sqlmodel import Field, Relationship, SQLModel


class UserRole(str, Enum):
    PARENT = "parent"
    STUDENT = "student"


class User(SQLModel, table=True):
    """
    Store parent and student information.
    """

    id: int | None = Field(default=None, primary_key=True)
    telegram_id: int = Field(index=True, unique=True)
    role: UserRole
    full_name: str
    email: str | None = None
    phone: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Use immutable Sequence instead of list
    notifications: Sequence["Notification"] = Relationship(back_populates="user")
    schedules: Sequence["Schedule"] = Relationship(back_populates="user")


class Schedule(SQLModel, table=True):
    """
    Store school timetable information.
    """

    id: int | None = Field(default=None, primary_key=True)
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
    """
    Track sent messages.
    """

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    type: NotificationType
    title: str
    content: str
    sent_at: datetime = Field(default_factory=datetime.utcnow)
    is_read: bool = Field(default=False)

    # Relationships
    user: User = Relationship(back_populates="notifications")


class EmailMessage(SQLModel, table=True):
    """
    Store school communications.
    """

    id: int | None = Field(default=None, primary_key=True)
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
                "notification_sent": True,
            }
        }
