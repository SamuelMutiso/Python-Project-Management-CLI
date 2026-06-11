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
