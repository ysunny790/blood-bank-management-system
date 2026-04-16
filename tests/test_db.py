"""Unit tests for the Blood Bank Management System database layer.

All database calls are mocked so no running MySQL instance is required.
"""

import pytest
from datetime import date
from unittest.mock import MagicMock, patch

from db import (
    DatabaseManager,
    validate_phone,
    validate_email,
    validate_age,
)


# ── Validation: phone ─────────────────────────────────────────────────────────

class TestValidatePhone:
    def test_valid_10_digits(self):
        assert validate_phone("9876543210") is True

    def test_valid_with_plus_prefix(self):
        assert validate_phone("+919876543210") is True

    def test_valid_15_digits(self):
        assert validate_phone("123456789012345") is True

    def test_too_short(self):
        assert validate_phone("12345") is False

    def test_too_long(self):
        assert validate_phone("1234567890123456") is False

    def test_contains_letters(self):
        assert validate_phone("abc1234567") is False

    def test_empty_string(self):
        assert validate_phone("") is False

    def test_whitespace_stripped(self):
        assert validate_phone("  9876543210  ") is True


# ── Validation: email ─────────────────────────────────────────────────────────

class TestValidateEmail:
    def test_valid_simple(self):
        assert validate_email("user@example.com") is True

    def test_valid_subdomain(self):
        assert validate_email("user@mail.example.co.uk") is True

    def test_missing_at(self):
        assert validate_email("userexample.com") is False

    def test_missing_domain(self):
        assert validate_email("user@") is False

    def test_empty_string(self):
        assert validate_email("") is False

    def test_whitespace_stripped(self):
        assert validate_email("  user@example.com  ") is True


# ── Validation: age ───────────────────────────────────────────────────────────

class TestValidateAge:
    def test_adult(self):
        assert validate_age(date(1990, 1, 1)) is True

    def test_exactly_18_today(self):
        today = date.today()
        dob = date(today.year - 18, today.month, today.day)
        assert validate_age(dob) is True

    def test_underage(self):
        assert validate_age(date(2020, 1, 1)) is False

    def test_custom_min_age_met(self):
        young = date(date.today().year - 16, 1, 1)
        assert validate_age(young, min_age=16) is True

    def test_custom_min_age_not_met(self):
        young = date(date.today().year - 15, 6, 1)
        assert validate_age(young, min_age=16) is False


# ── DatabaseManager helpers ───────────────────────────────────────────────────

def _make_mock_conn(fetchone=None, fetchall=None, lastrowid=1):
    """Return a (mock_conn, mock_cursor) pair with preset return values."""
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = fetchone
    mock_cursor.fetchall.return_value = fetchall if fetchall is not None else []
    mock_cursor.lastrowid = lastrowid

    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    return mock_conn, mock_cursor


# ── DatabaseManager tests ─────────────────────────────────────────────────────

