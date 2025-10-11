import json
import re
import random
import string

class CreateUser:
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
    
    def validate_email(self, email):
        pattern = r'^[a-z0-9._%+-]+@gmail\.com$'
        if not re.match(pattern, email.lower()):
            return False, "Invalid email! Must be @gmail.com domain."
        return True, "Valid email"
    
    def validate_mobile(self, mobile):
        if not re.match(r'^\d{10}$', mobile):
            return False, "Invalid mobile number! Must be 10 digits."
        return True, "Valid mobile number"
    
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
    
    def generate_user_id(self):
        return 'USER' + ''.join(random.choices(string.digits, k=6))
    
    def get_input_with_validation(self, prompt, validation_func=None, error_msg=None):
        while True:
            value = input(prompt).strip()
            if not value:
                print("This field cannot be empty. Please try again.")
                continue
            
            if validation_func:
                is_valid, message = validation_func(value)
                if not is_valid:
                    print(message)
                    continue
            
            return value
    
    def create_user(self):
        users = self.load_users()
        
        print("\n=== CREATE USER ===")
        
        # Name
        name = self.get_input_with_validation("Enter Name: ")
        
        # Mobile Number
        while True:
            mobile = input("Enter Mobile Number: ").strip()
            is_valid, msg = self.validate_mobile(mobile)
            if not is_valid:
                print(msg)
                continue
            
            # Check if mobile already exists
            mobile_exists = False
            for user_data in users.values():
                if user_data.get('mobile') == mobile:
                    print("Mobile number already registered! Please use a different number.")
                    mobile_exists = True
                    break
            
            if not mobile_exists:
                break
        
        # Email
        while True:
            email = input("Enter Email: ").strip().lower()
            is_valid, msg = self.validate_email(email)
            if not is_valid:
                print(msg)
                continue
            
            # Check if email already exists
            email_exists = False
            for user_data in users.values():
                if user_data.get('email') == email:
                    print("Email already registered! Please use a different email.")
                    email_exists = True
                    break
            
            if not email_exists:
                break
        
        # Gender
        while True:
            gender = input("Enter Gender (Male/Female/Other): ").strip().title()
            if gender in ['Male', 'Female', 'Other']:
                break
            else:
                print("Invalid gender! Please choose from Male, Female, or Other.")
        
        # Age
        while True:
            age_input = input("Enter Age: ").strip()
            try:
                age = int(age_input)
                if 1 <= age <= 120:
                    break
                else:
                    print("Invalid age! Must be between 1-120.")
            except ValueError:
                print("Age must be a number! Please try again.")
        
        # Position
        positions = ['Manager', 'Owner', 'Driver', 'Blue Collar']
        while True:
            print("Available positions:", ", ".join(positions))
            position = input("Enter Position: ").strip().title()
            if position in positions:
                break
            else:
                print("Invalid position! Please choose from:", ", ".join(positions))
        
        # Password
        while True:
            password = input("Enter Password: ").strip()
            is_valid, msg = self.validate_password(password)
            if not is_valid:
                print(msg)
                continue
            
            confirm_password = input("Confirm Password: ").strip()
            if password != confirm_password:
                print("Passwords do not match! Please try again.")
                continue
            break
        
        # Generate User ID
        user_id = self.generate_user_id()
        while user_id in users:
            user_id = self.generate_user_id()
        
        # Save user data
        users[user_id] = {
            "name": name,
            "mobile": mobile,
            "email": email,
            "gender": gender,
            "age": age,
            "position": position,
            "password": password
        }
        
        self.save_users(users)
        print("\nUser created successfully!")
        print("Your User ID:", user_id)
        input("Press Enter to continue...")