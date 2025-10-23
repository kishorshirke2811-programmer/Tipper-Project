import json
import re
import random
from datetime import datetime, date


class UserManagementSystem:
    def __init__(self):
        self.file = "users.json"

    def load_users(self):
        try:
            with open(self.file, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_users(self, users):
        with open(self.file, "w") as f:
            json.dump(users, f, indent=4)

    def validate_name(self, name):
        return bool(re.match(r"^[A-Za-z ]+$", name)) and len(name) <= 50

    def validate_email(self, email):
        return bool(re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email))

    def validate_mobile(self, mobile):
        return bool(re.match(r"^[6-9]\d{9}$", mobile))

    def validate_password(self, password):
        if len(password) < 8:
            print("Password must be at least 8 characters long.")
            return False
        if not re.search(r"[A-Z]", password):
            print("Password must contain an uppercase letter.")
            return False
        if not re.search(r"[a-z]", password):
            print("Password must contain a lowercase letter.")
            return False
        if not re.search(r"\d", password):
            print("Password must contain a digit.")
            return False
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            print("Password must contain a special character.")
            return False
        return True

    def get_age_from_dob(self, dob):
        try:
            dob_date = datetime.strptime(dob, "%d-%m-%Y").date()
            today = date.today()
            age = today.year - dob_date.year - ((today.month, today.day) < (dob_date.month, dob_date.day))
            return age
        except ValueError:
            return None

    def verify_password(self, user):
        for _ in range(3):
            pwd = input("Enter Password for Verification: ").strip()
            if pwd == user["password"]:
                return True
            print("Incorrect password.")
        print("Verification failed.")
        return False

    def create_user(self):
        print("\n=== CREATE USER ===")
        users = self.load_users()

        while True:
            name = input("Enter Name: ").strip()
            if name.lower() == "exit":
                return
            if self.validate_name(name):
                break
            print("Invalid name! Use only alphabets and spaces (max 50 chars).")

        while True:
            mobile = input("Enter Mobile (10 digits): ").strip()
            if mobile.lower() == "exit":
                return
            if self.validate_mobile(mobile):
                if any(u['mobile'] == mobile for u in users.values()):
                    print("Mobile already registered.")
                else:
                    break
            else:
                print("Invalid mobile number.")

        while True:
            email = input("Enter Email: ").strip()
            if email.lower() == "exit":
                return
            if self.validate_email(email):
                if any(u['email'] == email for u in users.values()):
                    print("Email already registered.")
                else:
                    break
            else:
                print("Invalid email format.")

        while True:
            gender = input("Enter Gender (Male/Female/Other): ").strip().title()
            if gender.lower() == "exit":
                return
            if gender in ["Male", "Female", "Other"]:
                break
            print("Invalid gender.")

        while True:
            dob = input("Enter Date of Birth (DD-MM-YYYY): ").strip()
            if dob.lower() == "exit":
                return
            age = self.get_age_from_dob(dob)
            if age is None:
                print("Invalid date format or date.")
                continue
            if age < 18:
                print("User must be at least 18 years old.")
                continue
            break

        while True:
            position = input("Enter Position (Manager/Owner/Driver/Bluecollar): ").strip().title()
            if position.lower() == "exit":
                return
            if position in ["Manager", "Owner", "Driver", "Bluecollar"]:
                break
            print("Invalid position!")

        while True:
            password = input("Create Password: ").strip()
            if password.lower() == "exit":
                return
            if not self.validate_password(password):
                continue
            confirm = input("Confirm Password: ").strip()
            if password != confirm:
                print("Passwords do not match.")
            else:
                break

        # Validate age based on position
        if position in ["Manager", "Owner"] and not (18 <= age <= 120):
            print("For Manager/Owner, age must be between 18 and 120.")
            return
        elif position in ["Driver", "Bluecollar"] and not (18 <= age <= 60):
            print("For Driver/Bluecollar, age must be between 18 and 60.")
            return

        user_id = f"{name.split()[0].lower()}{random.randint(1000,9999)}"
        users[user_id] = {
            "name": name,
            "mobile": mobile,
            "email": email,
            "gender": gender,
            "dob": dob,
            "age": age,
            "position": position,
            "password": password
        }

        self.save_users(users)
        print(f"User Registered Successfully! Your User ID: {user_id}")

    def get_user_details(self):
        users = self.load_users()
        if not users:
            print("No users found.")
            return
        identifier = input("Enter User ID or Mobile: ").strip()
        for uid, u in users.items():
            if uid == identifier or u["mobile"] == identifier:
                print(f"\nUser ID: {uid}")
                for k, v in u.items():
                    if k != "password":
                        print(f"{k.title()}: {v}")
                return
        print("User not found.")

    def get_all_users(self):
        users = self.load_users()
        if not users:
            print("No users found.")
            return
        for uid, u in users.items():
            print(f"\nUser ID: {uid}")
            for k, v in u.items():
                if k != "password":
                    print(f"{k.title()}: {v}")

    def update_user(self):
        print("\n=== UPDATE USER ===")
        users = self.load_users()
        if not users:
            print("No users found.")
            return

        identifier = input("Enter User ID or Mobile to update: ").strip()
        for uid, user in users.items():
            if uid == identifier or user["mobile"] == identifier:
                if not self.verify_password(user):
                    print("Password verification failed. Cannot update.")
                    return

                while True:
                    print("\n1. Name\n2. Mobile\n3. Email\n4. Gender\n5. DOB\n6. Position\n0. Exit Update")
                    choice = input("Enter field to update: ").strip()

                    if choice == "0":
                        print("Update session ended.")
                        break

                    elif choice == "1":
                        new_name = input("New Name: ").strip()
                        if self.validate_name(new_name):
                            user["name"] = new_name
                            print("Name updated.")
                        else:
                            print("Invalid name.")

                    elif choice == "2":
                        new_mobile = input("New Mobile: ").strip()
                        if self.validate_mobile(new_mobile):
                            user["mobile"] = new_mobile
                            print("Mobile updated.")
                        else:
                            print("Invalid mobile.")

                    elif choice == "3":
                        new_email = input("New Email: ").strip()
                        if self.validate_email(new_email):
                            user["email"] = new_email
                            print("Email updated.")
                        else:
                            print("Invalid email format.")

                    elif choice == "4":
                        new_gender = input("New Gender (Male/Female/Other): ").strip().title()
                        if new_gender in ["Male", "Female", "Other"]:
                            user["gender"] = new_gender
                            print("Gender updated.")
                        else:
                            print("Invalid gender.")

                    elif choice == "5":
                        new_dob = input("New DOB (DD-MM-YYYY): ").strip()
                        age = self.get_age_from_dob(new_dob)
                        if age and age >= 18:
                            user["dob"] = new_dob
                            user["age"] = age
                            print("DOB and age updated.")
                        else:
                            print("Invalid or underage DOB.")

                    elif choice == "6":
                        new_pos = input("New Position (Manager/Owner/Driver/Bluecollar): ").strip().title()
                        if new_pos in ["Manager", "Owner", "Driver", "Bluecollar"]:
                            user["position"] = new_pos
                            print("Position updated.")
                        else:
                            print("Invalid position.")

                    else:
                        print("Invalid choice.")

                    self.save_users(users)
                return
        print("User not found.")

    def delete_user(self):
        print("\n=== DELETE USER ===")
        users = self.load_users()
        if not users:
            print("No users found.")
            return
        identifier = input("Enter User ID or Mobile to delete: ").strip()
        for uid, u in users.items():
            if uid == identifier or u["mobile"] == identifier:
                if not self.verify_password(u):
                    print("Password verification failed. Cannot delete user.")
                    return
                confirm = input(f"Are you sure you want to delete user {u['name']}? (yes/no): ").strip().lower()
                if confirm == "yes":
                    del users[uid]
                    self.save_users(users)
                    print("User deleted successfully.")
                    return
                else:
                    print("Deletion cancelled.")
                    return
        print("User not found.")

    def password_management(self):
        print("\n=== PASSWORD MANAGEMENT ===")
        users = self.load_users()
        if not users:
            print("No users found.")
            return

        print("1. Change Password\n2. Forgot Password")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            identifier = input("Enter User ID or Mobile: ").strip()
            for uid, u in users.items():
                if uid == identifier or u["mobile"] == identifier:
                    if not self.verify_password(u):
                        print("Password verification failed.")
                        return
                    while True:
                        new_pwd = input("Enter New Password: ").strip()
                        if not self.validate_password(new_pwd):
                            continue
                        confirm_pwd = input("Confirm Password: ").strip()
                        if new_pwd == confirm_pwd:
                            u["password"] = new_pwd
                            self.save_users(users)
                            print("Password updated successfully.")
                            return
                        print("Passwords do not match.")
            print("User not found.")

        elif choice == "2":
            uid = input("Enter User ID: ").strip()
            mob = input("Enter Mobile: ").strip()
            email = input("Enter Email: ").strip()
            for u in users.values():
                if u["email"] == email and u["mobile"] == mob:
                    while True:
                        new_pwd = input("Enter New Password: ").strip()
                        if not self.validate_password(new_pwd):
                            continue
                        confirm_pwd = input("Confirm Password: ").strip()
                        if new_pwd == confirm_pwd:
                            u["password"] = new_pwd
                            self.save_users(users)
                            print("Password reset successfully.")
                            return
                        print("Passwords do not match.")
            print("Verification failed.")

    def login(self):
        users = self.load_users()
        if not users:
            print("No users found.")
            return
        identifier = input("Enter User ID or Mobile: ").strip()
        pwd = input("Enter Password: ").strip()
        for uid, u in users.items():
            if (uid == identifier or u["mobile"] == identifier) and u["password"] == pwd:
                print(f"Welcome {u['name']}! Login successful.")
                return
        print("Invalid credentials.")


def main():
    system = UserManagementSystem()
    while True:
        print("\n=== USER MANAGEMENT SYSTEM ===")
        print("1. Create User")
        print("2. Get User Details")
        print("3. Get All Users")
        print("4. Update User")
        print("5. Delete User")
        print("6. Password Management")
        print("7. Login")
        print("0. Exit")

        choice = input("Enter choice: ").strip()
        if choice == "1":
            system.create_user()
        elif choice == "2":
            system.get_user_details()
        elif choice == "3":
            system.get_all_users()
        elif choice == "4":
            system.update_user()
        elif choice == "5":
            system.delete_user()
        elif choice == "6":
            system.password_management()
        elif choice == "7":
            system.login()
        elif choice == "0":
            print("Exiting system. Goodbye!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
