from flask import request, redirect, url_for, session
from functools import wraps

def login_limit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get("usertel"):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login'))

    return wrapper