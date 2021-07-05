from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from apis.business_api import crud, models, schemas
from apis.business_api.api import dependencies as deps

router = APIRouter()

@router.get("/", response_model = List[schemas.User])
def read_users(db: Session = Depends(deps.get_db)):
    users = crud.user.get_users(db)
    return users

@router.post("/", response_model = schemas.User)
def create_user(user: schemas.UserCreate,
                db: Session = Depends(deps.get_db)):
    db_user = crud.user.get_user(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    return crud.user.create_user(db = db, user = user)
