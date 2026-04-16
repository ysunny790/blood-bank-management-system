"""Streamlit web interface for the Blood Bank Management System."""

import streamlit as st
import pandas as pd
from datetime import date

from db import (
    DatabaseManager,
    BLOOD_GROUPS,
    GENDERS,
    REQUEST_STATUSES,
    validate_phone,
    validate_email,
    validate_age,
)
from mysql.connector import IntegrityError, Error

# ── Page config ───────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Blood Bank System",
    page_icon="🩸",
    layout="wide",
)

# ── DB instance (one per Streamlit server process) ────────────────────────────

@st.cache_resource
def get_db() -> DatabaseManager:
    return DatabaseManager()

db = get_db()

# ── Title ─────────────────────────────────────────────────────────────────────

st.title("🩸 Blood Bank Management System")
st.markdown("Manage donors, blood inventory and requests efficiently")

# ── Sidebar menu ──────────────────────────────────────────────────────────────

MENU = [
    "Dashboard",
    "View Donors",
    "Add Donor",
    "Edit Donor",
    "Delete Donor",
    "Search Donor",
    "Blood Inventory",
    "Blood Requests",
    "Hospitals & Patients",
]

choice = st.sidebar.selectbox("Menu", MENU)

PAGE_SIZE = 10
DONOR_COLS = ["ID", "Name", "DOB", "Gender", "Blood Group", "Phone", "Email", "Last Donation"]

# ──────────────────────────────────────────────────────────────────────────────
# DASHBOARD
# ──────────────────────────────────────────────────────────────────────────────

if choice == "Dashboard":
    st.subheader("📊 Dashboard")
    try:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Donors", db.get_total_donors())
        col2.metric("Available Blood Units", db.get_available_units())
        col3.metric("Pending Requests", db.get_pending_requests())
        col4.metric("⚠️ Expiring (7 days)", db.get_expiring_soon_count())
    except Error as e:
        st.error(f"Database error: {e}")

# ──────────────────────────────────────────────────────────────────────────────
# VIEW DONORS
# ──────────────────────────────────────────────────────────────────────────────

