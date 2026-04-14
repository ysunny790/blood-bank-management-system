import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="sunny",
    database="test_bloodbank"
)

cursor = conn.cursor()

while True:
    print("\n===== Blood Bank System =====")
    print("1. View all donors")
    print("2. Add new donor")
    print("3. Search by blood group")
    print("4. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        cursor.execute("SELECT * FROM Donor")
        for row in cursor.fetchall():
            print(row)

    elif choice == "2":
        name = input("Enter name: ")
        dob = input("Enter DOB (YYYY-MM-DD): ")
        gender = input("Enter gender (Male/Female/Others): ")
        bloodgroup = input("Enter blood group: ")
        phone = input("Enter phone: ")
        email = input("Enter email: ")

        query = """
        INSERT INTO Donor (full_name, date_of_birth, gender, bloodgroup, phone_number, email)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        cursor.execute(query, (name, dob, gender, bloodgroup, phone, email))
        conn.commit()

        print("Donor added successfully!")

    elif choice == "3":
        bg = input("Enter blood group: ")
        query = "SELECT * FROM Donor WHERE bloodgroup = %s"
        cursor.execute(query, (bg,))
        
        results = cursor.fetchall()

        if results:
            for row in results:
                print(row)
        else:
            print("No donors found for this blood group.")

    elif choice == "4":
        print("Exiting program...")
        break

    else:
        print("Invalid choice. Try again.")

conn.close()