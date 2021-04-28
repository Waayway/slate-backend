from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship
import uuid

from sqlalchemy.sql.expression import true
from .database import Base


def uuid_gen():
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True, default=uuid_gen)
    username = Column(String, index=True, unique=True)
    email = Column(String, index=True)
    password = Column(String)
    permissions = Column(String)  # AS JSON ARRAY
    image = Column(String)  # BASE64 IMAGE
    friend_ids = Column(Integer, ForeignKey("users.id"))

    notes = relationship("Note", back_populates="owner")
    parents = relationship("ParentNote", back_populates="owner")
    friends = relationship("User")


class ParentNote(Base):
    __tablename__ = "parents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    content = Column(String)
    permission = Column(String)
    createdate = Column(Date)
    updatedate = Column(Date)
    owner_id = Column(String, ForeignKey("users.id"))
    # child_ids = Column(Integer, ForeignKey("notes.id"))

    childs = relationship("Note")
    owner = relationship("User", back_populates="parents")


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    type = Column(String)
    content = Column(String)
    permission = Column(String)
    createdate = Column(Date)
    updatedate = Column(Date)
    owner_id = Column(String, ForeignKey("users.id"))
    parent_id = Column(Integer, ForeignKey("parents.id"))

    owner = relationship("User", back_populates="notes")
    # parent = relationship("ParentNote", back_populates="childs")
