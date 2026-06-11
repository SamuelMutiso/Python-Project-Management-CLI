# main.py - this is like entry point for the Project Tracker CLI
# Run with: python main.py <command> [options]

import argparse
from tabulate import tabulate

from lib.models import User, Project, Task
from utils.storage import (
    USERS_FILE, PROJECTS_FILE, TASKS_FILE,
    load_data, save_data
)


# User commands 

def add_user(args):
    """Add a new user to the system."""
    users = load_data(USERS_FILE)

    # check if user already exists
    for u in users:
        if u["name"].lower() == args.name.lower():
            print(f"A user named '{args.name}' already exists.")
            return

    try:
        user = User(name=args.name, email=args.email)
        users.append(user.to_dict())
        save_data(USERS_FILE, users)
        print(f"User added: {user}")
    except ValueError as e:
        print(f"Error: {e}")


def list_users(args):
    """Print all registered users."""
    users = load_data(USERS_FILE)

    if not users:
        print("No users found. Add one with: python main.py add-user --name ... --email ...")
        return

    rows = [[u["name"], u["email"]] for u in users]
    print(tabulate(rows, headers=["Name", "Email"], tablefmt="grid"))