""" settings.py
"""

from dotenv import load_dotenv
from pathlib import Path
import os
 
load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

OLTP_HOST = os.getenv("OLTP_HOST")
OLTP_USERNAME = os.getenv("OLTP_USERNAME")
OLTP_PASSWORD = os.getenv("OLTP_PASSWORD")
OLTP_PORT = os.getenv("OLTP_PORT")

OLTP_TEST_HOST = os.getenv("OLTP_TEST_HOST")
OLTP_TEST_USERNAME = os.getenv("OLTP_TEST_USERNAME")
OLTP_TEST_PASSWORD = os.getenv("OLTP_TEST_PASSWORD")
OLTP_TEST_PORT = os.getenv("OLTP_TEST_PORT")

STAGE = os.getenv("STAGE")
