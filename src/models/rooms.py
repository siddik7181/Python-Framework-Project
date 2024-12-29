from .base import Base

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List

class Room(Base):
    __tablename__ = 'rooms'
    
    name: Mapped[str] = mapped_column(String, unique=True)
    owner_id: Mapped[str] = mapped_column(String, ForeignKey('users.id'))
    
    owner: Mapped["User"] = relationship(back_populates='rooms')
    messages: Mapped[List["Message"]]  = relationship(back_populates='room', cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Room(id={self.id}, name={self.name}) - {self.created_at} - {self.modified_at}>"
