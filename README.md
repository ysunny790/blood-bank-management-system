# 🩸 Blood Bank Management System

## 📌 Overview

A **full-stack data-driven application** for managing blood donation, storage, and distribution.

It integrates:

* **Relational Database (MySQL)**
* **Backend Logic (Python)**
* **Interactive Web Interface (Streamlit)**

---

## 🚀 Key Features

### 🧑‍⚕️ Donor Management

* View all donors with last-donation date and pagination
* Add donors with validated inputs (age ≥ 18, phone/email format)
* Edit and delete donor records
* Search donors by blood group

### 🩸 Blood Inventory

* Group-wise inventory summary with bar chart
* Configurable expiry alert (flags units expiring within N days)

### 📋 Blood Requests

* View all requests with patient and hospital details
* Submit new requests
* Update request status (Pending / Approved / Completed / Rejected)

### 🏥 Hospitals & Patients

* View and add hospitals
* View and add patients linked to hospitals

### 📊 Dashboard

* Live counts: total donors, available units, pending requests, expiring units

---

## 🧠 System Architecture

```text
User Interface (streamlit_app.py)
        ↓
Database Layer (db.py → DatabaseManager)
        ↓
MySQL Database (Relational Schema)
```

---

## 🗂️ Project Structure

```
blood-bank-management-system/
│
├── db.py                # Database layer (all SQL + validation helpers)
├── streamlit_app.py     # Web application (Streamlit UI)
├── app.py               # CLI version
│
├── schema.sql           # Database schema
├── data.sql             # Sample data
├── queries.sql          # Example SQL queries
│
├── tests/
│   └── test_db.py       # Unit tests (pytest, no DB required)
│
├── requirements.txt
├── .env.example         # Environment variable template
├── CONTRIBUTING.md
└── README.md
```

---

## 🛠️ Tech Stack

* Python 3.9+
* MySQL 8.0+
* Streamlit
* Pandas
* python-dotenv
* pytest

---

## ⚙️ How to Run Locally

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure credentials

```bash
cp .env.example .env
# Edit .env and set DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
```

### 3. Create the database

```bash
mysql -u root -p < schema.sql
mysql -u root -p Bloodbank_Management_System < data.sql
```

### 4. Run the web app

```bash
streamlit run streamlit_app.py
```

### 5. Run the CLI version (optional)

```bash
python app.py
```

---

## 🧪 Running Tests

No MySQL instance required — all database calls are mocked.

```bash
pytest tests/ -v
```

---

## 🔒 Security Notes

* Database credentials are loaded from a `.env` file (see `.env.example`).
* `.env` is listed in `.gitignore` and must **never** be committed.
* All user inputs are validated (phone format, email format, age ≥ 18) before any DB write.
* Specific MySQL exceptions (`IntegrityError`, `Error`) are caught; bare `except` is avoided.

---

## 🔥 What Makes This Project Stand Out

* Clean separation of **Database ↔ UI** layers
* Per-request DB connections (safe for concurrent Streamlit sessions)
* Full input validation with user-friendly error messages
* 38 unit tests with 100% pass rate
* GitHub Actions CI pipeline

---

## 👨‍💻 Author

**Sunny Yadav**
BSc Data Science & AI

---

## 📢 Note

This project reflects a transition from **academic database design** to a **production-ready application**, focusing on security, correctness, and maintainability.
