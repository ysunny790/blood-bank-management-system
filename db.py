"""Database access layer for the Blood Bank Management System.

All SQL lives here; the UI layer only calls methods on DatabaseManager.
Each method opens its own connection so the app is safe for concurrent
Streamlit sessions.
"""

import os
import re
from datetime import date

import mysql.connector
from dotenv import load_dotenv

load_dotenv()

BLOOD_GROUPS = ("A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-")
GENDERS = ("Male", "Female", "Others")
REQUEST_STATUSES = ("Pending", "Approved", "Completed", "Rejected")


# ── Validation helpers ────────────────────────────────────────────────────────

def validate_phone(phone: str) -> bool:
    """Return True if *phone* is 10–15 digits with an optional leading '+'."""
    return bool(re.fullmatch(r"\+?\d{10,15}", phone.strip()))


def validate_email(email: str) -> bool:
    """Return True if *email* looks like a valid e-mail address.

    Uses a linear-time pattern (no nested quantifiers) to avoid ReDoS.
    """
    return bool(re.fullmatch(r"[\w.+\-]+@[\w\-]+(?:\.[\w\-]+)+", email.strip()))


def validate_age(dob: date, min_age: int = 18) -> bool:
    """Return True if the person born on *dob* is at least *min_age* years old."""
    today = date.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    return age >= min_age


# ── Connection factory ────────────────────────────────────────────────────────

def get_connection() -> mysql.connector.MySQLConnection:
    """Return a fresh database connection using environment variables."""
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "Bloodbank_Management_System"),
    )


# ── DatabaseManager ───────────────────────────────────────────────────────────

