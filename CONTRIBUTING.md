# Contributing to Blood Bank Management System

## Prerequisites

- Python 3.9+
- MySQL 8.0+

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/ysunny790/blood-bank-management-system.git
cd blood-bank-management-system
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

```bash
cp .env.example .env
# Open .env and fill in your MySQL credentials
```

### 4. Create the database

```bash
mysql -u root -p < schema.sql
mysql -u root -p Bloodbank_Management_System < data.sql
```

### 5. Run the web app

```bash
streamlit run streamlit_app.py
```

### 6. Run the CLI version

```bash
python app.py
```

### 7. Run tests

No MySQL instance needed — all DB calls are mocked.

```bash
pytest tests/ -v
```

## Code Guidelines

- All SQL must live in `db.py`. The UI layer (`streamlit_app.py`) only calls
  methods on `DatabaseManager`.
- Each `DatabaseManager` method opens and closes its own connection so the app
  is safe for concurrent Streamlit sessions.
- Validate user input using the helpers in `db.py` (`validate_phone`,
  `validate_email`, `validate_age`) before writing to the database.
- Catch specific exceptions (`mysql.connector.Error`, `IntegrityError`) rather
  than bare `except Exception`.

## Pull Requests

1. Branch off `main`.
2. Write tests for any new `DatabaseManager` methods.
3. Update `README.md` if the setup steps change.
4. Keep commits focused and descriptive.
