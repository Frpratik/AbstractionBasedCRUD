import json
import os
from project_board_base import ProjectBoardBase
from exceptions import *
from utils import load_json, save_json, generate_id, OUT_DIR, handle_api_exceptions

BOARDS_FILE = "boards.json"
TASKS_FILE = "tasks.json"

class ProjectBoardManager(ProjectBoardBase):
    
    @handle_api_exceptions
    def create_board(self, request: str):
        req = json.loads(request)
        name = req.get("name", "").strip()
        desc = req.get("description", "").strip()
        team_id = req.get("team_id", "")
        creation_time = req.get("creation_time")
        if len(name) > 64:
            raise ValidationError("Board name ≤64 chars")
        if len(desc) > 128:
            raise ValidationError("Description ≤128 chars")
        boards = load_json(BOARDS_FILE, {"boards": []})["boards"]
        for b in boards:
            if b["team_id"] == team_id and b["name"].lower() == name.lower():
                raise BoardAlreadyExistsError()
        board_id = generate_id("board", boards)
        board = {
            "id": board_id,
            "name": name,
            "description": desc,
            "team_id": team_id,
            "creation_time": creation_time,
            "status": "OPEN",
            "end_time": None
        }
        boards.append(board)
        save_json(BOARDS_FILE, {"boards": boards})
        return json.dumps({"id": board_id})

    @handle_api_exceptions
    def close_board(self, request: str) -> str:
        req = json.loads(request)
        board_id = req["id"]
        boards = load_json(BOARDS_FILE, {"boards": []})["boards"]
        tasks = load_json(TASKS_FILE, {"tasks": []})["tasks"]
        idx = next((i for i, b in enumerate(boards) if b["id"] == board_id), None)
        if idx is None:
            raise BoardNotFoundError()
        board_tasks = [t for t in tasks if t["board_id"] == board_id]
        if any(t["status"] != "COMPLETE" for t in board_tasks):
            raise OperationNotAllowedError("All tasks must be COMPLETE to close the board")
        boards[idx]["status"] = "CLOSED"
        boards[idx]["end_time"] = req.get("end_time")
        save_json(BOARDS_FILE, {"boards": boards})
        return json.dumps({"id": board_id})

    @handle_api_exceptions
    def add_task(self, request: str) -> str:
        req = json.loads(request)
        title = req.get("title", "").strip()
        desc = req.get("description", "").strip()
        user_id = req.get("user_id", "")
        board_id = req.get("board_id")
        creation_time = req.get("creation_time")
        if len(title) > 64:
            raise ValidationError("Task title ≤64 chars")
        if len(desc) > 128:
            raise ValidationError("Description ≤128 chars")
        boards = load_json(BOARDS_FILE, {"boards": []})["boards"]
        board = next((b for b in boards if b["id"] == board_id), None)
        if not board:
            raise BoardNotFoundError()
        if board["status"] != "OPEN":
            raise OperationNotAllowedError("Can only add task to OPEN board")
        tasks = load_json(TASKS_FILE, {"tasks": []})["tasks"]
        if any(t["board_id"] == board_id and t["title"].lower() == title.lower() for t in tasks):
            raise TaskAlreadyExistsError()
        task_id = generate_id("task", tasks)
        task = {
            "id": task_id,
            "board_id": board_id,
            "title": title,
            "description": desc,
            "user_id": user_id,
            "status": "OPEN",
            "creation_time": creation_time
        }
        tasks.append(task)
        save_json(TASKS_FILE, {"tasks": tasks})
        return json.dumps({"id": task_id})

    @handle_api_exceptions
    def update_task_status(self, request: str):
        req = json.loads(request)
        task_id = req["id"]
        status = req["status"]
        tasks = load_json(TASKS_FILE, {"tasks": []})["tasks"]
        idx = next((i for i, t in enumerate(tasks) if t["id"] == task_id), None)
        if idx is None:
            raise TaskNotFoundError()
        if status not in ("OPEN", "IN_PROGRESS", "COMPLETE"):
            raise ValidationError("Invalid task status")
        tasks[idx]["status"] = status
        save_json(TASKS_FILE, {"tasks": tasks})
        return json.dumps({"id": task_id})

    @handle_api_exceptions
    def list_boards(self, request: str) -> str:
        team_id = json.loads(request)["id"]
        boards = load_json(BOARDS_FILE, {"boards": []})["boards"]
        open_boards = [
            {"id": b["id"], "name": b["name"]}
            for b in boards if b["team_id"] == team_id and b["status"] == "OPEN"
        ]
        return json.dumps(open_boards)

    @handle_api_exceptions
    def export_board(self, request: str) -> str:
        board_id = json.loads(request)["id"]
        boards = load_json(BOARDS_FILE, {"boards": []})["boards"]
        board = next((b for b in boards if b["id"] == board_id), None)
        if not board:
            raise BoardNotFoundError()
        tasks = load_json(TASKS_FILE, {"tasks": []})["tasks"]
        board_tasks = [t for t in tasks if t["board_id"] == board_id]
        lines = []
        lines.append(f"BOARD: {board['name']} (Status: {board['status']})\n")
        lines.append(f"Description: {board['description']}\n")
        lines.append(f"Created: {board.get('creation_time', '')}")
        if board['status'] == 'CLOSED':
            lines.append(f"Closed at: {board.get('end_time', '')}")
        lines.append("\nTasks:")
        t_status = {"OPEN": "🟢", "IN_PROGRESS": "🟡", "COMPLETE": "✅"}
        for t in board_tasks:
            lines.append(f"  [{t_status.get(t['status'], '?')}] {t['title']}: {t['description']} (Assigned: {t['user_id']}, Created: {t.get('creation_time','')})")
        out_name = f"board_{board_id}.txt"
        out_path = os.path.join(OUT_DIR, out_name)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        return json.dumps({"out_file": out_name})
