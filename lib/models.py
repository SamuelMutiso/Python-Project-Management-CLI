# Models for the project tracker
# Defines Person, User, Project, and Task classes

class Person:
    # Base class - holds common attributes shared by all people in the system
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Person(name={self.name})"


class User(Person):

    # Class attribute - tracks total users created across the system
    _count = 0


    # Inherits from Person, adds email with validation
    def __init__(self, name, email):
        super().__init__(name)
        self.email = email  # private, validated through property setter
        User._count += 1    # Increment the class-level counter

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        # basic email check - just make sure there's an @ symbol
        if "@" not in value:
            raise ValueError(f"'{value}' doesn't look like a valid email address.")
        self._email = value

    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email
        }

    def __str__(self):
        return f"{self.name} ({self.email})"

    def __repr__(self):
        return f"User(name={self.name}, email={self.email})"

# class project
class Project:

    # Class attribute - tracks total projects created across the system
    _count = 0


    # Represents a project that belongs to a user
    def __init__(self, title, description, due_date, owner):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.owner = owner  # username string - links project to a user
        Project._count += 1 # Increment the class-level counter

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "owner": self.owner
        }

    def __str__(self):
        return f"[{self.title}] owned by {self.owner} | due: {self.due_date}"

    def __repr__(self):
        return f"Project(title={self.title}, owner={self.owner})"

# class task
class Task:
    # Class attribute - tracks total tasks created across the system
    _count = 0


    
    # status is controlled through a property to prevent bad values
    VALID_STATUSES = ["pending", "completed"]

    def __init__(self, title, project_title, assigned_to, status="pending"):
        self.title = title
        self.project_title = project_title
        self.assigned_to = assigned_to
        self._status = status.lower()
        Task._count += 1    # Increment the class-level counter

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if value.lower() not in self.VALID_STATUSES:
            raise ValueError(f"Status must be one of {self.VALID_STATUSES}, got '{value}'")
        self._status = value.lower()

    def mark_complete(self):
        self._status = "completed"

    def to_dict(self):
        return {
            "title": self.title,
            "project_title": self.project_title,
            "assigned_to": self.assigned_to,
            "status": self.status
        }

    def __str__(self):
        return f"Task: {self.title} | Project: {self.project_title} | Assigned: {self.assigned_to} | Status: {self.status}"

    def __repr__(self):
        return f"Task(title={self.title}, status={self.status})"


