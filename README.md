# Todo API with Authentication + Python CLI Tools

A simple and fully functional **Todo API** built with **FastAPI**, featuring **JWT authentication**, **SQLite database**, and an easy-to-use **Python CLI tool** to interact with it.


## Features

- User signup and login with hashed passwords  
- JWT-based authentication  
- Each user has their own todos  
- Full CRUD (Create, Read, Update, Delete)  
- CLI tool for command-line interaction  
- SQLite + SQLModel backend  
- Clean and readable code structure  

---

## Project Structure


todo_project/
│
├── backend/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   │
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   ├── hashing.py
│   │   └── jwt_handler.py
│   │
│   ├── todo/
│   │   ├── __init__.py
│   │   └── routes.py
│
├── cli.py
├── requirements.txt
├── .gitignore
├── README.md
├── database.db
└── token.txt


---

## Installation

```bash
cd ~/Documents/todo_project
python3 -m venv todo_env
source todo_env/bin/activate
python3 -m pip install -r requirements.txt
```

---

## Run the FastAPI Server

```bash
python3 -m uvicorn backend.main:app --port 8003
```

Then open your browser at:  
    http://127.0.0.1:8003/docs

---

## CLI Commands

Run all commands from a new terminal (with environment activated):

### Signup
```bash
python cli.py signup --username <username> --password <password>
```

### Login
```bash
python cli.py login --username <username> --password <password>
```

### Who Am I
```bash
python cli.py whoami
```

### Add Todo
```bash
python cli.py add-todo --title "Buy milk" --description "2 litres"
```

### List Todos
```bash
python cli.py list-todos
```

### Update Todo
```bash
python cli.py update-todo --id <todo_id> --completed True
```

### Delete Todo
```bash
python cli.py delete-todo --id <todo_id>
```

### Logout
```bash
python cli.py logout
```

---

## .gitignore Example

```
todo_env/
__pycache__/
.DS_Store
token.txt
database.db
```

---

## user and pass

User1 - raj
Pass1 - 1234

User2 - rajdeep
Pass2 - 4321

User3 - hb
Pass - 1234

User4 - stepuser
Pass - pass1234

---