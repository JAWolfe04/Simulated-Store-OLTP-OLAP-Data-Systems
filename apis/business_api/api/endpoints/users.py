from typing import List

from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session

from apis.business_api import crud, models, schemas
from apis.business_api.api import dependencies as deps

router = APIRouter()

@router.post("/", response_model = schemas.User)
def create_user(db: Session = Depends(deps.get_db),
                username: str = Form(...),
                password: str = Form(...)):
    db_user = crud.user.get_user(db, username = username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    user = schemas.UserCreate(username = username, password = password)
    return crud.user.create_user(db = db, user = user)

@router.delete("/")
def delete_user(db: Session = Depends(deps.get_db),
                username: str = Form(...),
                password: str = Form(...)):
    user = crud.user.authenticate(db, username = username, password = password)
    if not user:
        raise HTTPException(status_code = 400,
                            detail = "Invalid username or password")
    crud.user.delete_user(db = db, user = user)
