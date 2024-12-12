import sqlite3
from database import verify_user_session

class UserSession:
    _instance = None
    _current_user = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UserSession, cls).__new__(cls)
        return cls._instance

    @classmethod
    def set_user(cls, username):
        if verify_user_session(username):
            cls._current_user = username
            return True
        return False

    @classmethod
    def get_user(cls):
        if cls._current_user and verify_user_session(cls._current_user):
            return cls._current_user
        return None

    @classmethod
    def clear(cls):
        cls._current_user = None

    @classmethod
    def is_valid(cls):
        return cls._current_user is not None and verify_user_session(cls._current_user) 