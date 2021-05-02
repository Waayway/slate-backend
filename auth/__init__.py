from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.hash import bcrypt
from sqlalchemy.orm.session import Session
from db import crud, schemas, get_db
import jwt
import json
import os

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

JWT_SECRET = os.getenv("JWT_SECRET")
SECRET_KEY = os.getenv("SECRET_KEY")

db = get_db()


def verify_password(password, password_hash):
    password = str(password) + SECRET_KEY
    return bcrypt.verify(password, password_hash)


def authenticate_user(username: str, password: str, db: Session):
    user = crud.get_user_by_name_with_password(db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return crud.get_user_by_name(db, user.username)


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        user = crud.get_user(db, payload.get('id'))
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid username or password")

    return user


def createUrls(app: FastAPI):
    #Get logged in user
    @app.get('/users/me', response_model=schemas.User)
    async def get_myself(user: str = Depends(get_current_user)):
        return user

    # Custom OAuth
    @app.post('/login')
    async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
        user = authenticate_user(form_data.username, form_data.password, db)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Invalid username or password")

        userJSON = json.loads(user.json())
        del userJSON["image"]
        token = jwt.encode(userJSON, JWT_SECRET)

        return {'access_token': token, 'token_type': 'bearer'}