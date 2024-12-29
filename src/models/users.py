
from .base import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean
from typing import List

class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    password_hash: Mapped[str] = mapped_column(String(100), nullable=False) 

    rooms: Mapped[List['Room']] = relationship(back_populates='owner', cascade="all, delete-orphan")
    messages: Mapped[List["Message"]] = relationship(back_populates='author', cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<User {self.id} - {self.username} - {self.email} - {self.created_at} - {self.modified_at}>"