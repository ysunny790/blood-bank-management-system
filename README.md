# 🩸 Blood Bank Management System

## 📌 Overview

This project is a **data-driven web application** for managing blood donors and blood inventory.

It is built using:

* **MySQL** for database management
* **Python** for backend logic
* **Streamlit** for interactive web interface

The goal is to move beyond a basic DBMS assignment and build a **working system with real interaction**.

---

## 🚀 Features

### 👨‍⚕️ Donor Management

* View all donors
* Add new donor records
* Search donors by blood group

### 🩸 Blood Inventory

* Track available blood units
* Group-wise availability of blood
* Visual representation using charts

### 📊 Dashboard

* Total donors count
* Available blood units

---

## 🧠 Database Design

The system uses a **relational database** with multiple tables:

* Donor
* Donation
* BloodUnit
* Bloodbank
* Hospital
* Patient
* Blood_Request

Includes:

* Primary & Foreign Keys
* Constraints (NOT NULL, UNIQUE, CHECK)
* Relationships between entities

---

## 🗂️ Project Structure

```
blood-bank-management-system/
│
├── schema.sql           # Database schema
├── data.sql             # Sample data
├── queries.sql          # SQL queries
├── app.py               # CLI version
├── streamlit_app.py     # Web application (main)
├── requirements.txt     # Dependencies
└── README.md
```

---

## ⚙️ How to Run

### 1. Setup Database

```sql
CREATE DATABASE test_bloodbank;
USE test_bloodbank;
```

Run:

```sql
SOURCE schema.sql;
SOURCE data.sql;
```

---

### 2. Install Dependencies

```bash
pip install mysql-connector-python streamlit pandas
```

---

### 3. Run the Application

```bash
streamlit run streamlit_app.py
```

---

## 📊 Example Functionalities

* Add a new donor through UI
* View all donors in tabular format
* Search donors by blood group
* Analyze blood availability using charts

---

## ⚠️ Current Limitations

* No blood request workflow implemented yet
* No authentication system
* Runs locally (not deployed online)

---

## 🔮 Future Improvements

* Add blood request and allocation system
* Integrate full donor → donation → request workflow
* Deploy application online
* Add analytics dashboard

---

## 🛠️ Tech Stack

* Python
* MySQL
* Streamlit
* Pandas

---

## 👨‍💻 Author

**Sunny Yadav**
BSc Data Science & AI

---

## 📢 Note

This project focuses on **practical implementation** of database concepts by converting them into a working application instead of just theoretical design.
