import pydantic, os
from pydantic.error_wrappers import ValidationError
from pydantic.schema import schema
from sqlalchemy.orm import Session
from passlib.hash import bcrypt

from . import models, schemas

SECRET_KEY = os.getenv("SECRET_KEY")


def get_user(db: Session, user_id: str):
    return schemas.User.from_orm(
        db.query(models.User).filter(models.User.id == user_id).first())


def get_user_by_name(db: Session, name: str):
    return schemas.User.from_orm(
        db.query(models.User).filter(models.User.username == name).first())


def get_user_by_name_with_password(db: Session, name: str):
    user = db.query(models.User).filter(models.User.username == name).first()
    if user is None:
        return user
    return schemas.UserCreate.from_orm(user)


def get_user_by_email(db: Session, email: str):
    return schemas.User.from_orm(
        db.query(models.User).filter(models.User.email == email).first())


def get_user_by_token(db: Session, token: str):
    return schemas.User.from_orm(
        db.query(models.User).filter(models.User.token == token).first())


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    password = bcrypt.hash(str(user.password) + SECRET_KEY)
    db_user = models.User(username=user.username,
                          email=user.email,
                          permissions=user.permissions,
                          password=password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db_user = schemas.User.from_orm(db_user)
    return db_user


def get_parent(db: Session, parent_id: int):
    return schemas.Parent.from_orm(
        db.query(models.ParentNote).filter(
            models.ParentNote.id == parent_id).first())


def get_parent_by_name(db: Session, name: str):
    return schemas.Parent.from_orm(
        db.query(
            models.ParentNote).filter(models.ParentNote.name == name).first())


def get_parents(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ParentNote).offset(skip).limit(limit).all()


def create_parent(db: Session, parent: schemas.ParentCreate):
    db_parent = models.ParentNote(name=parent.name,
                                  content=parent.content,
                                  permission=parent.permission,
                                  createdate=parent.createdate,
                                  updatedate=parent.updatedate,
                                  owner_id=parent.owner_id)
    db.add(db_parent)
    db.commit()
    db.refresh(db_parent)
    db_parent = schemas.Parent.from_orm(db_parent)
    return db_parent


def delete_parent(db: Session, parent_id: int):
    db_parent = db.query(
        models.ParentNote).filter(models.ParentNote.id == parent_id).first()
    db.delete(db_parent)
    db.commit()


def get_note(db: Session, note_id: int):
    try:
        return schemas.Note.from_orm(
            db.query(models.Note).filter(models.Note.id == note_id).first())
    except ValidationError:
        return None


def get_note_by_name(db: Session, name: str):
    return schemas.Note.from_orm(
        db.query(models.Note).filter(models.Note.name == name).first())


def get_notes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Note).all()


def create_note(db: Session, note: schemas.NoteCreate):
    db_note = models.Note(name=note.name,
                          type=note.type,
                          content=note.content,
                          permission=note.permission,
                          createdate=note.createdate,
                          updatedate=note.createdate,
                          owner_id=note.owner_id)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    db_note = schemas.Note.from_orm(db_note)
    return db_note


def delete_note(db: Session, note_id: int):
    db_note = db.query(models.Note).filter(models.Note.id == note_id).first()
    db.delete(db_note)
    db.commit()
