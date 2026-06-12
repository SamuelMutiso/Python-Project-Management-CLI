# Python Project Management CLI Tool

A command-line application for managing users, projects, and tasks. Built with Python using `argparse`, `tabulate`, and `python-dateutil`. Data is saved locally in JSON files so everything persists between sessions.


## Setup Instructions

### Requirements

- Python 3.10 or higher
- [pipenv] for dependency management

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/python-project-manager.git
cd python-project-manager
```

### 2. Install dependencies

```bash
pip install pipenv
pipenv install
```

### 3. Activate the virtual environment

```bash
pipenv shell
```


---

## How to Run CLI Commands

All commands follow this pattern:

```
python main.py <command> [options]
```

To see help for any command, add `--help`:

```bash
python main.py --help
python main.py add-user --help
```

---

### Users

**Add a user**
```bash
python main.py add-user --name "Alex" --email "alex@example.com"
```

**List all users**
```bash
python main.py list-users
```

---

### Projects

**Add a project** (user must exist first)
```bash
python main.py add-project --user "Alex" --title "CLI Tool" --description "Build the tracker" --due-date "2025-08-01"
```

> `--description` is optional and defaults to "No description provided"

**List projects for a user**
```bash
python main.py list-projects --user "Alex"
```

This also shows task progress (e.g. `2/3 done`) for each project.

---

### Tasks

**Add a task to a project** (project must exist first)
```bash
python main.py add-task --project "CLI Tool" --title "Write tests" --assigned-to "Brian"
```

**Mark a task as complete**
```bash
python main.py complete-task --project "CLI Tool" --title "Write tests"
```

**List all tasks for a project**
```bash
python main.py list-tasks --project "CLI Tool"
```

---

### Full Example Workflow

```bash
# 1. Add users
python main.py add-user --name "Alex" --email "alex@dev.com"
python main.py add-user --name "Brian" --email "brian@dev.com"

# 2. Create a project for Alex
python main.py add-project --user "Alex" --title "CLI Tool" --description "Build the tracker" --due-date "2025-09-01"

# 3. Add tasks to the project
python main.py add-task --project "CLI Tool" --title "Setup argparse" --assigned-to "Alex"
python main.py add-task --project "CLI Tool" --title "Write unit tests" --assigned-to "Brian"

# 4. Check project progress
python main.py list-projects --user "Alex"

# 5. Complete a task
python main.py complete-task --project "CLI Tool" --title "Setup argparse"

# 6. Verify task status
python main.py list-tasks --project "CLI Tool"
```

---

## Features Overview

| Feature | Description |
|---|---|
| User management | Add and list users with email validation |
| Project management | Create projects tied to users with due date validation |
| Task management | Add tasks to projects, assign to team members, mark complete |
| Progress tracking | `list-projects` shows how many tasks are done per project |
| Data persistence | All data saved to local JSON files in `data/` |
| Input validation | Duplicate user detection, unknown user/project checks, invalid date rejection |
| Clean output | Tables formatted with `tabulate` for easy reading |
| OOP design | Inheritance (`Person → User`), `@property` encapsulation, class-level counters |

---

## Project Structure

```
python-project-manager/
├── main.py               # CLI entry point — all commands defined here
├── lib/
│   ├── __init__.py
│   └── models.py         # Person, User, Project, Task class definitions
├── utils/
│   ├── __init__.py
│   └── storage.py        # load_data() and save_data() helpers
├── data/
│   ├── users.json        # persisted user records
│   ├── projects.json     # persisted project records
│   └── tasks.json        # persisted task records
├── tests/
│   ├── __init__.py
│   └── test_models.py    # unit tests for models, storage, and CLI commands
├── Pipfile               # project dependencies
├── Pipfile.lock
└── README.md
```

---

## Running Tests

```bash
pipenv run pytest tests/
```

Tests cover:
- User creation, email validation, inheritance from `Person`
- Task status property, `mark_complete()`, invalid status rejection
- Project `to_dict()` output
- `save_data()` and `load_data()` including missing file handling
- CLI commands: `add_user`, `add_project`, `complete_task` with mocked file paths

---

## Known Issues

- **No update or delete commands** — to edit or remove a user, project, or task you need to manually edit the relevant file in `data/`
- **Email validation is basic** — only checks for the presence of `@`, not full format validation
- **`assigned_to` is a free-text field** — tasks can be assigned to names that don't match any registered user
- **Project titles are case-sensitive for task linking** — `list-projects` matches on lowercase but it's worth being consistent when adding tasks
- **No pagination** — if you have many projects or tasks, they all print at once

---

## Dependencies

| Package | Version | Purpose |
|---|---|---|
| `tabulate` | latest | Formats CLI output as clean grid tables |
| `python-dateutil` | latest | Validates due date input on `add-project` |

Managed via `Pipfile`. Install with `pipenv install`.
