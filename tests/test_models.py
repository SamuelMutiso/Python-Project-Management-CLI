# Unit tests for the Project Tracker models and storage utilities

import os
import pytest
from lib.models import User, Project, Task
from utils.storage import load_data, save_data


# User tests

def test_user_has_correct_name_and_email():
    user = User(name="Alex", email="Alex@student.com")
    assert user.name == "Alex"
    assert user.email == "Alex@student.com"


def test_user_inherits_from_person():
    # User should have a .name attribute from the Person base class
    user = User(name="Brian", email="Brian@test.com")
    assert hasattr(user, "name")
    assert user.name == "Brian"


def test_email_setter_rejects_invalid_email():
    user = User(name="Test", email="valid@email.com")
    with pytest.raises(ValueError):
        user.email = "notanemail.com"


def test_email_setter_accepts_valid_email():
    user = User(name="Test", email="valid@email.com")
    user.email = "newemail@domain.com"
    assert user.email == "newemail@domain.com"


def test_user_to_dict():
    user = User(name="Diana", email="diana@example.com")
    d = user.to_dict()
    assert d["name"] == "Diana"
    assert d["email"] == "diana@example.com"


def test_user_str():
    user = User(name="Eve", email="eve@test.com")
    assert "Eve" in str(user)
    assert "eve@test.com" in str(user)


# Task tests
def test_task_default_status_is_pending():
    task = Task(title="Write tests", project_title="CLI Tool", assigned_to="Alex")
    assert task.status == "pending"


def test_task_mark_complete():
    task = Task(title="Write tests", project_title="CLI Tool", assigned_to="Alex")
    task.mark_complete()
    assert task.status == "completed"


def test_task_status_setter_rejects_invalid():
    task = Task(title="Write tests", project_title="CLI Tool", assigned_to="Alex")
    with pytest.raises(ValueError):
        task.status = "in-progress"  # not allowed


def test_task_to_dict_contains_expected_keys():
    task = Task(title="Deploy app", project_title="Backend", assigned_to="Brian")
    d = task.to_dict()
    assert "title" in d
    assert "project_title" in d
    assert "assigned_to" in d
    assert "status" in d

# Project tests 

def test_project_to_dict():
    project = Project(title="My App", description="A cool app", due_date="2025-09-01", owner="Alex")
    d = project.to_dict()
    assert d["title"] == "My App"
    assert d["owner"] == "Alex"


# Storage tests 

def test_save_and_load_data(tmp_path):
    test_file = str(tmp_path / "test_data.json")
    sample = [{"name": "Charlie", "email": "charlie@test.com"}]

    save_data(test_file, sample)
    assert os.path.exists(test_file)

    loaded = load_data(test_file)
    assert loaded == sample


def test_load_returns_empty_list_for_missing_file(tmp_path):
    missing = str(tmp_path / "nonexistent.json")
    result = load_data(missing)
    assert result == []

from unittest.mock import patch, MagicMock
from main import add_user, add_project, complete_task

def test_add_user_saves_to_file(tmp_path):
    users_file = str(tmp_path / "users.json")
    save_data(users_file, [])
    with patch("main.USERS_FILE", users_file):
        args = MagicMock()
        args.name = "TestUser"
        args.email = "test@test.com"
        add_user(args)
        result = load_data(users_file)
        assert any(u["name"] == "TestUser" for u in result)

def test_add_user_rejects_duplicate(tmp_path, capsys):
    users_file = str(tmp_path / "users.json")
    save_data(users_file, [{"name": "Alex", "email": "alex@test.com"}])
    with patch("main.USERS_FILE", users_file):
        args = MagicMock()
        args.name = "Alex"
        args.email = "alex@test.com"
        add_user(args)
        assert "already exists" in capsys.readouterr().out

def test_complete_task_updates_status(tmp_path):
    tasks_file = str(tmp_path / "tasks.json")
    save_data(tasks_file, [{"title": "Fix bug", "project_title": "MyApp", "assigned_to": "Alex", "status": "pending"}])
    with patch("main.TASKS_FILE", tasks_file):
        args = MagicMock()
        args.title = "Fix bug"
        args.project = "MyApp"
        complete_task(args)
        assert load_data(tasks_file)[0]["status"] == "completed"

def test_add_project_rejects_unknown_user(tmp_path, capsys):
    users_file = str(tmp_path / "users.json")
    save_data(users_file, [])
    with patch("main.USERS_FILE", users_file):
        args = MagicMock()
        args.user = "Ghost"
        args.title = "X"
        args.description = "desc"
        args.due_date = "2025-09-01"
        add_project(args)
        assert "No user named" in capsys.readouterr().out