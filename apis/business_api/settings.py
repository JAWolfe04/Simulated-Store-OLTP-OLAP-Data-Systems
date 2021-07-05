""" settings.py
"""

from dotenv import load_dotenv, find_dotenv
from pathlib import Path
import os
 
load_dotenv(find_dotenv())

POSTGRES_DB_CONN = os.getenv("POSTGRES_DB_CONN")