elif choice == "View Donors":
    st.subheader("👨‍⚕️ All Donors")
    try:
        rows = db.get_all_donors()
    except Error as e:
        st.error(f"Database error: {e}")
        rows = []

    if rows:
        total_pages = max(1, (len(rows) - 1) // PAGE_SIZE + 1)
        if "donor_page" not in st.session_state:
            st.session_state.donor_page = 0
        st.session_state.donor_page = min(st.session_state.donor_page, total_pages - 1)

        start = st.session_state.donor_page * PAGE_SIZE
        df = pd.DataFrame(rows[start : start + PAGE_SIZE], columns=DONOR_COLS)

        st.metric("Total Donors", len(rows))
        st.dataframe(df, use_container_width=True)

        nav1, nav2, nav3 = st.columns([1, 3, 1])
        with nav1:
            if st.button("← Prev", disabled=st.session_state.donor_page == 0):
                st.session_state.donor_page -= 1
                st.rerun()
        with nav2:
            st.write(f"Page {st.session_state.donor_page + 1} of {total_pages}")
        with nav3:
            if st.button("Next →", disabled=st.session_state.donor_page >= total_pages - 1):
                st.session_state.donor_page += 1
                st.rerun()
    else:
        st.info("No donors in the database yet.")

# ──────────────────────────────────────────────────────────────────────────────
# ADD DONOR
# ──────────────────────────────────────────────────────────────────────────────

elif choice == "Add Donor":
    st.subheader("➕ Add New Donor")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name")
        dob = st.date_input(
            "Date of Birth",
            value=date(1990, 1, 1),
            min_value=date(1900, 1, 1),
            max_value=date.today(),
        )
        gender = st.selectbox("Gender", GENDERS)
    with col2:
        blood_group = st.selectbox("Blood Group", BLOOD_GROUPS)
        phone = st.text_input("Phone Number (10–15 digits)")
        email = st.text_input("Email Address")

    if st.button("Add Donor"):
        errors = []
        name = name.strip()
        if len(name) < 2:
            errors.append("Name must be at least 2 characters.")
        if not validate_age(dob):
            errors.append("Donor must be at least 18 years old.")
        if not validate_phone(phone):
            errors.append("Phone must be 10–15 digits (optionally prefixed with +).")
        if not validate_email(email):
            errors.append("Please enter a valid email address.")

        if errors:
            for err in errors:
                st.error(f"❌ {err}")
        else:
            try:
                db.add_donor(name, dob.isoformat(), gender, blood_group, phone, email)
                st.success("✅ Donor added successfully!")
            except IntegrityError:
                st.error("❌ A donor with this phone or email already exists.")
            except Error as e:
                st.error(f"Database error: {e}")

# ──────────────────────────────────────────────────────────────────────────────
# EDIT DONOR
# ──────────────────────────────────────────────────────────────────────────────

elif choice == "Edit Donor":
    st.subheader("✏️ Edit Donor")
    donor_id = st.number_input("Donor ID", min_value=1, step=1, format="%d")

    if st.button("Load Donor"):
        try:
            st.session_state.loaded_donor = db.get_donor_by_id(int(donor_id))
        except Error as e:
            st.error(f"Database error: {e}")

    if st.session_state.get("loaded_donor"):
        d = st.session_state.loaded_donor
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name", value=d[1], key="edit_name")
            dob_val = d[2] if isinstance(d[2], date) else date.fromisoformat(str(d[2]))
            dob = st.date_input(
                "Date of Birth",
                value=dob_val,
                min_value=date(1900, 1, 1),
                max_value=date.today(),
                key="edit_dob",
            )
            gender = st.selectbox(
                "Gender", GENDERS, index=list(GENDERS).index(d[3]), key="edit_gender"
            )
        with col2:
            blood_group = st.selectbox(
                "Blood Group",
                BLOOD_GROUPS,
                index=list(BLOOD_GROUPS).index(d[4]),
                key="edit_bg",
            )
            phone = st.text_input("Phone Number", value=d[5], key="edit_phone")
            email = st.text_input("Email Address", value=d[6], key="edit_email")

        if st.button("Save Changes"):
            errors = []
            name = name.strip()
            if len(name) < 2:
                errors.append("Name must be at least 2 characters.")
            if not validate_age(dob):
                errors.append("Donor must be at least 18 years old.")
            if not validate_phone(phone):
                errors.append("Phone must be 10–15 digits.")
            if not validate_email(email):
                errors.append("Please enter a valid email address.")

            if errors:
                for err in errors:
                    st.error(f"❌ {err}")
            else:
                try:
                    db.update_donor(
                        int(donor_id), name, dob.isoformat(),
                        gender, blood_group, phone, email,
                    )
                    st.success("✅ Donor updated successfully!")
                    del st.session_state.loaded_donor
                except IntegrityError:
                    st.error("❌ A donor with this phone or email already exists.")
                except Error as e:
                    st.error(f"Database error: {e}")
    elif "loaded_donor" in st.session_state:
        st.warning("Donor not found.")

# ──────────────────────────────────────────────────────────────────────────────
# DELETE DONOR
# ──────────────────────────────────────────────────────────────────────────────

elif choice == "Delete Donor":
    st.subheader("🗑️ Delete Donor")
    donor_id = st.number_input("Donor ID to delete", min_value=1, step=1, format="%d")

    try:
        row = db.get_donor_by_id(int(donor_id))
    except Error as e:
        st.error(f"Database error: {e}")
        row = None

    if row:
        st.info(
            f"Donor: **{row[1]}** | Blood Group: **{row[4]}** | Phone: **{row[5]}**"
        )
        if st.button("⚠️ Confirm Delete", type="primary"):
            try:
                db.delete_donor(int(donor_id))
                st.success("✅ Donor deleted successfully.")
            except Error as e:
                st.error(f"Database error: {e}")
    else:
        st.warning("No donor found with that ID.")

# ──────────────────────────────────────────────────────────────────────────────
# SEARCH DONOR
# ──────────────────────────────────────────────────────────────────────────────

elif choice == "Search Donor":
    st.subheader("🔍 Search Donors by Blood Group")
    bg = st.selectbox("Blood Group", BLOOD_GROUPS)

    if st.button("Search"):
        try:
            results = db.get_donors_by_blood_group(bg)
        except Error as e:
            st.error(f"Database error: {e}")
            results = []

        if results:
            df = pd.DataFrame(results, columns=DONOR_COLS)
            st.success(f"Found {len(df)} donor(s)")
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("No donors found for this blood group.")

# ──────────────────────────────────────────────────────────────────────────────
# BLOOD INVENTORY
# ──────────────────────────────────────────────────────────────────────────────

elif choice == "Blood Inventory":
    st.subheader("🩸 Blood Inventory")

    try:
        data = db.get_inventory_summary()
    except Error as e:
        st.error(f"Database error: {e}")
        data = []

    if data:
        df = pd.DataFrame(data, columns=["Blood Group", "Units Available"])
        st.dataframe(df, use_container_width=True)
        st.subheader("📊 Inventory Chart")
        st.bar_chart(df.set_index("Blood Group"))
    else:
        st.warning("No available blood units in inventory.")

    st.subheader("⏰ Expiry Alerts")
    days_ahead = st.slider("Show units expiring within (days)", 1, 30, 7)

    try:
        expiring = db.get_expiring_units_detail(days_ahead)
    except Error as e:
        st.error(f"Database error: {e}")
        expiring = []

    if expiring:
        exp_df = pd.DataFrame(
            expiring,
            columns=["Unit ID", "Blood Group", "Collection Date", "Expiry Date", "Days Left"],
        )
        st.warning(f"⚠️ {len(exp_df)} unit(s) expiring within {days_ahead} days")
        st.dataframe(exp_df, use_container_width=True)
    else:
        st.success(f"No units expiring within {days_ahead} days.")

# ──────────────────────────────────────────────────────────────────────────────
# BLOOD REQUESTS
# ──────────────────────────────────────────────────────────────────────────────

elif choice == "Blood Requests":
    st.subheader("📋 Blood Requests")
    tab1, tab2, tab3 = st.tabs(["View All", "New Request", "Update Status"])

    with tab1:
        try:
            requests = db.get_all_requests()
        except Error as e:
            st.error(f"Database error: {e}")
            requests = []

        if requests:
            req_df = pd.DataFrame(
                requests,
                columns=["ID", "Patient", "Hospital", "Blood Group", "Units", "Request Date", "Status"],
            )
            st.dataframe(req_df, use_container_width=True)
        else:
            st.info("No blood requests found.")

    with tab2:
        try:
            patients = db.get_all_patients()
        except Error as e:
            st.error(f"Database error: {e}")
            patients = []

        if patients:
            patient_options = {f"{p[0]} – {p[1]}": p[0] for p in patients}
            selected_patient = st.selectbox("Patient", list(patient_options.keys()))
            patient_id = patient_options[selected_patient]
            req_bg = st.selectbox("Blood Group Required", BLOOD_GROUPS, key="req_bg")
            req_qty = st.number_input("Quantity (units)", min_value=1, step=1)
            req_date = st.date_input("Request Date", value=date.today())

            if st.button("Submit Request"):
                try:
                    db.add_request(patient_id, req_bg, int(req_qty), req_date.isoformat())
                    st.success("✅ Blood request submitted successfully!")
                except Error as e:
                    st.error(f"Database error: {e}")
        else:
            st.warning("No patients in the database. Add patients first via Hospitals & Patients.")

    with tab3:
        req_id = st.number_input("Request ID", min_value=1, step=1, format="%d")
        new_status = st.selectbox("New Status", REQUEST_STATUSES)

        if st.button("Update Status"):
            try:
                db.update_request_status(int(req_id), new_status)
                st.success(f"✅ Request {req_id} updated to '{new_status}'.")
            except Error as e:
                st.error(f"Database error: {e}")

# ──────────────────────────────────────────────────────────────────────────────
# HOSPITALS & PATIENTS
# ──────────────────────────────────────────────────────────────────────────────

elif choice == "Hospitals & Patients":
    st.subheader("🏥 Hospitals & Patients")
    tab1, tab2, tab3, tab4 = st.tabs(
        ["View Hospitals", "Add Hospital", "View Patients", "Add Patient"]
    )

    with tab1:
        try:
            hospitals = db.get_all_hospitals()
        except Error as e:
            st.error(f"Database error: {e}")
            hospitals = []

        if hospitals:
            h_df = pd.DataFrame(hospitals, columns=["ID", "Name", "Address", "Contact"])
            st.dataframe(h_df, use_container_width=True)
        else:
            st.info("No hospitals found.")

    with tab2:
        h_name = st.text_input("Hospital Name")
        h_address = st.text_input("Address")
        h_contact = st.text_input("Contact Number (10–15 digits)")

        if st.button("Add Hospital"):
            errors = []
            if not h_name.strip():
                errors.append("Hospital name is required.")
            if not h_address.strip():
                errors.append("Address is required.")
            if not validate_phone(h_contact):
                errors.append("Contact must be 10–15 digits.")

            if errors:
                for err in errors:
                    st.error(f"❌ {err}")
            else:
                try:
                    db.add_hospital(h_name.strip(), h_address.strip(), h_contact.strip())
                    st.success("✅ Hospital added successfully!")
                except IntegrityError:
                    st.error("❌ A hospital with this contact number already exists.")
                except Error as e:
                    st.error(f"Database error: {e}")

    with tab3:
        try:
            patients = db.get_all_patients()
        except Error as e:
            st.error(f"Database error: {e}")
            patients = []

        if patients:
            p_df = pd.DataFrame(
                patients,
                columns=["ID", "Name", "DOB", "Blood Group", "Gender", "Hospital"],
            )
            st.dataframe(p_df, use_container_width=True)
        else:
            st.info("No patients found.")

    with tab4:
        try:
            hospitals = db.get_all_hospitals()
        except Error as e:
            st.error(f"Database error: {e}")
            hospitals = []

        if hospitals:
            hosp_options = {f"{h[0]} – {h[1]}": h[0] for h in hospitals}
            p_name = st.text_input("Patient Full Name")
            p_dob = st.date_input(
                "Date of Birth",
                value=date(1990, 1, 1),
                min_value=date(1900, 1, 1),
                max_value=date.today(),
                key="p_dob",
            )
            p_bg = st.selectbox("Blood Group", BLOOD_GROUPS, key="p_bg")
            p_gender = st.selectbox("Gender", GENDERS, key="p_gender")
            p_hosp = st.selectbox("Hospital", list(hosp_options.keys()))
            p_hosp_id = hosp_options[p_hosp]

            if st.button("Add Patient"):
                p_name = p_name.strip()
                if len(p_name) < 2:
                    st.error("❌ Patient name must be at least 2 characters.")
                else:
                    try:
                        db.add_patient(p_name, p_dob.isoformat(), p_bg, p_gender, p_hosp_id)
                        st.success("✅ Patient added successfully!")
                    except Error as e:
                        st.error(f"Database error: {e}")
        else:
            st.warning("No hospitals available. Add a hospital first.")

# ── Footer ────────────────────────────────────────────────────────────────────

st.markdown("---")
st.caption("Built by Sunny Yadav | Data Science & AI")