import json
from team_base import TeamBase
from exceptions import *
from utils import load_json, save_json, generate_id, handle_api_exceptions

TEAMS_FILE = "teams.json"
USERS_FILE = "users.json"

class TeamManager(TeamBase):
        
    @handle_api_exceptions
    def create_team(self, request: str) -> str:
        req = json.loads(request)
        name = req.get("name", "").strip()
        description = req.get("description", "").strip()
        admin = req.get("admin", "")
        if not name or len(name) > 64:
            raise ValidationError("Name must be ≤64 chars and unique")
        if len(description) > 128:
            raise ValidationError("Description ≤128 chars")
        teams = load_json(TEAMS_FILE, {"teams": []})["teams"]
        if any(t["name"].lower() == name.lower() for t in teams):
            raise TeamAlreadyExistsError()
        team_id = generate_id("team", teams)
        team = {
            "id": team_id,
            "name": name,
            "description": description,
            "creation_time": req.get("creation_time"),
            "admin": admin,
            "users": [admin],
        }
        teams.append(team)
        save_json(TEAMS_FILE, {"teams": teams})
        return json.dumps({"id": team_id})

    @handle_api_exceptions
    def list_teams(self) -> str:
        teams = load_json(TEAMS_FILE, {"teams": []})["teams"]
        return json.dumps([
            {
                "name": t["name"],
                "description": t.get("description", ""),
                "creation_time": t.get("creation_time", ""),
                "admin": t["admin"]
            } for t in teams
        ])

    @handle_api_exceptions
    def describe_team(self, request: str) -> str:
        team_id = json.loads(request)["id"]
        teams = load_json(TEAMS_FILE, {"teams": []})["teams"]
        team = next((t for t in teams if t["id"] == team_id), None)
        if not team:
            raise TeamNotFoundError()
        return json.dumps({
            "name": team["name"],
            "description": team["description"],
            "creation_time": team.get("creation_time", ""),
            "admin": team["admin"]
        })

    @handle_api_exceptions
    def update_team(self, request: str) -> str:
        req = json.loads(request)
        team_id = req["id"]
        teams = load_json(TEAMS_FILE, {"teams": []})["teams"]
        idx = next((i for i, t in enumerate(teams) if t["id"] == team_id), None)
        if idx is None:
            raise TeamNotFoundError()
        t = teams[idx]
        update = req["team"]
        name = update.get("name", t["name"]).strip()
        description = update.get("description", t["description"]).strip()
        admin = update.get("admin", t["admin"])
        if name != t["name"] and any(tm["name"].lower() == name.lower() for tm in teams):
            raise TeamAlreadyExistsError()
        if len(name) > 64 or len(description) > 128:
            raise ValidationError("Max char exceeded")
        t.update({"name": name, "description": description, "admin": admin})
        teams[idx] = t
        save_json(TEAMS_FILE, {"teams": teams})
        return json.dumps({"id": team_id})

    @handle_api_exceptions
    def add_users_to_team(self, request: str):
        req = json.loads(request)
        team_id = req["id"]
        user_ids = req.get("users", [])
        teams = load_json(TEAMS_FILE, {"teams": []})["teams"]
        idx = next((i for i, t in enumerate(teams) if t["id"] == team_id), None)
        if idx is None:
            raise TeamNotFoundError()
        users_list = teams[idx].get("users", [])
        if len(users_list) + len(user_ids) > 50:
            raise ValidationError("Max users in a team: 50")
        for uid in user_ids:
            if uid not in users_list:
                users_list.append(uid)
        teams[idx]["users"] = users_list
        save_json(TEAMS_FILE, {"teams": teams})
        return json.dumps({"id": team_id})

    @handle_api_exceptions
    def remove_users_from_team(self, request: str):
        req = json.loads(request)
        team_id = req["id"]
        user_ids = set(req.get("users", []))
        teams = load_json(TEAMS_FILE, {"teams": []})["teams"]
        idx = next((i for i, t in enumerate(teams) if t["id"] == team_id), None)
        if idx is None:
            raise TeamNotFoundError()
        users_list = teams[idx].get("users", [])
        teams[idx]["users"] = [u for u in users_list if u not in user_ids]
        save_json(TEAMS_FILE, {"teams": teams})
        return json.dumps({"id": team_id})

    @handle_api_exceptions
    def list_team_users(self, request: str):
        req = json.loads(request)
        team_id = req["id"]
        teams = load_json(TEAMS_FILE, {"teams": []})["teams"]
        team = next((t for t in teams if t["id"] == team_id), None)
        if not team:
            raise TeamNotFoundError()
        users_ids = team.get("users", [])
        all_users = load_json(USERS_FILE, {"users": []})["users"]
        res = []
        for uid in users_ids:
            user = next((u for u in all_users if u["id"] == uid), None)
            if user:
                res.append({
                    "id": user["id"],
                    "name": user["name"],
                    "display_name": user.get("display_name", "")
                })
        return json.dumps(res)
