from apis.business_api import models, schemas
from apis.business_api import security

from sqlalchemy.orm import Session

class Crud_User:

    def get_user(self, db: Session, username: str):
        return db.query(models.User).filter(models.User.username == username).first()

    def create_user(self, db: Session, user: schemas.UserCreate):
        db_user = models.User(
            username = user.username,
            hash_password = security.get_password_hash(user.password),
            disabled = False)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def authenticate(self, db: Session, username: str, password: str):
        user = self.get_user(db, username)
        if not user:
            return False
        if not security.verify_password(password, user.hash_password):
            return False
        return user

    def delete_user(self, db: Session, user: schemas.UserCreate):
        db.delete(user)
        db.commit()

user = Crud_User()
