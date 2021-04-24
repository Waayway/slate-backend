from datetime import date
from fastapi.openapi.models import OperationWithCallbacks
from pydantic.schema import schema
from starlette.status import HTTP_202_ACCEPTED, HTTP_401_UNAUTHORIZED
import auth
from fastapi.applications import FastAPI
from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session
from fastapi.responses import JSONResponse, Response
from fastapi import status
from sqlalchemy.orm.session import Session
from db import crud, models, schemas, get_db

db = get_db()


def addPostRequests(app: FastAPI):
    @app.post('/users', response_model=schemas.User)
    async def create_user(user: schemas.UserCreate):
        user_obj = crud.create_user(db, user)
        return user_obj

    @app.post('/users/change', response_model=schemas.User)
    async def change_myself(ChangeUser: schemas.ChangeUser,
                            user=Depends(auth.get_current_user)):
        user_sql = db.query(
            models.User).filter(models.User.id == user.id).first()
        if ChangeUser.username:
            user_sql.username = ChangeUser.username
        if ChangeUser.email:
            user_sql.email = ChangeUser.email
        if ChangeUser.image:
            user_sql.image = ChangeUser.image
        if ChangeUser.permissions:
            user_sql.permissions = ChangeUser.permissions
        if ChangeUser.full_name:
            user_sql.permissions = ChangeUser.full_name
        db.commit()
        db.refresh(user_sql)
        return schemas.User.from_orm(user_sql)

    @app.post('/parents', response_model=schemas.Parent)
    async def create_parent(parent: schemas.ParentCreate,
                            user=Depends(auth.get_current_user)):
        print(parent)
        parent.owner_id = user.id
        parent_obj = crud.create_parent(db, parent)
        return parent_obj

    @app.post('/parent/change/{id}', response_model=schemas.Parent)
    async def change_parent(id,
                            ChangeParent: schemas.ChangeParent,
                            user=Depends(auth.get_current_user)):
        # parent_sql = crud.get_parent(db, id)
        parent_sql = db.query(
            models.ParentNote).filter(models.ParentNote.id == id).first()
        if parent_sql.owner_id != user.id:
            return Response("Not authenticated",
                            status_code=status.HTTP_401_UNAUTHORIZED)
        if ChangeParent.name:
            parent_sql.name = ChangeParent.name
        if ChangeParent.content:
            parent_sql.content = ChangeParent.content
        if ChangeParent.permission:
            parent_sql.permission = ChangeParent.permission
        if ChangeParent.updatedate:
            parent_sql.updatedate = ChangeParent.updatedate
        db.commit()
        db.refresh(parent_sql)
        return schemas.Parent.from_orm(parent_sql)

    @app.post('/notes', response_model=schemas.Note)
    async def create_note(note: schemas.NoteCreate,
                          user=Depends(auth.get_current_user)):
        note.owner_id = user.id
        note_obj = crud.create_note(db, note)
        return note_obj

    @app.post('/notes/change/{id}', response_model=schemas.Note)
    async def change_note(id,
                          note: schemas.ChangeNote,
                          user=Depends(auth.get_current_user)):
        note_sql = db.query(models.Note).filter(models.Note.id == id).first()
        if note_sql.owner_id != user.id:
            return Response("Not authenticated",
                            status_code=status.HTTP_401_UNAUTHORIZED)
        if note.name:
            note_sql.name = note.name
        if note.content:
            note_sql.content = note.content
        if note.permission:
            note_sql.permission = note.permission
        if note.updatedate:
            note_sql.updatedate = note.updatedate
        db.commit()
        db.refresh(note_sql)
        return schemas.Note.from_orm(note_sql)

    @app.post('/notes/link')
    @app.post('/parents/link')
    def link_parent_and_note(link: schemas.LinkParentToNote,
                             user=Depends(auth.get_current_user)):
        note_sql = db.query(models.Note).filter(models.Note.id == link.noteid +
                                                1).first()
        parent_sql = db.query(models.ParentNote).filter(
            models.ParentNote.id == link.parentid).first()
        print(note_sql, parent_sql)
        if (note_sql.owner_id != user.id or parent_sql.owner_id != user.id):
            return Response("Not authenticated",
                            status_code=status.HTTP_401_UNAUTHORIZED)
        if (note_sql.parent_id == parent_sql.id):
            note_sql.parent_id = None
        else:
            note_sql.parent_id = parent_sql.id
        db.commit()
        return Response("OK", status_code=status.HTTP_202_ACCEPTED)
