import json
import random
import time
from datetime import datetime, timedelta


class InsuranceSystem:
    FILE = "insurance.json"

    def __init__(self):
        try:
            with open(self.FILE, "r") as f:
                self.records = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.records = []

    # -------------------
    # SAVE DATA
    # -------------------
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

        # Expiry date exactly 1 year later
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

        print("\n Insurance Created Successfully!")
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

        # Expiry exactly 1 year later
        expiry_date = issue_date + timedelta(days=365)
        matched["Issue Date"] = new_issue
        matched["Expiry Date"] = expiry_date.strftime("%Y-%m-%d")
        matched["Status"] = "ACTIVE"

        self.save_data()
        print("\n Issue and Expiry Dates Updated Successfully!")
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
    # GET INSURANCE BY ID
    # -------------------
    def get_insurance(self):
        print("\n--- GET INSURANCE BY ID ---")
        insurance_id = input("Enter Insurance ID: ").strip()
        rec = next((r for r in self.records if r["Insurance ID"] == insurance_id), None)
        if rec:
            print(json.dumps(rec, indent=4))
        else:
            print("No record found with this Insurance ID.")

    # -------------------
    # GET INSURANCE LIST
    # -------------------
    def get_insurance_list(self):
        print("\n--- GET INSURANCE LIST ---")
        if not self.records:
            print("No records found.")
            return
        print(f"Total {len(self.records)} records:")
        for rec in self.records:
            print(json.dumps(rec, indent=4))

    # -------------------
    # AUTO CLEANER: DELETE INACTIVE INSURANCE
    # -------------------
    def check_and_delete_inactive(self):
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Checking insurance status...")

        active_records = []
        deleted_count = 0

        for record in self.records:
            expiry_date = datetime.strptime(record["Expiry Date"], "%Y-%m-%d")
            today = datetime.today()

            if expiry_date >= today:
                record["Status"] = "ACTIVE"
                active_records.append(record)
            else:
                record["Status"] = "INACTIVE"
                deleted_count += 1
                print(f" Deleted INACTIVE insurance: {record['Insurance ID']} (Vehicle: {record['Vehicle ID']})")

        self.records = active_records
        self.save_data()
        print(f" Cleanup completed — {deleted_count} inactive insurances removed.\n")

    # -------------------
    # RUN CLEANUP DAILY AT MIDNIGHT
    # -------------------
    def run_daily_at_midnight(self):
        print("Insurance auto-cleaner started. It will check every minute and run cleanup at midnight (00:00).")
        while True:
            current_time = datetime.now().strftime("%H:%M")
            if current_time == "00:00":
                self.check_and_delete_inactive()
                time.sleep(61)  # Avoid double runs
            else:
                time.sleep(60)


# -------------------
# MAIN MENU
# -------------------
if __name__ == "__main__":
    system = InsuranceSystem()

    while True:
        print("\n--- INSURANCE SYSTEM MENU ---")
        print("1. Create Insurance")
        print("2. Update Insurance (Issue Date Only)")
        print("3. Check Insurance Status")
        print("4. Get Insurance by ID")
        print("5. Get Insurance List")
        print("6. Run Cleanup Now")
        print("7. Start Auto-Cleanup at Midnight")
        print("8. Exit")

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
            system.check_and_delete_inactive()
        elif choice == "7":
            system.run_daily_at_midnight()
        elif choice == "8":
            print("Exiting program... Goodbye!")
            break
        else:
            print("Invalid choice, Try again.")
