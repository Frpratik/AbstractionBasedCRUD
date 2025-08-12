import os
import json
import threading
from exceptions import *

DB_DIR = os.path.join(os.path.dirname(__file__), 'db')
OUT_DIR = os.path.join(os.path.dirname(__file__), 'out')
os.makedirs(DB_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)
FILE_LOCK = threading.Lock()

def db_file(filename):
    return os.path.join(DB_DIR, filename)

def load_json(filename, default):
    try:
        with open(db_file(filename), 'r') as f:
            return json.load(f)
    except Exception:
        return default.copy()

def save_json(filename, data):
    with FILE_LOCK:
        with open(db_file(filename), 'w') as f:
            json.dump(data, f, indent=2)

def generate_id(prefix, data_list):
    max_id = 0
    for entry in data_list:
        if entry.get('id', '').startswith(prefix):
            try:
                n = int(entry['id'].split('_')[1])
                if n > max_id: max_id = n
            except Exception: pass
    return f"{prefix}_{max_id + 1}"

def handle_api_exceptions(func):

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (UserAlreadyExistsError, UserNotFoundError,
                TeamAlreadyExistsError, TeamNotFoundError,
                BoardAlreadyExistsError, BoardNotFoundError,
                TaskAlreadyExistsError, TaskNotFoundError,
                ValidationError, OperationNotAllowedError) as e:
            return json.dumps({
                "error": type(e).__name__,
                "message": str(e) if str(e) else "An error occurred"
            })
        except Exception as e:
            return json.dumps({
                "error": "InternalError",
                "message": "Internal server error"
            })
    return wrapper
