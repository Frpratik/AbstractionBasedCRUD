from user import UserManager
from team import TeamManager
from project_board import ProjectBoardManager
import json
import datetime

def now():
    return datetime.datetime.now().isoformat()

# --- USER ---
um = UserManager()
user_req = json.dumps({"name": "akshat", "display_name": "Akshat", "creation_time": now()})
print(um.create_user(user_req))  # Should return {"id": "user_1"}
print(um.list_users())

# --- TEAM ---
tm = TeamManager()
user_id = json.loads(um.create_user(json.dumps({"name": "neha", "display_name": "Neha", "creation_time": now()})))["id"]
team_req = json.dumps({"name": "teamx", "description": "test team", "admin": user_id, "creation_time": now()})
print(tm.create_team(team_req))   # Should return {"id": "team_1"}
print(tm.list_teams())

# --- ADD USER TO TEAM ---
print(tm.add_users_to_team(json.dumps({"id": "team_1", "users": [user_id]})))
print(tm.list_team_users(json.dumps({"id": "team_1"})))

# --- BOARD & TASK ---
bm = ProjectBoardManager()
board_req = json.dumps({"name": "Sprint 1", "description": "First Sprint", "team_id": "team_1", "creation_time": now()})
print(bm.create_board(board_req))
print(bm.list_boards(json.dumps({"id": "team_1"})))

# Create a new task assigned to this user
task_req = json.dumps({
    "title": "Do onboarding",
    "description": "Complete onboarding task",
    "user_id": user_id,
    "board_id": "board_1",
    "creation_time": now()
})
print(bm.add_task(task_req))
# Update task status
print(bm.update_task_status(json.dumps({"id": "task_1", "status": "COMPLETE"})))

# List boards and export one
print(bm.export_board(json.dumps({"id": "board_1"})))