class DatabaseManager:
    """Single access point for all database operations."""

    def _run(self, query: str, params: tuple = (), *, fetch: str = "none"):
        """
        Execute *query* with *params* and optionally fetch results.

        fetch='one'  → single row (tuple | None)
        fetch='all'  → list of tuples
        fetch='none' → commit and return lastrowid
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            try:
                cursor.execute(query, params)
                if fetch == "one":
                    return cursor.fetchone()
                if fetch == "all":
                    return cursor.fetchall()
                conn.commit()
                return cursor.lastrowid
            finally:
                cursor.close()
        finally:
            conn.close()

    # ── Dashboard ─────────────────────────────────────────────────────────────

    def get_total_donors(self) -> int:
        row = self._run("SELECT COUNT(*) FROM Donor", fetch="one")
        return row[0] if row else 0

    def get_available_units(self) -> int:
        row = self._run(
            "SELECT COUNT(*) FROM BloodUnit WHERE status = 'Available'",
            fetch="one",
        )
        return row[0] if row else 0

    def get_pending_requests(self) -> int:
        row = self._run(
            "SELECT COUNT(*) FROM Blood_Request WHERE status = 'Pending'",
            fetch="one",
        )
        return row[0] if row else 0

    def get_expiring_soon_count(self, days: int = 7) -> int:
        row = self._run(
            "SELECT COUNT(*) FROM BloodUnit "
            "WHERE status = 'Available' "
            "  AND expiry_date BETWEEN CURDATE() "
            "      AND DATE_ADD(CURDATE(), INTERVAL %s DAY)",
            (days,),
            fetch="one",
        )
        return row[0] if row else 0

    # ── Donors ────────────────────────────────────────────────────────────────

    def get_all_donors(self) -> list:
        return self._run(
            """
            SELECT d.donor_id, d.full_name, d.date_of_birth, d.gender,
                   d.bloodgroup, d.phone_number, d.email,
                   MAX(dn.donation_date) AS last_donation
            FROM Donor d
            LEFT JOIN Donation dn ON d.donor_id = dn.donor_id
            GROUP BY d.donor_id, d.full_name, d.date_of_birth,
                     d.gender, d.bloodgroup, d.phone_number, d.email
            ORDER BY d.donor_id
            """,
            fetch="all",
        )

    def get_donor_by_id(self, donor_id: int):
        return self._run(
            "SELECT donor_id, full_name, date_of_birth, gender, "
            "bloodgroup, phone_number, email FROM Donor WHERE donor_id = %s",
            (donor_id,),
            fetch="one",
        )

    def get_donors_by_blood_group(self, blood_group: str) -> list:
        return self._run(
            """
            SELECT d.donor_id, d.full_name, d.date_of_birth, d.gender,
                   d.bloodgroup, d.phone_number, d.email,
                   MAX(dn.donation_date) AS last_donation
            FROM Donor d
            LEFT JOIN Donation dn ON d.donor_id = dn.donor_id
            WHERE d.bloodgroup = %s
            GROUP BY d.donor_id, d.full_name, d.date_of_birth,
                     d.gender, d.bloodgroup, d.phone_number, d.email
            """,
            (blood_group,),
            fetch="all",
        )

    def add_donor(
        self,
        name: str,
        dob: str,
        gender: str,
        blood_group: str,
        phone: str,
        email: str,
    ) -> int:
        return self._run(
            "INSERT INTO Donor "
            "(full_name, date_of_birth, gender, bloodgroup, phone_number, email) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (name, dob, gender, blood_group, phone, email),
        )

    def update_donor(
        self,
        donor_id: int,
        name: str,
        dob: str,
        gender: str,
        blood_group: str,
        phone: str,
        email: str,
    ) -> None:
        self._run(
            "UPDATE Donor SET full_name=%s, date_of_birth=%s, gender=%s, "
            "bloodgroup=%s, phone_number=%s, email=%s WHERE donor_id=%s",
            (name, dob, gender, blood_group, phone, email, donor_id),
        )

    def delete_donor(self, donor_id: int) -> None:
        self._run("DELETE FROM Donor WHERE donor_id = %s", (donor_id,))

    def donor_eligible_to_donate(self, donor_id: int) -> bool:
        """Return True if the donor's last donation was more than 90 days ago (or never)."""
        row = self._run(
            "SELECT MAX(donation_date) FROM Donation WHERE donor_id = %s",
            (donor_id,),
            fetch="one",
        )
        if row is None or row[0] is None:
            return True
        return (date.today() - row[0]).days > 90

    # ── Inventory ─────────────────────────────────────────────────────────────

    def get_inventory_summary(self) -> list:
        return self._run(
            """
            SELECT dr.bloodgroup, COUNT(*) AS units_available
            FROM BloodUnit bu
            JOIN Donation d  ON bu.donation_id = d.donation_id
            JOIN Donor   dr  ON d.donor_id     = dr.donor_id
            WHERE bu.status = 'Available'
            GROUP BY dr.bloodgroup
            ORDER BY dr.bloodgroup
            """,
            fetch="all",
        )

    def get_expiring_units_detail(self, days: int = 7) -> list:
        return self._run(
            """
            SELECT bu.bloodunit_id, dr.bloodgroup,
                   bu.collection_date, bu.expiry_date,
                   DATEDIFF(bu.expiry_date, CURDATE()) AS days_left
            FROM BloodUnit bu
            JOIN Donation d  ON bu.donation_id = d.donation_id
            JOIN Donor   dr  ON d.donor_id     = dr.donor_id
            WHERE bu.status = 'Available'
              AND bu.expiry_date BETWEEN CURDATE()
                  AND DATE_ADD(CURDATE(), INTERVAL %s DAY)
            ORDER BY bu.expiry_date
            """,
            (days,),
            fetch="all",
        )

    # ── Hospitals ─────────────────────────────────────────────────────────────

    def get_all_hospitals(self) -> list:
        return self._run(
            "SELECT hospital_id, name, address, contact_number "
            "FROM Hospital ORDER BY hospital_id",
            fetch="all",
        )

    def add_hospital(self, name: str, address: str, contact: str) -> int:
        return self._run(
            "INSERT INTO Hospital (name, address, contact_number) VALUES (%s, %s, %s)",
            (name, address, contact),
        )

    # ── Patients ──────────────────────────────────────────────────────────────

    def get_all_patients(self) -> list:
        return self._run(
            """
            SELECT p.patient_id, p.full_name, p.date_of_birth,
                   p.bloodgroup, p.gender, h.name AS hospital
            FROM Patient  p
            JOIN Hospital h ON p.hospital_id = h.hospital_id
            ORDER BY p.patient_id
            """,
            fetch="all",
        )

    def add_patient(
        self,
        name: str,
        dob: str,
        blood_group: str,
        gender: str,
        hospital_id: int,
    ) -> int:
        return self._run(
            "INSERT INTO Patient "
            "(full_name, date_of_birth, bloodgroup, gender, hospital_id) "
            "VALUES (%s, %s, %s, %s, %s)",
            (name, dob, blood_group, gender, hospital_id),
        )

    # ── Blood Requests ────────────────────────────────────────────────────────

    def get_all_requests(self) -> list:
        return self._run(
            """
            SELECT br.bloodrequest_id, p.full_name AS patient,
                   h.name AS hospital,
                   br.bloodgroup, br.quantity_units,
                   br.request_date, br.status
            FROM Blood_Request br
            JOIN Patient  p ON br.patient_id  = p.patient_id
            JOIN Hospital h ON p.hospital_id  = h.hospital_id
            ORDER BY br.request_date DESC
            """,
            fetch="all",
        )

    def add_request(
        self,
        patient_id: int,
        blood_group: str,
        quantity: int,
        request_date: str,
    ) -> int:
        return self._run(
            "INSERT INTO Blood_Request "
            "(patient_id, bloodgroup, quantity_units, request_date) "
            "VALUES (%s, %s, %s, %s)",
            (patient_id, blood_group, quantity, request_date),
        )

    def update_request_status(self, request_id: int, status: str) -> None:
        self._run(
            "UPDATE Blood_Request SET status = %s WHERE bloodrequest_id = %s",
            (status, request_id),
        )
