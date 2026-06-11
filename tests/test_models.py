# tests/test_models.py
# Unit tests for the Project Tracker models and storage utilities

import os
import pytest
from lib.models import User, Project, Task
from utils.storage import load_data, save_data


# --- User tests ---

def test_user_has_correct_name_and_email():
    user = User(name="Alex", email="alex@student.com")
    assert user.name == "Alex"
    assert user.email == "alex@student.com"


def test_user_inherits_from_person():
    # User should have a .name attribute from the Person base class
    user = User(name="Brian", email="brian@test.com")
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