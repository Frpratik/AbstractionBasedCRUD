# 🗂️ Team Project Planner Tool

A **Python-based application** for managing **Users, Teams, Project Boards, and Tasks** — all stored **locally** in JSON files with no database server required.  
Built with **abstract base classes** for a clean, modular, and extendable architecture.

---

## 📌 Overview
The **Team Project Planner Tool** provides APIs to:

- 👤 **Manage Users** – Create, update, list, and describe users.  
- 👥 **Manage Teams** – Create teams, add/remove members, and list teams.  
- 📋 **Manage Project Boards** – Create boards for teams and manage them.  
- ✅ **Manage Tasks** – Add, update, and list tasks inside boards.  
- 💾 **Local Persistence** – All data stored in the `db/` folder in **JSON format**.  
- ⚠️ **Exception Handling** – Descriptive errors for invalid inputs **using decorator**.  

---

## 🚀 Features

- User, Team, Board, and Task Management  
- Local JSON file storage (no database needed)  
- Modular and maintainable code structure  
- Custom exception handling  
- Demo script for instant showcase of all features  

---

## 🛠️ Tech Stack

- **Language**: Python 3.x  
- **Persistence**: Local file storage (**JSON format**)  
- **Libraries**:  
  - Built-in Python modules: `json`, `os`, `abc`  
  - Extra dependencies in `requirements.txt`  

---

## 📂 Project Structure

```plaintext
FACTWISE-PYTHON/
│
├── db/                       # Local storage (auto-created, excluded from repo)
├── out/                      # Optional output folder
├── __pycache__/              # Python cache (ignored)
│
├── exceptions.py             # Custom exception classes
├── project_board_base.py     # Abstract base class for boards & tasks
├── project_board.py          # Concrete implementation for boards & tasks
├── team_base.py              # Abstract base class for teams
├── team.py                   # Concrete implementation for teams
├── user_base.py              # Abstract base class for users
├── user.py                   # Concrete implementation for users
├── utils.py                  # Helper functions
│
├── test_app.py               # Demo script to run & test features
├── requirements.txt          # Dependencies
├── README.md                 # This file
└── ProblemStatement.md       # Original problem description
```
---

## ⚡ How to Get the Project

### Option 1 — Clone via Git
git clone https://github.com/Frpratik/AbstractionBasedCRUD.git

### Option 2 — Download as ZIP  
If you don’t want to use Git:

1. Click the green **Code** button in the repository.  
2. Select **Download ZIP**.  
3. Extract the ZIP on your local machine.  
4. Follow the setup steps below.

---

## ⚡ How to Run

### 1️⃣ (Optional) Create a Virtual Environment
python -m venv venv
source venv/bin/activate # Linux/Mac
venv\Scripts\activate # Windows



### 2️⃣ Install Dependencies
pip install -r requirements.txt



### 3️⃣ Run the Demo Script
python test_app.py



---

## 🎯 Sample Output
```plaintext
Creating users...
User created: {"id": "U001", "name": "Pratik", "email": "pratik@example.com"}

Creating teams...
Team created: {"id": "T001", "name": "Backend Ninjas"}

Creating project board...
Board created: {"id": "B001", "name": "API Development"}

Adding tasks...
Task created: {"id": "TSK001", "title": "Implement User API"}

Listing all tasks...
[
{"id": "TSK001", "title": "Implement User API", "status": "Pending"}
]
```

---

## 🧠 Design Choices

- **Abstract Base Classes** → clear separation between interface and implementation  
- **Local JSON Storage** → no database setup, portable, human-readable files  
- **Modular Organization** → independent modules for scalability  
- **Custom Exceptions** → precise error handling  
- **Demo Script** → quick to test and learn


---


## 👨‍💻 Author

**Pratik Ghuge**  
📧 [LinkedIn](https://linkedin.com/in/pratik-ghuge1926)  
🐙 [GitHub](https://github.com/Frpratik)

---

## 📜 License

This project is for **educational and evaluation purposes** only.

**Happy Coding! 🚀**
