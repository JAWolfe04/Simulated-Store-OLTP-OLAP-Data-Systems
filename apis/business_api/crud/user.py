from apis.business_api import models, schemas

from sqlalchemy.orm import Session

class Crud_User:

    def get_user(self, db: Session, username: str):
        return db.query(models.User).filter(models.User.username == username).first()

    def get_users(self, db: Session):
        return db.query(models.User).all()

    def create_user(self, db: Session, user: schemas.UserCreate):
        db_user = models.User(username = user.username,
                              hash_password = user.password,
                              disabled = False)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

user = Crud_User()
