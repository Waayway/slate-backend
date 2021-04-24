import auth
from fastapi.applications import FastAPI
from fastapi import status, FastAPI
from fastapi.param_functions import Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm.session import Session
from db import crud, get_db
import json

db = get_db()


def addGetRequests(app: FastAPI):
    @app.get("/users/id/{id}")
    def get_user_by_id(id: str):
        user = crud.get_user(db, id)
        if user:
            # return JSONResponse({"data": user, "message": "OK"}, status_code=status.HTTP_302_FOUND)
            return {"data": user, "message": "OK"}
        else:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                                content="None")

    @app.get("/users/name/{name}")
    def get_user_by_name(name: str):
        user = crud.get_user_by_name(db, name)
        if user:
            return f"{{'data': {user}}}"
            # return JSONResponse({"data": user.__str__(), "message": "OK"}, status_code=status.HTTP_302_FOUND)
        else:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                                content="None")

    @app.get("/parent/id/{id}")
    def get_parent_by_id(id: int):
        parent = crud.get_parent(db, id)
        if parent:
            return JSONResponse(
                {
                    "data": json.loads(parent.json()),
                    "message": "OK"
                },
                status_code=status.HTTP_302_FOUND)
        else:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                                content="None")

    @app.get("/parent/name/{name}")
    def get_parent_by_str(name: str):
        parent = crud.get_parent_by_name(db, name)
        if parent:
            return JSONResponse(
                {
                    "data": json.loads(parent.json()),
                    "message": "OK"
                },
                status_code=status.HTTP_302_FOUND)
        else:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                                content="None")

    @app.get("/notes/id/{id}")
    def get_note_by_id(id: int):
        note = crud.get_note(db, id)
        if note:
            return JSONResponse(
                {
                    "data": json.loads(note.json()),
                    "message": "OK"
                },
                status_code=status.HTTP_302_FOUND)
        else:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                                content="None")

    @app.get("/notes/name/{name}")
    def get_note_by_name(name: str):
        note = crud.get_note_by_name(db, name)
        if note:
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
    def get_parent_from_note(id: int):
        note = crud.get_note(db, id)
        if not note:
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
