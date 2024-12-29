from .base import Base

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

class Message(Base):
    __tablename__ = 'messages'
    
    message: Mapped[str] = mapped_column(String)

    room_id: Mapped[str] = mapped_column(String, ForeignKey('rooms.id'))
    author_id: Mapped[str] = mapped_column(String, ForeignKey('users.id'))
    
    room: Mapped["Room"] = relationship(back_populates='messages')
    author: Mapped["User"] = relationship(back_populates='messages')

    def __repr__(self):
        return f"<Message(id={self.id}, author_id={self.author_id}, content={self.message})>"
