#!/usr/bin/env python3
"""User authentication"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Sequence, INTEGER

Base = declarative_base()


class User(Base):
    """User table model"""

    __tablename__: str = 'users'

    id = Column(Integer,
                primary_key=True
                )
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
