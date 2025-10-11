import json

class Login:
    USER_FILE = "users.json"
    
    def load_users(self):
        try:
            with open(self.USER_FILE, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def find_user_by_identifier(self, identifier, users):
        # Check by User ID
        if identifier in users:
            return users[identifier]
        
        # Check by Mobile
        for user_data in users.values():
            if user_data.get('mobile') == identifier:
                return user_data
        
        # Check by Email
        for user_data in users.values():
            if user_data.get('email') == identifier.lower():
                return user_data
        
        return None
    
    def login(self):
        users = self.load_users()
        
        if not users:
            print("No users found in the system!")
            input("Press Enter to continue...")
            return
        
        print("\n=== LOGIN ===")
        
        while True:
            identifier = input("Enter User ID / Mobile Number / Email: ").strip()
            user = self.find_user_by_identifier(identifier, users)
            if user:
                break
            else:
                print("User not found! Please try again.")
        
        while True:
            password = input("Enter Password: ").strip()
            if password == user.get('password'):
                print("\nLogin successful!")
                print("Welcome,", user.get('name'))
                print("Position:", user.get('position'))
                break
            else:
                print("Invalid password! Please try again.")
        
        input("Press Enter to continue...")