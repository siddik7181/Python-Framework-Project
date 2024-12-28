from .base import Base

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

class Room(Base):
    __tablename__ = 'rooms'
    
    name: Mapped[str] = mapped_column(String, unique=True)
    # owner_id = Column(Integer, ForeignKey('users.id'))
    
    # owner = relationship('User', back_populates='rooms')
    # messages = relationship('Message', back_populates='room')

    def __repr__(self):
        return f"<Room(id={self.id}, name={self.name}) - {self.created_at} - {self.modified_at}>"
