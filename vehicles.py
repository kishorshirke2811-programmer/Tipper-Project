import json
import random
import re

# -----------------------------
# User Management
# -----------------------------
class UserManagement:
    USER_FILE = "users.json"

    def load_users(self):
        try:
            with open(self.USER_FILE, "r") as f:
                data = json.load(f)
                users_list = []
                for uid, details in data.items():
                    user = details.copy()
                    user["user_id"] = uid
                    user["role"] = details.get("position", "").lower()  # map 'position' to 'role'
                    users_list.append(user)
                return users_list
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def list_drivers(self):
        users = self.load_users()
        return [{"user_id": u.get("user_id"), "name": u.get("name")}
                for u in users if u.get("role") == "driver"]

    def list_managers(self):
        users = self.load_users()
        return [{"user_id": u.get("user_id"), "name": u.get("name")}
                for u in users if u.get("role") == "manager"]

    def get_user_by_id(self, user_id, role):
        users = self.load_users()
        for u in users:
            if u.get("user_id", "").upper() == user_id.upper() and u.get("role") == role.lower():
                return u
        return None

# -----------------------------
# Vehicle Management
# -----------------------------
class VehicleManagement:
    VEHICLE_FILE = "vehicles.json"

    def __init__(self):
        self.um = UserManagement()

    # -----------------------------
    # Load & Save
    # -----------------------------
    def normalize_vehicles(self, vehicles):
        updated = False
        for v in vehicles:
            if "vehicle_id" not in v: v["vehicle_id"] = self.generate_vehicle_id(vehicles); updated = True
            if "vehicle_number" not in v: v["vehicle_number"] = "-"; updated = True
            if "engine_number" not in v: v["engine_number"] = "-"; updated = True
            if "chassis_number" not in v: v["chassis_number"] = "-"; updated = True
            if "manager_name" not in v: v["manager_name"] = "-"; updated = True
            if "driver_assigned" not in v: v["driver_assigned"] = "Not Assigned"; updated = True
            if "driver_id" not in v: v["driver_id"] = None; updated = True
            if "model" not in v: v["model"] = "TATA Prima E.28K"; updated = True
        return updated

    def load_vehicles(self):
        try:
            with open(self.VEHICLE_FILE, "r") as f:
                vehicles = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            vehicles = []

        if self.normalize_vehicles(vehicles):
            self.save_vehicles(vehicles)
            print("Some old vehicle records were missing fields. Defaults applied.")

        return vehicles

    def save_vehicles(self, data):
        with open(self.VEHICLE_FILE, "w") as f:
            json.dump(data, f, indent=4)

    # -----------------------------
    # Generate Vehicle ID
    # -----------------------------
    def generate_vehicle_id(self, vehicles):
        existing = [v.get("vehicle_id", "") for v in vehicles]
        while True:
            vid = "VID-" + "".join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") for _ in range(6))
            if vid not in existing:
                return vid

    # -----------------------------
    # Validators
    # -----------------------------
    def validate_vehicle_number(self, vnum):
        return re.match(r"^[A-Z]{2}\d{2}[A-Z]{2}\d{4}$", vnum)

    def validate_engine_number(self, eng):
        return re.match(r"^[A-Z]{1}\d{3}[A-Z]{4}\d{5}$", eng)

    def validate_chassis_number(self, ch):
        """Standard VIN validation (17 chars, letters except I/O/Q, digits 0-9)"""
        return re.match(r"^[A-HJ-NPR-Z0-9]{17}$", ch.upper())

    # -----------------------------
    # Create Vehicle
    # -----------------------------
    def create_vehicle(self):
        vehicles = self.load_vehicles()
        print("\n=== CREATE VEHICLE ===")

        # Vehicle Number
        while True:
            vnum = input("Enter vehicle number (e.g., MH12AB1234): ").strip().upper()
            if not self.validate_vehicle_number(vnum):
                print("Invalid format! Must match 'MH12AB1234'. Try again.")
            elif any(v.get("vehicle_number","") == vnum for v in vehicles):
                print("This vehicle number already exists! Try again.")
            else:
                break

        # Engine Number
        while True:
            eng = input("Enter engine number (13 chars, e.g., A123BCDE56789): ").strip().upper()
            if not self.validate_engine_number(eng):
                print("Invalid engine number! Must be 13 chars. Try again.")
            else:
                break

        # Chassis Number
        while True:
            ch = input("Enter chassis number (17 chars VIN, e.g., 1HGCM82633A004352): ").strip().upper()
            if not self.validate_chassis_number(ch):
                print("Invalid chassis number! Must be 17 chars VIN. Try again.")
            else:
                break

        # Manager Assignment
        managers = self.um.list_managers()
        if managers:
            print("\nAvailable Managers:")
            for m in managers:
                print(f"{m['user_id']}: {m['name']}")
            while True:
                manager_id = input("Enter Manager ID: ").strip()
                manager = self.um.get_user_by_id(manager_id, "manager")
                if manager:
                    manager_name = manager["name"]
                    break
                else:
                    print("User not found. Try again.")
        else:
            print("No managers found in users.json!")
            manager_name = "Not Assigned"

        # Driver Assignment
        drivers = self.um.list_drivers()
        if drivers:
            print("\nAvailable Drivers:")
            for d in drivers:
                print(f"{d['user_id']}: {d['name']}")
            while True:
                driver_id = input("Enter Driver ID to assign (blank for 'Not Assigned'): ").strip()
                if driver_id == "":
                    driver_name, driver_id_selected = "Not Assigned", None
                    break
                driver = self.um.get_user_by_id(driver_id, "driver")
                if driver:
                    driver_name, driver_id_selected = driver["name"], driver["user_id"]
                    break
                else:
                    print("Invalid Driver ID! Try again.")
        else:
            driver_name, driver_id_selected = "Not Assigned", None

        # Model
        model = "TATA Prima E.28K"

        # Create new vehicle
        new_vehicle = {
            "vehicle_id": self.generate_vehicle_id(vehicles),
            "vehicle_number": vnum,
            "engine_number": eng,
            "chassis_number": ch,
            "manager_name": manager_name,
            "driver_assigned": driver_name,
            "driver_id": driver_id_selected,
            "model": model
        }

        vehicles.append(new_vehicle)
        self.save_vehicles(vehicles)
        print(f"\nVehicle created successfully with ID: {new_vehicle['vehicle_id']}")

    # -----------------------------
    # Update Vehicle
    # -----------------------------
    def update_vehicle(self):
        vehicles = self.load_vehicles()
        if not vehicles:
            print("No vehicles found!")
            return

        vid = input("Enter Vehicle ID to update: ").strip().upper()
        found = next((v for v in vehicles if v.get("vehicle_id", "").upper() == vid), None)
        if not found:
            print("Vehicle not found!")
            return

        print("\nOnly Manager Name and Driver Assigned can be updated.\n")

        # Manager update
        managers = self.um.list_managers()
        if managers:
            print("\nAvailable Managers:")
            for m in managers:
                print(f"{m['user_id']}: {m['name']}")
            while True:
                manager_id = input(f"Enter new Manager ID (current: {found.get('manager_name','-')}) or blank to skip: ").strip()
                if manager_id == "":
                    break
                manager = self.um.get_user_by_id(manager_id, "manager")
                if manager:
                    found["manager_name"] = manager["name"]
                    break
                else:
                    print("User not found! Try again.")

        # Driver update
        drivers = self.um.list_drivers()
        if drivers:
            print("\nAvailable Drivers:")
            for d in drivers:
                print(f"{d['user_id']}: {d['name']}")
            while True:
                driver_id = input(f"Enter new Driver ID (current: {found.get('driver_assigned','Not Assigned')}) or blank to skip: ").strip()
                if driver_id == "":
                    break
                driver = self.um.get_user_by_id(driver_id, "driver")
                if driver:
                    found["driver_assigned"] = driver["name"]
                    found["driver_id"] = driver["user_id"]
                    break
                else:
                    print("Invalid Driver ID! Try again.")

        self.save_vehicles(vehicles)
        print(f"Vehicle {vid} updated successfully!")

    # -----------------------------
    # Delete Vehicle
    # -----------------------------
    def delete_vehicle(self):
        vehicles = self.load_vehicles()
        if not vehicles:
            print("No vehicles to delete.")
            return

        vid = input("Enter Vehicle ID to delete: ").strip().upper()
        found = next((v for v in vehicles if v.get("vehicle_id", "").upper() == vid), None)
        if not found:
            print("Vehicle not found!")
            return

        confirm = input(f"Are you sure you want to delete {vid}? (yes/no): ").strip().lower()
        if confirm == "yes":
            vehicles.remove(found)
            self.save_vehicles(vehicles)
            print(f"Vehicle {vid} deleted successfully!")
        else:
            print("Delete cancelled.")

    # -----------------------------
    # Get Vehicle by ID
    # -----------------------------
    def get_vehicle_by_id(self):
        vehicles = self.load_vehicles()
        if not vehicles:
            print("No vehicles found.")
            return

        vid = input("Enter Vehicle ID to view details: ").strip().upper()
        found = next((v for v in vehicles if v.get("vehicle_id", "").upper() == vid), None)
        if found:
            print("\n=== Vehicle Details ===")
            print(f"Vehicle ID       : {found.get('vehicle_id','-')}")
            print(f"Vehicle Number   : {found.get('vehicle_number','-')}")
            print(f"Engine Number    : {found.get('engine_number','-')}")
            print(f"Chassis Number   : {found.get('chassis_number','-')}")
            print(f"Manager Name     : {found.get('manager_name','-')}")
            print(f"Driver Assigned  : {found.get('driver_assigned','Not Assigned')}")
            print(f"Model            : {found.get('model','TATA Prima E.28K')}")
        else:
            print("Vehicle not found!")

    # -----------------------------
    # View All Vehicles
    # -----------------------------
    def get_vehicle_list(self):
        vehicles = self.load_vehicles()
        if not vehicles:
            print("No vehicles found.")
            return

        print("\nVehicle List:")
        print("-" * 100)
        print(f"{'ID':<12} {'Number':<15} {'Engine No':<15} {'Chassis No':<20} {'Manager':<15} {'Driver':<15}")
        print("-" * 100)
        for v in vehicles:
            print(f"{v.get('vehicle_id','-'):<12} "
                  f"{v.get('vehicle_number','-'):<15} "
                  f"{v.get('engine_number','-'):<15} "
                  f"{v.get('chassis_number','-'):<20} "
                  f"{v.get('manager_name','-'):<15} "
                  f"{v.get('driver_assigned','Not Assigned'):<15}")
        print("-" * 100)
        print(f"Total Vehicles: {len(vehicles)}")

    # -----------------------------
    # Menu
    # -----------------------------
    def run(self):
        while True:
            print("\n=== VEHICLE MANAGEMENT MENU ===")
            print("1. Create Vehicle")
            print("2. Update Vehicle (Manager/Driver only)")
            print("3. Delete Vehicle")
            print("4. View Vehicle List")
            print("5. Get Vehicle by ID")
            print("6. Exit")

            choice = input("Enter your choice: ").strip()
            if choice == "1":
                self.create_vehicle()
            elif choice == "2":
                self.update_vehicle()
            elif choice == "3":
                self.delete_vehicle()
            elif choice == "4":
                self.get_vehicle_list()
            elif choice == "5":
                self.get_vehicle_by_id()
            elif choice == "6":
                print("Exiting... Goodbye!")
                break
            else:
                print("Invalid choice! Try again.")

# -----------------------------
# Run Application
# -----------------------------
if __name__ == "__main__":
    VehicleManagement().run()

