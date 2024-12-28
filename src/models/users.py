
from .base import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean

class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    password_hash: Mapped[str] = mapped_column(String(100), nullable=False) 

    # rooms = relationship('Room', back_populates='owner')
    # messages = relationship('Message', back_populates='author')

    def __repr__(self) -> str:
        return f"<User {self.id} - {self.username} - {self.email} - {self.created_at} - {self.modified_at}>"