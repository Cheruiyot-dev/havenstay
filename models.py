from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base  # Assuming you have a `Base` in a database.py file
from enum import Enum as PyEnum


class BookingStatus(PyEnum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    # user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  
    # room_id = Column(Integer, ForeignKey("rooms.id"), nullable=True)   
    # table_id = Column(Integer, ForeignKey("tables.id"), nullable=True)  
    # event_id = Column(Integer, ForeignKey("events.id"), nullable=True)  
    booking_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    check_in_date = Column(DateTime, nullable=False)
    check_out_date = Column(DateTime, nullable=True) 
    total_amount = Column(Float, nullable=False)
    status = Column(Enum(BookingStatus), default=BookingStatus.PENDING)
    special_requests = Column(String, nullable=True)

    # Relationships
    # user = relationship("User", back_populates="bookings")
    # room = relationship("Room", back_populates="bookings")
    # table = relationship("Table", back_populates="bookings")
    # event = relationship("Event", back_populates="bookings")

    def __repr__(self):
        return f"<Booking id={self.id} status={self.status}>"
