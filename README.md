# 🩸 Blood Bank Management System

## 📌 Overview

This project is a **full-stack data-driven application** designed to manage blood donation, storage, and distribution efficiently.

It integrates:

* **Relational Database (MySQL)**
* **Backend Logic (Python)**
* **Interactive Web Interface (Streamlit)**

The system simulates real-world blood bank operations including donor management, inventory tracking, and data analysis.

---

## 🚀 Key Features

### 🧑‍⚕️ Donor Management

* View all donors
* Add new donor records
* Search donors by blood group

### 🩸 Blood Inventory System

* Track available blood units
* Group-wise inventory analysis
* Real-time data retrieval

### 📊 Dashboard & Analytics

* Total donors count
* Available blood units
* Visual representation using charts

### 💻 Interactive Web App

* Built using Streamlit
* Clean UI with sidebar navigation
* Real-time database interaction

---

## 🧠 System Architecture

```text
User Interface (Streamlit)
        ↓
Python Backend (MySQL Connector)
        ↓
MySQL Database (Relational Schema)
```

---

## 🗂️ Project Structure

```
blood-bank-management-system/
│
├── schema.sql           # Database structure
├── data.sql             # Sample data
├── queries.sql          # SQL operations
├── app.py               # CLI version (basic interaction)
├── streamlit_app.py     # Web application (main project)
└── README.md
```

---

## 🛠️ Tech Stack

* Python
* MySQL
* Streamlit
* Pandas

---

## ⚙️ How to Run Locally

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

### 3. Run Application

```bash
streamlit run streamlit_app.py
```

---

## 📊 Sample Functionalities

* Add a new donor through UI
* Search donors by blood group
* View complete donor list
* Analyze available blood inventory
* Visualize data using charts

---

## 🔥 What Makes This Project Stand Out

* Combines **Database + Backend + UI**
* Demonstrates **real-world system design**
* Uses **SQL joins, constraints, and indexing**
* Converts academic DBMS project into a **working application**
* Includes **data visualization and analytics**

---

## ⚠️ Challenges Solved

* Maintaining referential integrity
* Handling relational data across multiple tables
* Connecting Python with MySQL
* Designing an interactive UI for database operations

---

## 🔮 Future Improvements

* Add hospital & blood request module
* Implement authentication system
* Deploy app online (Streamlit Cloud)
* Add advanced analytics dashboard

---

## 👨‍💻 Author

**Sunny Yadav**
BSc Data Science & AI

---

## 📢 Note

This project reflects a transition from **academic database design** to a **real-world application**, focusing on practical implementation and system building.
