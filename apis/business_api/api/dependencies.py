from apis.business_api.database import SessionLocal
from apis.business_api import settings
from apis.business_api import crud, models, schemas

from jose import JWTError, jwt

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from pydantic import ValidationError

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl = "/v1/login/access-token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(db: Session = Depends(get_db),
                           token: str = Depends(reusable_oauth2)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY,
                             algorithms = [settings.ALGORITHM])
        token_data = schemas.TokenPayload(**payload)
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Could not validate credentials")
    user = crud.user.get_user(db, username = token_data.username)
    if not user:
        raise HTTPException(status_code = 404, detail = "User not found")
    return user
