import json

class GetUser:
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
    
    def get_user_details(self):
        users = self.load_users()
        
        if not users:
            print("No users found in the system!")
            input("Press Enter to continue...")
            return
        
        print("\n=== GET USER DETAILS ===")
        
        while True:
            print("Search by: 1. User ID, 2. Mobile Number, 3. Email")
            choice = input("Enter your choice: ").strip()
            
            if choice == "1":
                identifier = input("Enter User ID: ").strip()
                break
            elif choice == "2":
                identifier = input("Enter Mobile Number: ").strip()
                break
            elif choice == "3":
                identifier = input("Enter Email: ").strip().lower()
                break
            else:
                print("Invalid choice! Please enter 1, 2, or 3.")
        
        user_id, user = self.find_user_by_identifier(identifier, users)
        
        if user:
            print("\nUser Found:")
            print("User ID:", user_id)
            print("Name:", user.get('name'))
            print("Mobile:", user.get('mobile'))
            print("Email:", user.get('email'))
            print("Gender:", user.get('gender'))
            print("Age:", user.get('age'))
            print("Position:", user.get('position'))
        else:
            print("User not found!")
        
        input("Press Enter to continue...")
    
    def get_user_list(self):
        users = self.load_users()
        
        if not users:
            print("No users found in the system!")
            input("Press Enter to continue...")
            return
        
        print("\n=== USER LIST ===")
        print("Total Users:", len(users))
        print()
        
        for user_id, user_data in users.items():
            print("User ID:", user_id)
            print("Name:", user_data.get('name'))
            print("Mobile:", user_data.get('mobile'))
            print("Email:", user_data.get('email'))
            print("Position:", user_data.get('position'))
            print("-" * 40)
        
        input("Press Enter to continue...")

if __name__ == "__main__":
    import sys
    getter = GetUser()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--list':
        getter.get_user_list()
    else:
        getter.get_user_details()
