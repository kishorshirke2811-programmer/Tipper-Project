import json
import os
from datetime import datetime

class MaintenanceManager:
    VEHICLE_FILE = "vehicles.json"

    def __init__(self, file_path='maintenance_data.json'):
        self.file_path = file_path
        self.data = self.load_data()
        self.vehicles = self.load_vehicles()

    # Load maintenance data
    def load_data(self):
        if not os.path.exists(self.file_path):
            return []
        with open(self.file_path, 'r') as file:
            return json.load(file)

    # Save maintenance data
    def save_data(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.data, file, indent=4)

    # Load vehicles data
    def load_vehicles(self):
        if not os.path.exists(self.VEHICLE_FILE):
            return []
        with open(self.VEHICLE_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []

    # Check if vehicle ID exists
    def is_valid_vehicle(self, vehicle_id):
        for v in self.vehicles:
            if v.get("vehicle_id", "").upper() == vehicle_id.upper():
                return True
        return False

    # Create maintenance record
    def create_maintenance(self):
        # Auto-generate Maintenance ID
        if self.data:
            last_id = max([int(record["maintenance_id"].replace("MNT", "")) for record in self.data])
            maintenance_id = f"MNT{last_id + 1:03d}"
        else:
            maintenance_id = "MNT001"

        print(f"\nGenerated Maintenance ID: {maintenance_id}")

        # Vehicle ID validation
        while True:
            vehicle_id = input("Enter Vehicle ID: ").strip()
            if self.is_valid_vehicle(vehicle_id):
                break
            else:
                print("Vehicle ID not found in vehicles.json. Please enter a valid Vehicle ID.")

        maintenance_type = input("Enter Maintenance Type (regular/docker): ").lower()
        if maintenance_type not in ['regular', 'docker']:
            print("Invalid maintenance type.")
            return

        last_date = input("Enter Last Maintenance Date (YYYY-MM-DD): ").strip()

        maintenance_status = input("Enter Maintenance Status (ok/not ok): ").lower()
        if maintenance_status not in ['ok', 'not ok']:
            print("Invalid maintenance status.")
            return

        # Only ask for problem description if status is 'not ok'
        problem_description = ""
        if maintenance_status == "not ok":
            problem_description = input("Enter problem description: ").strip()

        new_record = {
            "maintenance_id": maintenance_id,
            "vehicle_id": vehicle_id,
            "maintenance_type": maintenance_type,
            "last_date_of_maintenance": last_date,
            "maintenance_status": maintenance_status,
            "problem_description": problem_description
        }

        self.data.append(new_record)
        self.save_data()
        print("Maintenance record created successfully.")

    # Get maintenance details by ID
    def get_maintenance_details(self):
        maintenance_id = input("Enter Maintenance ID to search: ").strip()
        found = False
        for record in self.data:
            if record["maintenance_id"] == maintenance_id:
                print("\nMaintenance Record Found:")
                print(f"  Maintenance ID       : {record['maintenance_id']}")
                print(f"  Vehicle ID           : {record['vehicle_id']}")
                print(f"  Maintenance Type     : {record['maintenance_type']}")
                print(f"  Last Maintenance Date: {record['last_date_of_maintenance']}")
                print(f"  Maintenance Status   : {record['maintenance_status']}")
                print(f"  Problem Description  : {record.get('problem_description', 'N/A')}")
                found = True
                break
        if not found:
            print("Maintenance record not found.")

    # Get all maintenance records
    def get_maintenance_list(self):
        if not self.data:
            print("No maintenance records found.")
            return
        print("\nAll Maintenance Records:")
        for record in self.data:
            print(json.dumps(record, indent=4))

    # Update maintenance record
    def update_maintenance(self):
        maintenance_id = input("Enter Maintenance ID to update: ").strip()
        for record in self.data:
            if record["maintenance_id"] == maintenance_id:
                print("Leave blank to keep current value.")

                new_type = input(f"New Maintenance Type (current: {record['maintenance_type']}): ").lower().strip()
                new_date = input(f"New Last Maintenance Date (current: {record['last_date_of_maintenance']}): ").strip()
                new_status = input(f"New Status (current: {record['maintenance_status']}): ").lower().strip()

                if new_type in ['regular', 'docker']:
                    record['maintenance_type'] = new_type
                if new_date:
                    record['last_date_of_maintenance'] = new_date
                if new_status in ['ok', 'not ok']:
                    record['maintenance_status'] = new_status
                    # Problem description only if status is 'not ok'
                    if new_status == "not ok":
                        record['problem_description'] = input("Enter problem description: ").strip()
                    elif new_status == "ok":
                        record['problem_description'] = ""  # clear previous description

                self.save_data()
                print("Maintenance record updated.")
                return
        print("Maintenance ID not found.")

    # Delete maintenance record
    def delete_maintenance(self):
        maintenance_id = input("Enter Maintenance ID to delete: ").strip()
        original_len = len(self.data)
        self.data = [r for r in self.data if r['maintenance_id'] != maintenance_id]
        if len(self.data) < original_len:
            self.save_data()
            print("Record deleted.")
        else:
            print("Maintenance ID not found.")


# Main program
if __name__ == "__main__":
    manager = MaintenanceManager()
    while True:
        print("\nMaintenance Management Menu:")
        print("1. Create Maintenance")  
        print("2. Get Maintenance Details")  
        print("3. Get Maintenance List")
        print("4. Update Maintenance")
        print("5. Delete Maintenance")
        print("6. Exit")

        choice = input("Enter your choice: ").strip()
        if choice == '1':
            manager.create_maintenance()
        elif choice == '2':
            manager.get_maintenance_details()
        elif choice == '3':
            manager.get_maintenance_list()
        elif choice == '4':
            manager.update_maintenance()
        elif choice == '5':
            manager.delete_maintenance()
        elif choice == '6':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")

