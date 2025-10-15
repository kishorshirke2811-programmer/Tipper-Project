import json
import re

class PasswordManagement:
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
    
    def validate_password(self, password):
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter"
        if not re.search(r'[a-z]', password):
            return False, "Password must contain at least one lowercase letter"
        if not re.search(r'[0-9]', password):
            return False, "Password must contain at least one digit"
        if not re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/|\\]', password):
            return False, "Password must contain at least one special character"
        return True, "Strong password"
    
    def find_user_by_identifier(self, identifier):
        users = self.load_users()
        
        # Check by User ID
        if identifier in users:
            return identifier, users[identifier]
        
        # Check by Mobile
        for user_id, user_data in users.items():
            if user_data.get('mobile') == identifier:
                return user_id, user_data
        
        # Check by Email
        for user_id, user_data in users.items():
            if user_data.get('email') == identifier.lower():
                return user_id, user_data
        
        return None, None
    
    def create_password(self):
        print("\n=== CREATE PASSWORD ===")
        
        while True:
            identifier = input("Enter User ID / Mobile Number / Email: ").strip()
            user_id, user = self.find_user_by_identifier(identifier)
            if user:
                break
            else:
                print("User not found! Please try again.")
        
        print("User Found:", user.get('name'))
        
        while True:
            password = input("Enter new password: ").strip()
            is_valid, msg = self.validate_password(password)
            if not is_valid:
                print(msg)
                continue
            
            confirm_password = input("Confirm password: ").strip()
            if password != confirm_password:
                print("Passwords do not match! Please try again.")
                continue
            
            break
        
        users = self.load_users()
        users[user_id]['password'] = password
        self.save_users(users)
        print("Password created successfully!")
        input("Press Enter to continue...")
    
    def forgot_password(self):
        print("\n=== FORGOT PASSWORD ===")
        
        while True:
            identifier = input("Enter User ID / Mobile Number / Email: ").strip()
            user_id, user = self.find_user_by_identifier(identifier)
            if user:
                break
            else:
                print("User not found! Please try again.")
        
        print("User Found:", user.get('name'))
        
        # Verify identity
        while True:
            input_mobile = input("Enter your registered mobile number: ").strip()
            input_email = input("Enter your registered email: ").strip().lower()
            
            if input_mobile == user.get('mobile') and input_email == user.get('email'):
                break
            else:
                print("Mobile or email doesn't match our records! Please try again.")
        
        while True:
            new_password = input("Enter new password: ").strip()
            is_valid, msg = self.validate_password(new_password)
            if not is_valid:
                print(msg)
                continue
            
            if new_password == user.get('password'):
                print("New password cannot be same as old password! Please try again.")
                continue
            
            confirm_password = input("Confirm new password: ").strip()
            if new_password != confirm_password:
                print("Passwords do not match! Please try again.")
                continue
            
            break
        
        users = self.load_users()
        users[user_id]['password'] = new_password
        self.save_users(users)
        print("Password reset successfully!")
        input("Press Enter to continue...")
    
    def create_forgot_password(self):
        print("\n=== PASSWORD MANAGEMENT ===")
        
        while True:
            print("1. Create Password")
            print("2. Forgot Password")
            choice = input("Enter your choice: ").strip()
            
            if choice == "1":
                self.create_password()
                break
            elif choice == "2":
                self.forgot_password()
                break
            else:
                print("Invalid choice! Please enter 1 or 2.")