"""Command-line interface for the Blood Bank Management System."""

from datetime import date

from dotenv import load_dotenv
from mysql.connector import IntegrityError, Error

from db import DatabaseManager, validate_phone, validate_email, validate_age

load_dotenv()

db = DatabaseManager()


def main():
    while True:
        print("\n===== Blood Bank System =====")
        print("1. View all donors")
        print("2. Add new donor")
        print("3. Search by blood group")
        print("4. Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            try:
                for row in db.get_all_donors():
                    print(row)
            except Error as e:
                print(f"Error: {e}")

        elif choice == "2":
            name = input("Enter name: ").strip()
            dob_str = input("Enter DOB (YYYY-MM-DD): ").strip()
            gender = input("Enter gender (Male/Female/Others): ").strip()
            blood_group = input("Enter blood group: ").strip()
            phone = input("Enter phone: ").strip()
            email = input("Enter email: ").strip()

            errors = []
            dob = None
            try:
                dob = date.fromisoformat(dob_str)
            except ValueError:
                errors.append("Invalid date format. Use YYYY-MM-DD.")

            if len(name) < 2:
                errors.append("Name must be at least 2 characters.")
            if dob and not validate_age(dob):
                errors.append("Donor must be at least 18 years old.")
            if not validate_phone(phone):
                errors.append("Phone must be 10-15 digits.")
            if not validate_email(email):
                errors.append("Invalid email address.")

            if errors:
                for err in errors:
                    print(f"  \u2717 {err}")
            else:
                try:
                    db.add_donor(name, dob_str, gender, blood_group, phone, email)
                    print("Donor added successfully!")
                except IntegrityError:
                    print("Error: A donor with this phone or email already exists.")
                except Error as e:
                    print(f"Error: {e}")

        elif choice == "3":
            bg = input("Enter blood group: ").strip()
            try:
                results = db.get_donors_by_blood_group(bg)
                if results:
                    for row in results:
                        print(row)
                else:
                    print("No donors found for this blood group.")
            except Error as e:
                print(f"Error: {e}")

        elif choice == "4":
            print("Exiting program...")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()