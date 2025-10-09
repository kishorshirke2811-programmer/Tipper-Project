"""This is User Management module."""

def add_user():
    """Add a new user."""
    user_name = input("Enter username: ")
    password = input("Enter password: ")
    return {"username": user_name, "password": password}