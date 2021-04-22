
from fastapi.applications import FastAPI
from fastapi.param_functions import Depends
from fastapi.responses import PlainTextResponse
from fastapi import status
from starlette.responses import Response
from db import get_db, crud
import auth


db = get_db()


def addDeleteRequests(app: FastAPI):
    @app.delete('/parent/{id}')
    async def delete_parent(id):
        crud.delete_parent(db, id)
        return PlainTextResponse("OK", status_code=status.HTTP_200_OK)

    @app.delete('/notes/{id}')
    async def delete_note(id, user=Depends(auth.get_current_user)):
        note = crud.get_note(db, id)
        if (note == None or note.owner_id != user.id):
            return Response("Not authenticated", status_code=status.HTTP_401_UNAUTHORIZED)
        crud.delete_note(db, id)
        return PlainTextResponse("OK", status_code=status.HTTP_200_OK)
