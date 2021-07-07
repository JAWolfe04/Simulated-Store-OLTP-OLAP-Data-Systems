from datetime import timedelta

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from apis.business_api import security, settings, schemas, crud

from apis.business_api.api import dependencies as deps

router = APIRouter()

@router.post("/access-token", response_model = schemas.Token)
async def login_for_access_token(db: Session = Depends(deps.get_db),
        form_data: OAuth2PasswordRequestForm = Depends()):
    user = crud.user.authenticate(db, username = form_data.username,
                                  password = form_data.password)
    if not user:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Incorrect username or password")
    elif user.disabled:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user")
    access_token_expires = timedelta(
        minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data = {"sub": user.username}, expires_delta = access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
