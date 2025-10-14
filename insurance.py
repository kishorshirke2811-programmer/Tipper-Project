from create_update import Insurance   # Import class from Part 1


class InsuranceGetter(Insurance):
    # --- GET INSURANCE BY ID ---
    def get_insurance(self):
        print("\n----- GET INSURANCE -----")
        insurance_id = input("Enter Insurance ID to get insurance details: ")

        for record in self.records:
            if record["Insurance ID"] == insurance_id:
                print(f"Insurance ID: {record['Insurance ID']}")
                print(f"Vehicle ID: {record['Vehicle ID']}")
                print(f"Insurance Type: {record['Insurance Type']}")
                print(f"Expiry Date: {record['Expiry Date']}")
                print(f"Issue Date: {record['Issue Date']}")
                print(f"Status: {record['Status']}")
                return
        print("No record found with this Insurance ID.")

    # --- GET INSURANCE LIST ---
    def get_insurance_list(self):
        print("\n----- GET INSURANCE LIST -----")
        if not self.records:
            print("No records found.")
            return
        print(f"Total {len(self.records)} records found.")
        for rec in self.records:
            print(f"{rec['Insurance ID']} | {rec['Vehicle ID']} | {rec['Insurance Type']} | "
                  f"{rec['Expiry Date']} | {rec['Issue Date']} | {rec['Status']}")


# Run Part 2 separately
if __name__ == "__main__":
    system = InsuranceGetter()
    while True:
        print("\n--- GET MENU ---")
        print("1. Get Insurance by ID")
        print("2. Get Insurance List")
        print("3. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            system.get_insurance()
        elif choice == "2":
            system.get_insurance_list()
        elif choice == "3":
            break
        else:
            print("Invalid choice!")

