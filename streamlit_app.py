import streamlit as st
import mysql.connector
import pandas as pd

st.set_page_config(page_title="Blood Bank System", page_icon="🩸", layout="wide")

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="sunny",
    database="test_bloodbank"
)

cursor = conn.cursor()

st.title("🩸 Blood Bank Management System")
st.markdown("Manage donors and blood inventory efficiently")

menu = ["Dashboard", "View Donors", "Add Donor", "Search Donor", "Blood Inventory"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Dashboard":
    st.subheader("📊 Dashboard")

    cursor.execute("SELECT COUNT(*) FROM Donor")
    total_donors = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM BloodUnit WHERE status='Available'")
    available_units = cursor.fetchone()[0]

    col1, col2 = st.columns(2)
    col1.metric("Total Donors", total_donors)
    col2.metric("Available Blood Units", available_units)

elif choice == "View Donors":
    st.subheader("👨‍⚕️ All Donors")

    cursor.execute("SELECT * FROM Donor")
    data = cursor.fetchall()

    df = pd.DataFrame(data, columns=[
        "ID", "Name", "DOB", "Gender", "Blood Group", "Phone", "Email"
    ])

    st.metric("Total Donors", len(df))
    st.dataframe(df, use_container_width=True)

elif choice == "Add Donor":
    st.subheader("➕ Add New Donor")

    name = st.text_input("Full Name")
    dob = st.text_input("Date of Birth (YYYY-MM-DD)")
    gender = st.selectbox("Gender", ["Male", "Female", "Others"])
    bloodgroup = st.selectbox("Blood Group", ["A+","A-","B+","B-","O+","O-","AB+","AB-"])
    phone = st.text_input("Phone Number")
    email = st.text_input("Email")

    if st.button("Add Donor"):
        if not name or not dob or not phone or not email:
            st.error("❌ Fill all fields")
        else:
            query = """
            INSERT INTO Donor 
            (full_name, date_of_birth, gender, bloodgroup, phone_number, email)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (name, dob, gender, bloodgroup, phone, email))
            conn.commit()
            st.success("✅ Donor added successfully")

elif choice == "Search Donor":
    st.subheader("🔍 Search Donor")

    bg = st.selectbox("Blood Group", ["A+","A-","B+","B-","O+","O-","AB+","AB-"])

    if st.button("Search"):
        cursor.execute("SELECT * FROM Donor WHERE bloodgroup=%s", (bg,))
        results = cursor.fetchall()

        if results:
            df = pd.DataFrame(results, columns=[
                "ID", "Name", "DOB", "Gender", "Blood Group", "Phone", "Email"
            ])
            st.dataframe(df)
        else:
            st.warning("No donors found")

elif choice == "Blood Inventory":
    st.subheader("🩸 Blood Inventory")

    query = """
    SELECT dr.bloodgroup, COUNT(*)
    FROM BloodUnit bu
    JOIN Donation d ON bu.donation_id = d.donation_id
    JOIN Donor dr ON d.donor_id = dr.donor_id
    WHERE bu.status='Available'
    GROUP BY dr.bloodgroup
    """

    cursor.execute(query)
    data = cursor.fetchall()

    if data:
        df = pd.DataFrame(data, columns=["Blood Group", "Units"])
        st.dataframe(df)
        st.bar_chart(df.set_index("Blood Group"))
    else:
        st.warning("No data")

st.markdown("---")
st.caption("Built by Sunny Yadav")