# Models for the project tracker
# Defines Person, User, Project, and Task classes

class Person:
    # Base class - holds common attributes shared by all people in the system
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Person(name={self.name})"


class User(Person):
    # Inherits from Person, adds email with validation
    def __init__(self, name, email):
        super().__init__(name)
        self._email = email  # private, validated through property setter

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