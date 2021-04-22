# pylint: disable=no-name-in-module
# pylint: disable=no-self-argument
from typing import List, Optional
from datetime import date

from pydantic import BaseModel
from sqlalchemy.sql.expression import true


class NoteBase(BaseModel):
    name: str
    type: str
    content: str
    permission: str
    createdate: date
    updatedate: date


class NoteCreate(NoteBase):
    owner_id: Optional[str]


class Note(NoteBase):
    id: int
    user: Optional[int]
    owner_id: str = None
    parent_id: int = None

    class Config:
        orm_mode = True


class ParentBase(BaseModel):
    name: str
    content: str
    permission: str
    createdate: date
    updatedate: date

    class Config:
        orm_mode = True


class ParentCreate(ParentBase):
    owner_id: Optional[str]


class Parent(ParentBase):
    id: int
    childs: List[Note] = None


class UserBase(BaseModel):
    username: Optional[str]
    email: Optional[str]
    full_name: Optional[str]
    permissions: str = "[]"

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: Optional[str]
    image: str = None
    notes: List[Note] = None
    parents: List[Parent] = None
    friends: List[UserBase] = None


class ChangeUser(BaseModel):
    username: Optional[str]
    email: Optional[str]
    full_name: Optional[str]
    image: Optional[str]
    permissions: Optional[str] = "[]"


class ChangeParent(BaseModel):
    name: Optional[str]
    content: Optional[str]


class ChangeNote(BaseModel):
    name: Optional[str]
    content: Optional[str]
    permission: Optional[str]
    updatedate: Optional[date]
