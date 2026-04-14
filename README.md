# 🩸 Blood Bank Management System

## 📌 Overview

This project is a **relational database system** designed to manage blood donation, storage, and distribution efficiently between donors, blood banks, hospitals, and patients.

The system ensures **data integrity, traceability, and real-world constraint handling**, simulating how an actual blood bank operates.

---

## 🎯 Objectives

* Maintain accurate records of donors and donations
* Track blood units with expiry and availability status
* Handle hospital requests and patient requirements
* Ensure safe allocation of blood units based on compatibility
* Enforce **data consistency using constraints and relationships**

---

## 🧠 Database Design

### Core Entities:

* **Bloodbank**
* **Donor**
* **Donation**
* **BloodUnit**
* **Hospital**
* **Patient**
* **Blood_Request**
* **Request_BloodUnit (Bridge Table)**

### Key Concepts Implemented:

* Primary & Foreign Keys
* One-to-Many Relationships
* Many-to-Many Relationship (via bridge table)
* Referential Integrity
* Constraints (NOT NULL, UNIQUE, CHECK, DEFAULT)
* Indexing for performance optimization

---

## ⚙️ Features

* 🔍 Track donors and their donation history
* 🧪 Monitor blood units with expiry and status
* 🏥 Manage hospital and patient records
* 📦 Allocate blood units to requests
* 🔄 Maintain full traceability from donor → patient
* ⚠️ Prevent invalid operations using constraints

---

## 🗂️ Project Structure

```
blood-bank-management-system/
│
├── schema.sql     # Database structure (tables, constraints, indexes)
├── data.sql       # Sample data for testing
├── queries.sql    # SQL queries (SELECT, JOIN, UPDATE, DELETE)
└── README.md
```

---

## 🧪 Sample Queries Implemented

* Retrieve available blood units by blood group
* Track donor donation frequency
* Join patient, hospital, and request data
* Identify expired blood units
* Update request status (approve/reject)

---

## 🚀 How to Run

1. Open MySQL / any SQL environment
2. Run:

   ```sql
   SOURCE schema.sql;
   SOURCE data.sql;
   SOURCE queries.sql;
   ```

---

## 🛠️ Tech Stack

* SQL (MySQL)
* Relational Database Design

---

## 📈 What Makes This Project Strong

This is not just a basic academic project. It demonstrates:

* Real-world system modeling
* Proper normalization and schema design
* Use of constraints to enforce business rules
* Efficient query writing with joins and aggregations
* Clean project structuring for reproducibility

---

## 🔮 Future Improvements

* Integrate with Python (backend logic)
* Build a web interface (Streamlit / Flask)
* Add authentication and role-based access
* Implement real-time inventory tracking

---

## 👨‍💻 Author

**Sunny Yadav**
BSc Data Science & AI Student

---

## 📢 Note

This project is part of my learning journey in **Data Science and Database Systems**, focused on building practical, real-world systems rather than just theoretical knowledge.
