""" settings.py
"""

from dotenv import load_dotenv, find_dotenv
from pathlib import Path
import os
import secrets
 
load_dotenv(find_dotenv())

POSTGRES_DB_CONN = os.getenv("POSTGRES_DB_CONN")

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 3

SECRET_KEY = secrets.token_urlsafe(32)

ALGORITHM = "HS256"
