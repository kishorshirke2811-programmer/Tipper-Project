import json
import re

class UpdateUser:
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
    
    def find_user_by_identifier(self, identifier, users):
        # Check by User ID
        if identifier in users:
            return identifier, users[identifier]
        
        # Check by Mobile
        for user_id, user_data in users.items():
            if user_data.get('mobile') == identifier:
                return user_id, user_data
        
        return None, None
    
    def update_user(self):
        users = self.load_users()
        
        if not users:
            print("No users found in the system!")
            input("Press Enter to continue...")
            return
        
        print("\n=== UPDATE USER ===")
        
        while True:
            print("Update by: 1. User ID, 2. Mobile Number")
            choice = input("Enter your choice: ").strip()
            
            if choice == "1":
                identifier = input("Enter User ID: ").strip()
                user_id, user = self.find_user_by_identifier(identifier, users)
                if user:
                    break
                else:
                    print("User not found! Please try again.")
            elif choice == "2":
                identifier = input("Enter Mobile Number: ").strip()
                user_id, user = self.find_user_by_identifier(identifier, users)
                if user:
                    break
                else:
                    print("User not found! Please try again.")
            else:
                print("Invalid choice! Please enter 1 or 2.")
        
        print(f"\nCurrent details of {user.get('name')}:")
        print("User ID:", user_id)
        print("1. Name:", user.get('name'))
        print("2. Mobile:", user.get('mobile'))
        print("3. Email:", user.get('email'))
        print("4. Gender:", user.get('gender'))
        print("5. Age:", user.get('age'))
        print("6. Position:", user.get('position'))
        
        while True:
            print("\nWhat would you like to update?")
            print("1. Name, 2. Mobile, 3. Email, 4. Gender, 5. Age, 6. Position")
            choice = input("Enter your choice: ").strip()
            
            if choice == "1":
                while True:
                    new_value = input("Enter new Name: ").strip()
                    if new_value:
                        users[user_id]['name'] = new_value
                        break
                    else:
                        print("Name cannot be empty! Please try again.")
                break
            
            elif choice == "2":
                while True:
                    new_value = input("Enter new Mobile: ").strip()
                    is_valid, msg = self.validate_mobile(new_value)
                    if not is_valid:
                        print(msg)
                        continue
                    
                    # Check mobile uniqueness
                    mobile_exists = False
                    for uid, user_data in users.items():
                        if uid != user_id and user_data.get('mobile') == new_value:
                            print("Mobile number already used by another user!")
                            mobile_exists = True
                            break
                    
                    if not mobile_exists:
                        users[user_id]['mobile'] = new_value
                        break
                break
            
            elif choice == "3":
                while True:
                    new_value = input("Enter new Email: ").strip().lower()
                    is_valid, msg = self.validate_email(new_value)
                    if not is_valid:
                        print(msg)
                        continue
                    
                    # Check email uniqueness
                    email_exists = False
                    for uid, user_data in users.items():
                        if uid != user_id and user_data.get('email') == new_value:
                            print("Email already used by another user!")
                            email_exists = True
                            break
                    
                    if not email_exists:
                        users[user_id]['email'] = new_value
                        break
                break
            
            elif choice == "4":
                while True:
                    new_value = input("Enter new Gender (Male/Female/Other): ").strip().title()
                    if new_value in ['Male', 'Female', 'Other']:
                        users[user_id]['gender'] = new_value
                        break
                    else:
                        print("Invalid gender! Please choose from Male, Female, or Other.")
                break
            
            elif choice == "5":
                while True:
                    new_value = input("Enter new Age: ").strip()
                    try:
                        age = int(new_value)
                        if 1 <= age <= 120:
                            users[user_id]['age'] = age
                            break
                        else:
                            print("Invalid age! Must be between 1-120.")
                    except ValueError:
                        print("Age must be a number! Please try again.")
                break
            
            elif choice == "6":
                positions = ['Manager', 'Owner', 'Driver', 'Blue Collar']
                while True:
                    print("Available positions:", ", ".join(positions))
                    new_value = input("Enter new Position: ").strip().title()
                    if new_value in positions:
                        users[user_id]['position'] = new_value
                        break
                    else:
                        print("Invalid position! Please choose from:", ", ".join(positions))
                break
            
            else:
                print("Invalid choice! Please enter 1-6.")
        
        self.save_users(users)
        print("User details updated successfully!")
        input("Press Enter to continue...")

if __name__ == "__main__":
    UpdateUser().update_user()