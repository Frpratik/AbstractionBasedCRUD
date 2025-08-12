import json
from user_base import UserBase
from exceptions import *
from utils import load_json, save_json, generate_id, handle_api_exceptions

USERS_FILE = "users.json"
TEAMS_FILE = "teams.json"

class UserManager(UserBase):
        
    @handle_api_exceptions
    def create_user(self, request: str) -> str:
        req = json.loads(request)
        name = req.get("name", "").strip()
        display_name = req.get("display_name", "").strip()
        if not name or len(name) > 64:
            raise ValidationError("Username must be unique and ≤64 chars")
        if len(display_name) > 64:
            raise ValidationError("Display name ≤64 chars")
        users = load_json(USERS_FILE, {"users": []})["users"]
        if any(u['name'].lower() == name.lower() for u in users):
            raise UserAlreadyExistsError()
        user_id = generate_id("user", users)
        user = {
            "id": user_id,
            "name": name,
            "display_name": display_name,
            "creation_time": req.get("creation_time")
        }
        users.append(user)
        save_json(USERS_FILE, {"users": users})
        return json.dumps({"id": user_id})

    @handle_api_exceptions
    def list_users(self) -> str:
        users = load_json(USERS_FILE, {"users": []})["users"]
        return json.dumps([
            {
                "name": u["name"],
                "display_name": u.get("display_name", ""),
                "creation_time": u.get("creation_time", "")
            } for u in users
        ])

    @handle_api_exceptions
    def describe_user(self, request: str) -> str:
        user_id = json.loads(request)['id']
        users = load_json(USERS_FILE, {"users": []})["users"]
        user = next((u for u in users if u["id"] == user_id), None)
        if not user:
            raise UserNotFoundError()
        return json.dumps({
            "name": user["name"],
            "display_name": user.get("display_name", ""),
            "creation_time": user.get("creation_time", "")
        })

    @handle_api_exceptions
    def update_user(self, request: str) -> str:
        req = json.loads(request)
        user_id = req["id"]
        users = load_json(USERS_FILE, {"users": []})["users"]
        idx = next((i for i, u in enumerate(users) if u["id"] == user_id), None)
        if idx is None:
            raise UserNotFoundError()
        user = users[idx]
        if "name" in req["user"] and req["user"]["name"] != user["name"]:
            raise ValidationError("User name cannot be updated")
        dn = req["user"].get("display_name", "").strip()
        if len(dn) > 128:
            raise ValidationError("Display name ≤128 chars")
        user["display_name"] = dn
        users[idx] = user
        save_json(USERS_FILE, {"users": users})
        return json.dumps({"id": user_id})

    @handle_api_exceptions
    def get_user_teams(self, request: str) -> str:
        user_id = json.loads(request)["id"]
        teams = load_json(TEAMS_FILE, {"teams": []})["teams"]
        filtered = [
            {
                "name": t["name"],
                "description": t.get("description", ""),
                "creation_time": t.get("creation_time", "")
            }
            for t in teams if user_id in t.get("users", [])
        ]
        return json.dumps(filtered)