class TestDatabaseManager:

    @patch("db.get_connection")
    def test_get_total_donors(self, mock_get_conn):
        mock_conn, _ = _make_mock_conn(fetchone=(7,))
        mock_get_conn.return_value = mock_conn
        assert DatabaseManager().get_total_donors() == 7

    @patch("db.get_connection")
    def test_get_total_donors_empty_db(self, mock_get_conn):
        mock_conn, _ = _make_mock_conn(fetchone=None)
        mock_get_conn.return_value = mock_conn
        assert DatabaseManager().get_total_donors() == 0

    @patch("db.get_connection")
    def test_get_available_units(self, mock_get_conn):
        mock_conn, _ = _make_mock_conn(fetchone=(3,))
        mock_get_conn.return_value = mock_conn
        assert DatabaseManager().get_available_units() == 3

    @patch("db.get_connection")
    def test_get_pending_requests(self, mock_get_conn):
        mock_conn, _ = _make_mock_conn(fetchone=(2,))
        mock_get_conn.return_value = mock_conn
        assert DatabaseManager().get_pending_requests() == 2

    @patch("db.get_connection")
    def test_get_expiring_soon_count(self, mock_get_conn):
        mock_conn, _ = _make_mock_conn(fetchone=(4,))
        mock_get_conn.return_value = mock_conn
        assert DatabaseManager().get_expiring_soon_count(days=7) == 4

    @patch("db.get_connection")
    def test_get_all_donors_returns_list(self, mock_get_conn):
        rows = [
            (1, "Alice", date(1990, 1, 1), "Female", "A+",
             "9999999999", "alice@test.com", None)
        ]
        mock_conn, _ = _make_mock_conn(fetchall=rows)
        mock_get_conn.return_value = mock_conn
        assert DatabaseManager().get_all_donors() == rows

    @patch("db.get_connection")
    def test_get_donor_by_id_found(self, mock_get_conn):
        row = (1, "Alice", date(1990, 1, 1), "Female", "A+", "9999999999", "alice@test.com")
        mock_conn, _ = _make_mock_conn(fetchone=row)
        mock_get_conn.return_value = mock_conn
        assert DatabaseManager().get_donor_by_id(1) == row

    @patch("db.get_connection")
    def test_get_donor_by_id_not_found(self, mock_get_conn):
        mock_conn, _ = _make_mock_conn(fetchone=None)
        mock_get_conn.return_value = mock_conn
        assert DatabaseManager().get_donor_by_id(999) is None

    @patch("db.get_connection")
    def test_add_donor_returns_lastrowid(self, mock_get_conn):
        mock_conn, _ = _make_mock_conn(lastrowid=5)
        mock_get_conn.return_value = mock_conn
        row_id = DatabaseManager().add_donor(
            "Bob", "1985-06-15", "Male", "O+", "8888888888", "bob@test.com"
        )
        assert row_id == 5
        mock_conn.commit.assert_called_once()

    @patch("db.get_connection")
    def test_update_donor_commits(self, mock_get_conn):
        mock_conn, mock_cursor = _make_mock_conn()
        mock_get_conn.return_value = mock_conn
        DatabaseManager().update_donor(
            1, "Alice", "1990-01-01", "Female", "A+", "9999999999", "alice@test.com"
        )
        mock_conn.commit.assert_called_once()

    @patch("db.get_connection")
    def test_delete_donor_commits(self, mock_get_conn):
        mock_conn, _ = _make_mock_conn()
        mock_get_conn.return_value = mock_conn
        DatabaseManager().delete_donor(3)
        mock_conn.commit.assert_called_once()

    @patch("db.get_connection")
    def test_donor_eligible_never_donated(self, mock_get_conn):
        mock_conn, _ = _make_mock_conn(fetchone=(None,))
        mock_get_conn.return_value = mock_conn
        assert DatabaseManager().donor_eligible_to_donate(1) is True

    @patch("db.get_connection")
    def test_donor_eligible_old_donation(self, mock_get_conn):
        old = date(date.today().year - 1, 1, 1)
        mock_conn, _ = _make_mock_conn(fetchone=(old,))
        mock_get_conn.return_value = mock_conn
        assert DatabaseManager().donor_eligible_to_donate(1) is True

    @patch("db.get_connection")
    def test_donor_not_eligible_recent_donation(self, mock_get_conn):
        recent = date.today()  # donated today → 0 days ago, not > 90
        mock_conn, _ = _make_mock_conn(fetchone=(recent,))
        mock_get_conn.return_value = mock_conn
        assert DatabaseManager().donor_eligible_to_donate(1) is False

    @patch("db.get_connection")
    def test_add_request_returns_id(self, mock_get_conn):
        mock_conn, _ = _make_mock_conn(lastrowid=10)
        mock_get_conn.return_value = mock_conn
        row_id = DatabaseManager().add_request(1, "A+", 2, "2026-04-16")
        assert row_id == 10
        mock_conn.commit.assert_called_once()

    @patch("db.get_connection")
    def test_update_request_status_commits(self, mock_get_conn):
        mock_conn, mock_cursor = _make_mock_conn()
        mock_get_conn.return_value = mock_conn
        DatabaseManager().update_request_status(2, "Approved")
        mock_conn.commit.assert_called_once()
        mock_cursor.execute.assert_called_once()

    @patch("db.get_connection")
    def test_connection_error_propagates(self, mock_get_conn):
        from mysql.connector import Error
        mock_get_conn.side_effect = Error("Connection refused")
        with pytest.raises(Error):
            DatabaseManager().get_total_donors()

    @patch("db.get_connection")
    def test_connection_closed_after_query(self, mock_get_conn):
        mock_conn, _ = _make_mock_conn(fetchone=(5,))
        mock_get_conn.return_value = mock_conn
        DatabaseManager().get_total_donors()
        mock_conn.close.assert_called_once()

    @patch("db.get_connection")
    def test_cursor_closed_after_query(self, mock_get_conn):
        mock_conn, mock_cursor = _make_mock_conn(fetchone=(5,))
        mock_get_conn.return_value = mock_conn
        DatabaseManager().get_total_donors()
        mock_cursor.close.assert_called_once()
