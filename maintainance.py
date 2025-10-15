import json
import os
from datetime import datetime
class MaintenanceManager:
 def init(self, file_path='maintenance_data.json'):
   self.file_path = file_path
   self.data = self.load_data()
# Step 3.1: Load data from JSON
 def load_data(self):
    if not os.path.exists(self.file_path):
        return []
    with open(self.file_path, 'r') as file:
        return json.load(file)

# Step 3.2: Save data to JSON
 def save_data(self):
    with open(self.file_path, 'w') as file:
        json.dump(self.data, file, indent=4)

# Step 3.3: Create maintenance record
 def create_maintenance(self):
    maintenance_id = input("Enter Maintenance ID: ")
    for record in self.data:
        if record['maintenance_id'] == maintenance_id:
            print(" Maintenance ID already exists.")
            return

    vehicle_id = input("Enter Vehicle ID: ")
    maintenance_type = input("Enter Maintenance Type (regular/docker): ").lower()
    if maintenance_type not in ['regular', 'docker']:
        print(" Invalid maintenance type.")
        return

    last_date = input("Enter Last Maintenance Date (YYYY-MM-DD): ")
    maintenance_status = input("Enter Maintenance Status (ok/not ok): ").lower()
    if maintenance_status not in ['ok', 'not ok']:
        print(" Invalid maintenance status.")
        return

    new_record = {
        "maintenance_id": maintenance_id,
        "vehicle_id": vehicle_id,
        "maintenance_type": maintenance_type,
        "last_date_of_maintenance": last_date,
        "maintenance_status": maintenance_status
    }

    self.data.append(new_record)
    self.save_data()
    print(" Maintenance record created successfully.")

# Step 3.4: Get maintenance details by ID
 def get_maintenance_details(self):
    maintenance_id = input("Enter Maintenance ID to search: ")
    found = False
    for record in self.data:
        if record["maintenance_id"] == maintenance_id:
            print("\n Maintenance Record Found:")
            print(f"  Maintenance ID       : {record['maintenance_id']}")
            print(f"  Vehicle ID           : {record['vehicle_id']}")
            print(f"  Maintenance Type     : {record['maintenance_type']}")
            print(f"  Last Maintenance Date: {record['last_date_of_maintenance']}")
            print(f"  Maintenance Status   : {record['maintenance_status']}")
            found = True
            break
    if not found:
        print(" Maintenance record not found.")

# Step 3.5: Get all maintenance list
 def get_maintenance_list(self):
    if not self.data:
        print(" No maintenance records found.")
        return
    print("\n All Maintenance Records:")
    for record in self.data:
        print(json.dumps(record, indent=4))

# Step 3.6: Update maintenance
 def update_maintenance(self):
    maintenance_id = input("Enter Maintenance ID to update: ")
    for record in self.data:
        if record["maintenance_id"] == maintenance_id:
            print("Leave blank to keep current value.")

            new_type = input(f"New Maintenance Type (current: {record['maintenance_type']}): ").lower()
            new_date = input(f"New Last Maintenance Date (current: {record['last_date_of_maintenance']}): ")
            new_status = input(f"New Status (current: {record['maintenance_status']}): ").lower()

            if new_type in ['regular', 'docker']:
                record['maintenance_type'] = new_type
            if new_date:
                record['last_date_of_maintenance'] = new_date
            if new_status in ['ok', 'not ok']:
                record['maintenance_status'] = new_status

            self.save_data()
            print("Maintenance record updated.")
            return
    print(" Maintenance ID not found.")

# Step 3.7: Delete maintenance
 def delete_maintenance(self):
    maintenance_id = input("Enter Maintenance ID to delete: ")
    original_len = len(self.data)
    self.data = [r for r in self.data if r['maintenance_id'] != maintenance_id]
    if len(self.data) < original_len:
        self.save_data()
        print(" Record deleted.")
    else:
        print(" Maintenance ID not found.")

if __name__ == "__main__":
    manager = MaintenanceManager()
    manager.init()  
    while True:
        print("\n Maintenance Management Menu:")
        print("1. Create Maintenance")  
        print("2. Get Maintenance Details")  
        print("3. Get Maintenance List")
        print("4. Update Maintenance")
        print("5. Delete Maintenance")
        print("6. Exit")

        choice = input("Enter your choice: ")
        if choice == '1':
            manager.create_maintenance()
        elif choice == '2':
            manager.get_maintenance_details()
        elif choice == '3':
            manager.get_maintenance_list
        elif choice == '4':
            manager.update_maintenance()
        elif choice == '5':
            manager.delete_maintenance()
        elif choice == '6':
            print("Exiting the program.")
            break
        else:
            print(" Invalid choice. Please try again.")

