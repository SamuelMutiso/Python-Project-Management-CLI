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

# Project commands 

def add_project(args):
    """Add a new project under an existing user."""
    users = load_data(USERS_FILE)
    user_names = [u["name"].lower() for u in users]

    if args.user.lower() not in user_names:
        print(f"No user named '{args.user}' found. Please add them first.")
        return

    projects = load_data(PROJECTS_FILE)
    project = Project(
        title=args.title,
        description=args.description,
        due_date=args.due_date,
        owner=args.user
    )
    projects.append(project.to_dict())
    save_data(PROJECTS_FILE, projects)
    print(f"Project '{args.title}' added for {args.user}.")


def list_projects(args):
    """Show all projects for a given user, with task progress."""
    projects = load_data(PROJECTS_FILE)
    tasks = load_data(TASKS_FILE)

# filter down to this user's projects
    user_projects = [p for p in projects if p["owner"].lower() == args.user.lower()]

    if not user_projects:
        print(f"No projects found for '{args.user}'.")
        return

    rows = []
    for p in user_projects:
        # count how many tasks are done vs total
        project_tasks = [t for t in tasks if t["project_title"].lower() == p["title"].lower()]
        done = sum(1 for t in project_tasks if t["status"] == "completed")
        total = len(project_tasks)
        progress = f"{done}/{total} done" if total > 0 else "no tasks yet"

        rows.append([p["title"], p["description"], p["due_date"], progress])

    print(f"\nProjects for {args.user}:")
    print(tabulate(rows, headers=["Title", "Description", "Due Date", "Progress"], tablefmt="grid"))


# Task commands 

def add_task(args):
    """Add a task to an existing project."""
    projects = load_data(PROJECTS_FILE)
    project_titles = [p["title"].lower() for p in projects]

    if args.project.lower() not in project_titles:
        print(f"No project named '{args.project}' found.")
        return

    tasks = load_data(TASKS_FILE)
    task = Task(
        title=args.title,
        project_title=args.project,
        assigned_to=args.assigned_to
    )
    tasks.append(task.to_dict())
    save_data(TASKS_FILE, tasks)
    print(f"Task '{args.title}' added to '{args.project}', assigned to {args.assigned_to}.")


def complete_task(args):
    """Mark a specific task as completed."""
    tasks = load_data(TASKS_FILE)
    found = False

    for t in tasks:
        if (t["title"].lower() == args.title.lower() and
                t["project_title"].lower() == args.project.lower()):
            task = Task(
                title=t["title"],
                project_title=t["project_title"],
                assigned_to=t["assigned_to"],
                status=t["status"]
            )
            task.mark_complete()
            t["status"] = task.status
            found = True
            break

    if found:
        save_data(TASKS_FILE, tasks)
        print(f"Task '{args.title}' marked as completed.")
    else:
        print(f"Task '{args.title}' in project '{args.project}' not found.")


def list_tasks(args):
    """Show all tasks for a given project."""
    tasks = load_data(TASKS_FILE)
    project_tasks = [t for t in tasks if t["project_title"].lower() == args.project.lower()]

    if not project_tasks:
        print(f"No tasks found for project '{args.project}'.")
        return

    rows = [[t["title"], t["assigned_to"], t["status"]] for t in project_tasks]
    print(f"\nTasks for '{args.project}':")
    print(tabulate(rows, headers=["Task", "Assigned To", "Status"], tablefmt="grid"))