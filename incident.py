import json
import random
from datetime import datetime, timedelta

class Insurance:
    FILE = "insurance.json"

    def __init__(self):
        # Load insurance records
        try:
            with open(self.FILE, "r") as f:
                self.records = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.records = []

    def save_data(self):
        with open(self.FILE, "w") as f:
            json.dump(self.records, f, indent=4, default=str)

    # -------------------
    # CREATE INSURANCE
    # -------------------
    def create_insurance(self):
        print("\n--- CREATE INSURANCE ---")

        # Load vehicles
        try:
            with open("vehicles.json", "r") as f:
                vehicles = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            vehicles = []

        vehicle_ids = [v.get("vehicle_id") for v in vehicles]

        if not vehicle_ids:
            print("No vehicles found in vehicles.json! Cannot create insurance.")
            return

        # Vehicle ID input with validation
        while True:
            vehicle_id = input("Enter Vehicle ID: ").strip()
            if vehicle_id in vehicle_ids:
                break
            else:
                print("\nInvalid Vehicle ID!")
                print("Available Vehicle IDs:")
                for vid in vehicle_ids:
                    print(f"  - {vid}")
                print("Please enter a valid Vehicle ID.\n")

        # Insurance type
        print("\nChoose Insurance Type:")
        print("1. Third Party")
        print("2. Comprehensive")
        print("3. Zero Depreciation")
        while True:
            choice = input("Enter your choice (1/2/3): ").strip()
            if choice == "1":
                insurance_type = "Third Party"
                break
            elif choice == "2":
                insurance_type = "Comprehensive"
                break
            elif choice == "3":
                insurance_type = "Zero Depreciation"
                break
            else:
                print("Invalid choice! Please enter 1, 2, or 3.")

        # Issue Date
        while True:
            issue_date_input = input("Enter Issue Date (YYYY-MM-DD): ").strip()
            try:
                issue_date = datetime.strptime(issue_date_input, "%Y-%m-%d")
                break
            except ValueError as e:
                print(f"Invalid date: {e}. Please enter a valid date (YYYY-MM-DD).")

        # Expiry date exactly 1 year
        expiry_date = issue_date + timedelta(days=365)

        # Insurance ID: 11-digit numeric
        insurance_id = str(random.randint(10000000000, 99999999999))

        record = {
            "Insurance ID": insurance_id,
            "Vehicle ID": vehicle_id,
            "Insurance Type": insurance_type,
            "Issue Date": issue_date.strftime("%Y-%m-%d"),
            "Expiry Date": expiry_date.strftime("%Y-%m-%d"),
            "Status": "ACTIVE"
        }

        self.records.append(record)
        self.save_data()

        print("\nInsurance Created Successfully!")
        print("Insurance ID:", insurance_id)
        print("Expiry Date:", expiry_date.strftime("%Y-%m-%d"))

    # -------------------
    # UPDATE INSURANCE (Issue Date only)
    # -------------------
    def update_insurance(self):
        print("\n--- UPDATE INSURANCE ---")
        insurance_id = input("Enter Insurance ID to update: ").strip()
        matched = next((r for r in self.records if r["Insurance ID"] == insurance_id), None)

        if not matched:
            print("Invalid Insurance ID.")
            return

        print("\nYou can update only the Issue Date of this insurance.")
        while True:
            new_issue = input("Enter New Issue Date (YYYY-MM-DD): ").strip()
            try:
                issue_date = datetime.strptime(new_issue, "%Y-%m-%d")
                break
            except ValueError as e:
                print(f"Invalid date: {e}. Please enter a valid date (YYYY-MM-DD).")

        # Expiry exactly 1 year
        expiry_date = issue_date + timedelta(days=365)
        matched["Issue Date"] = new_issue
        matched["Expiry Date"] = expiry_date.strftime("%Y-%m-%d")
        matched["Status"] = "ACTIVE"

        self.save_data()
        print("\nIssue and Expiry Dates Updated Successfully!")
        print(f"New Expiry Date: {expiry_date.strftime('%Y-%m-%d')}")

    # -------------------
    # CHECK INSURANCE STATUS
    # -------------------
    def insurance_status(self):
        print("\n--- CHECK INSURANCE STATUS ---")
        vehicle_id = input("Enter Vehicle ID: ").strip()
        found = False
        for rec in self.records:
            if rec["Vehicle ID"] == vehicle_id:
                found = True
                expiry_date = datetime.strptime(rec["Expiry Date"], "%Y-%m-%d")
                today = datetime.today()
                rec["Status"] = "ACTIVE" if expiry_date >= today else "INACTIVE"
                print(f"Vehicle ID: {vehicle_id} | Insurance Status: {rec['Status']}")
                self.save_data()
                return
        if not found:
            print(f"No insurance found for Vehicle ID: {vehicle_id}. Status: INACTIVE")

# -------------------
# EXTENDED CLASS FOR GET
# -------------------
class InsuranceGetter(Insurance):
    def get_insurance(self):
        print("\n--- GET INSURANCE BY ID ---")
        insurance_id = input("Enter Insurance ID: ").strip()
        rec = next((r for r in self.records if r["Insurance ID"] == insurance_id), None)
        if rec:
            print(json.dumps(rec, indent=4))
        else:
            print("No record found with this Insurance ID.")

    def get_insurance_list(self):
        print("\n--- GET INSURANCE LIST ---")
        if not self.records:
            print("No records found.")
            return
        print(f"Total {len(self.records)} records:")
        for rec in self.records:
            print(json.dumps(rec, indent=4))

# -------------------
# MAIN MENU
# -------------------
if __name__ == "__main__":
    system = InsuranceGetter()

    while True:
        print("\n--- INSURANCE SYSTEM MENU ---")
        print("1. Create Insurance")
        print("2. Update Insurance (Issue Date Only)")
        print("3. Check Insurance Status")
        print("4. Get Insurance by ID")
        print("5. Get Insurance List")
        print("6. Exit")

        choice = input("Enter your choice: ").strip()
        if choice == "1":
            system.create_insurance()
        elif choice == "2":
            system.update_insurance()
        elif choice == "3":
            system.insurance_status()
        elif choice == "4":
            system.get_insurance()
        elif choice == "5":
            system.get_insurance_list()
        elif choice == "6":
            print("Exiting program... Goodbye!")
            break
        else:
            print("Invalid choice, Try again.")

