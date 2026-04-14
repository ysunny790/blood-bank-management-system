import streamlit as st
import mysql.connector
import pandas as pd

# ------------------------------
# Page Config
# ------------------------------
st.set_page_config(
    page_title="Blood Bank System",
    page_icon="🩸",
    layout="wide"
)

# ------------------------------
# Database Connection
# ------------------------------
@st.cache_resource
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="sunny",  # CHANGE THIS
        database="test_bloodbank"
    )

conn = get_connection()
cursor = conn.cursor()

# ------------------------------
# Title
# ------------------------------
st.title("🩸 Blood Bank Management System")
st.markdown("Manage donors, blood inventory and requests efficiently")

# ------------------------------
# Sidebar Menu
# ------------------------------
menu = [
    "Dashboard",
    "View Donors",
    "Add Donor",
    "Search Donor",
    "Blood Inventory"
]

choice = st.sidebar.selectbox("Menu", menu)

# ------------------------------
# DASHBOARD
# ------------------------------
if choice == "Dashboard":
    st.subheader("📊 Dashboard")

    cursor.execute("SELECT COUNT(*) FROM Donor")
    total_donors = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM BloodUnit WHERE status='Available'")
    available_units = cursor.fetchone()[0]

    col1, col2 = st.columns(2)

    col1.metric("Total Donors", total_donors)
    col2.metric("Available Blood Units", available_units)

# ------------------------------
# VIEW DONORS
# ------------------------------
elif choice == "View Donors":
    st.subheader("👨‍⚕️ All Donors")

    cursor.execute("SELECT * FROM Donor")
    data = cursor.fetchall()

    df = pd.DataFrame(data, columns=[
        "ID", "Name", "DOB", "Gender", "Blood Group", "Phone", "Email"
    ])

    st.metric("Total Donors", len(df))
    st.dataframe(df, use_container_width=True)

# ------------------------------
# ADD DONOR
# ------------------------------
elif choice == "Add Donor":
    st.subheader("➕ Add New Donor")

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Full Name")
        dob = st.text_input("Date of Birth (YYYY-MM-DD)")
        gender = st.selectbox("Gender", ["Male", "Female", "Others"])

    with col2:
        bloodgroup = st.selectbox("Blood Group", ["A+","A-","B+","B-","O+","O-","AB+","AB-"])
        phone = st.text_input("Phone Number")
        email = st.text_input("Email")

    if st.button("Add Donor"):
        if not name or not dob or not phone or not email:
            st.error("❌ Please fill all required fields")
        else:
            try:
                query = """
                INSERT INTO Donor 
                (full_name, date_of_birth, gender, bloodgroup, phone_number, email)
                VALUES (%s, %s, %s, %s, %s, %s)
                """

                cursor.execute(query, (name, dob, gender, bloodgroup, phone, email))
                conn.commit()

                st.success("✅ Donor added successfully!")

            except Exception as e:
                st.error(f"Error: {e}")

# ------------------------------
# SEARCH DONOR
# ------------------------------
elif choice == "Search Donor":
    st.subheader("🔍 Search Donor by Blood Group")

    bg = st.selectbox("Select Blood Group", ["A+","A-","B+","B-","O+","O-","AB+","AB-"])

    if st.button("Search"):
        query = "SELECT * FROM Donor WHERE bloodgroup = %s"
        cursor.execute(query, (bg,))
        results = cursor.fetchall()

        if results:
            df = pd.DataFrame(results, columns=[
                "ID", "Name", "DOB", "Gender", "Blood Group", "Phone", "Email"
            ])
            st.success(f"Found {len(df)} donors")
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("No donors found")

# ------------------------------
# BLOOD INVENTORY (NEW FEATURE)
# ------------------------------
elif choice == "Blood Inventory":
    st.subheader("🩸 Blood Inventory")

    query = """
    SELECT dr.bloodgroup, COUNT(*) as total_units
    FROM BloodUnit bu
    JOIN Donation d ON bu.donation_id = d.donation_id
    JOIN Donor dr ON d.donor_id = dr.donor_id
    WHERE bu.status = 'Available'
    GROUP BY dr.bloodgroup
    """

    cursor.execute(query)
    data = cursor.fetchall()

    if data:
        df = pd.DataFrame(data, columns=["Blood Group", "Units Available"])

        st.dataframe(df, use_container_width=True)

        st.subheader("📊 Inventory Chart")
        st.bar_chart(df.set_index("Blood Group"))

    else:
        st.warning("No data available")

# ------------------------------
# FOOTER
# ------------------------------
st.markdown("---")
st.caption("Built by Sunny Yadav | Data Science & AI")