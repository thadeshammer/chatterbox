# datastore/db/query.py
"""Centralized location for app queries to seperate the ORM from the core.
"""
from typing import Optional

from sqlmodel import select

from .db import get_db

# TODO queries live here
