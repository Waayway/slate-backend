from os import stat
from sqlalchemy.sql.sqltypes import JSON
from starlette.responses import Response
from starlette.status import HTTP_401_UNAUTHORIZED
import auth
from fastapi.applications import FastAPI
from fastapi import status, FastAPI
from fastapi.param_functions import Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm.session import Session
from db import crud, get_db, models, schemas
import json

db = get_db()


def addGetRequests(app: FastAPI):
    # @app.get("/users/id/{id}")
    # def get_user_by_id(id: str):
    #     user = crud.get_user(db, id)
    #     if user:
    #         # return JSONResponse({"data": user, "message": "OK"}, status_code=status.HTTP_302_FOUND)
    #         return {"data": user, "message": "OK"}
    #     else:
    #         return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
    #                             content="None")

    # @app.get("/users/name/{name}")
    # def get_user_by_name(name: str):
    #     user = crud.get_user_by_name(db, name)
    #     if user:
    #         return f"{{'data': {user}}}"
    #         # return JSONResponse({"data": user.__str__(), "message": "OK"}, status_code=status.HTTP_302_FOUND)
    #     else:
    #         return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
    #                             content="None")

    @app.get("/parent/id/{id}")
    def get_parent_by_id(id: int, user=Depends(auth.get_current_user)):
        parent = crud.get_parent(db, id)
        if parent:
            user_sql = db.query(
                models.User).filter(models.User.id == user.id).first()
            print()
            if (parent.owner_id != user.id
                    and parent.permission not in user_sql.permissions):
                return Response("Not authenticated",
                                status_code=status.HTTP_401_UNAUTHORIZED)
            return JSONResponse(
                {
                    "data": json.loads(parent.json()),
                    "message": "OK",
                    "edit": parent.owner_id == user.id
                },
                status_code=status.HTTP_302_FOUND)
        else:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                                content="None")

    @app.get("/parent/name/{name}")
    def get_parent_by_str(name: str, user=Depends(auth.get_current_user)):
        parent = crud.get_parent_by_name(db, name)
        if parent:
            if (parent.owner_id != user.id):
                return Response("Not authenticated",
                                status_code=status.HTTP_401_UNAUTHORIZED)
            return JSONResponse(
                {
                    "data": json.loads(parent.json()),
                    "message": "OK"
                },
                status_code=status.HTTP_302_FOUND)
        else:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                                content="None")

    @app.get('/parent/permission', response_model=schemas.ReturnLinkedParents)
    def get_parent_based_on_permission(user=Depends(auth.get_current_user)):
        user_sql = db.query(
            models.User).filter(models.User.id == user.id).first()
        parents = []
        permissions = json.loads(user_sql.permissions)
        for i in permissions:
            parents.append(
                schemas.Parent.from_orm(
                    db.query(models.ParentNote).filter(
                        models.ParentNote.permission == i).first()))
        if parents == []:
            return JSONResponse({"message": "Nothing found"},
                                status_code=status.HTTP_404_NOT_FOUND)
        return {"data": parents}

    @app.get("/notes/id/{id}")
    def get_note_by_id(id: int, user=Depends(auth.get_current_user)):
        note = crud.get_note(db, id)
        if note:
            user_sql = db.query(
                models.User).filter(models.User.id == user.id).first()
            parent = crud.get_parent(db, note.parent_id)
            if (note.owner_id != user.id
                    and parent.permission not in user_sql.permissions):
                return Response("Not authenticated",
                                status_code=status.HTTP_401_UNAUTHORIZED)
            return JSONResponse(
                {
                    "data": json.loads(note.json()),
                    "message": "OK",
                    "edit": note.owner_id == user.id
                },
                status_code=status.HTTP_302_FOUND)
        else:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                                content="None")

    @app.get("/notes/name/{name}")
    def get_note_by_name(name: str, user=Depends(auth.get_current_user)):
        note = crud.get_note_by_name(db, name)
        if note:
            if (note.owner_id != user.id):
                return Response("Not authenticated",
                                status_code=status.HTTP_401_UNAUTHORIZED)
            return JSONResponse(
                {
                    "data": json.loads(note.json()),
                    "message": "OK"
                },
                status_code=status.HTTP_302_FOUND)
        else:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                                content="None")

    @app.get("/notes/parent/{id}")
    def get_parent_from_note(id: int, user=Depends(auth.get_current_user)):
        note = crud.get_note(db, id)
        if not note or note.owner_id != user.id:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                                content="None")
        else:
            if note.parent_id:
                parent = crud.get_parent(note.parent_id)
                if parent:
                    return JSONResponse(
                        {
                            "data": json.loads(parent.json()),
                            "message": "OK"
                        },
                        status_code=status.HTTP_302_FOUND)
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                                content="None")
