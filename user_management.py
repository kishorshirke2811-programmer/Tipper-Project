import json
import re

class DeleteUser:
    USER_FILE = "users.json"
    
    def load_users(self):
        try:
            with open(self.USER_FILE, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def save_users(self, users):
        with open(self.USER_FILE, 'w') as f:
            json.dump(users, f, indent=4)
    
    def find_user_by_identifier(self, identifier, users):
        # Check by User ID
        if identifier in users:
            return identifier, users[identifier]
        
        # Check by Mobile
        for user_id, user_data in users.items():
            if user_data.get('mobile') == identifier:
                return user_id, user_data
        
        return None, None
    
    def delete_user(self):
        users = self.load_users()
        
        if not users:
            print("No users found in the system!")
            input("Press Enter to continue...")
            return
        
        print("\n=== DELETE USER ===")
        
        while True:
            print("Delete by: 1. User ID, 2. Mobile Number")
            choice = input("Enter your choice: ").strip()
            
            if choice == "1":
                identifier = input("Enter User ID: ").strip()
                break
            elif choice == "2":
                identifier = input("Enter Mobile Number: ").strip()
                break
            else:
                print("Invalid choice! Please enter 1 or 2.")
        
        user_id, user = self.find_user_by_identifier(identifier, users)
        
        if not user:
            print("User not found!")
            input("Press Enter to continue...")
            return
        
        print("User Found:", user.get('name'))
        
        # Verify password
        while True:
            password = input("Enter password for verification: ").strip()
            if password == user.get('password'):
                break
            else:
                print("Incorrect password! Please try again.")
        
        # Confirm deletion
        while True:
            confirm = input(f"Are you sure you want to delete user '{user.get('name')}'? (yes/no): ").strip().lower()
            if confirm in ['yes', 'no']:
                break
            else:
                print("Please enter 'yes' or 'no'.")
        
        if confirm == 'yes':
            del users[user_id]
            self.save_users(users)
            print("User deleted successfully!")
        else:
            print("Deletion cancelled.")
        
        input("Press Enter to continue...")