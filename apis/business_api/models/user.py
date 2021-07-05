from apis.business_api.database import Base

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

class User(Base):
    __tablename__ = "users"

    username = Column(String, primary_key=True, index=True)
    hash_password = Column(String)
    disabled = Column(Boolean)
