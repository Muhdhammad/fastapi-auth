from database.database import Base
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, func, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
# from sqlalchemy.sql import func

# func is a way of calling database side sql functions, not python functions


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    role = Column(String, nullable=False, server_default="user")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    # When a row is inserted, let the database automatically store the current time (UTC), and never allow it to be NULL.

    totp_config = relationship("UserTOTP", back_populates="user", uselist=False) # One to one

class UserTOTP(Base):
    __tablename__ = "users_totp"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    secret_key = Column(String, nullable=True)
    is_enabled = Column(Boolean, default=False, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())

    user = relationship("User", back_populates="totp_config")

