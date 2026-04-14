-- ===============================
-- 1. Bloodbank (2 records)
-- ===============================
INSERT INTO Bloodbank (name, location, contact_no) VALUES
('City Blood Center', 'Downtown', '9876543210'),
('Red Cross Unit', 'Uptown', '9123456780');

-- ===============================
-- 2. Hospital (3 records)
-- ===============================
INSERT INTO Hospital (name, address, contact_number) VALUES
('General Hospital', 'Main Road', '9000000001'),
('LifeCare Hospital', 'North Avenue', '9000000002'),
('Hope Medical Center', 'East Street', '9000000003');

-- ===============================
-- 3. Donor (10 records)
-- ===============================
INSERT INTO Donor (full_name, date_of_birth, gender, bloodgroup, phone_number, email) VALUES
('Rahul Sharma', '1995-05-10', 'Male', 'A+', '8000000001', 'rahul1@mail.com'),
('Anita Verma', '1992-08-15', 'Female', 'B+', '8000000002', 'anita1@mail.com'),
('Suresh Kumar', '1990-01-20', 'Male', 'O+', '8000000003', 'suresh1@mail.com'),
('Priya Singh', '1998-03-12', 'Female', 'AB+', '8000000004', 'priya1@mail.com'),
('Vikram Joshi', '1989-07-22', 'Male', 'A-', '8000000005', 'vikram1@mail.com'),
('Neha Patel', '1996-11-05', 'Female', 'O-', '8000000006', 'neha1@mail.com'),
('Rohan Das', '1994-09-18', 'Male', 'B-', '8000000007', 'rohan1@mail.com'),
('Sneha Roy', '1993-12-30', 'Female', 'AB-', '8000000008', 'sneha1@mail.com'),
('Amit Gupta', '1991-04-11', 'Male', 'A+', '8000000009', 'amit1@mail.com'),
('Kavita Mehta', '1997-06-25', 'Female', 'O+', '8000000010', 'kavita1@mail.com');

-- ===============================
-- 4. Donation (10 records)
-- ===============================
INSERT INTO Donation (donor_id, bloodbank_id, donation_date, quantity_ml, hemoglobin_level) VALUES
(1, 1, '2025-01-01', 450, 13.5),
(2, 1, '2025-01-02', 450, 12.8),
(3, 2, '2025-01-03', 500, 14.1),
(4, 2, '2025-01-04', 450, 13.2),
(5, 1, '2025-01-05', 450, 12.9),
(6, 2, '2025-01-06', 450, 13.8),
(7, 1, '2025-01-07', 500, 14.0),
(8, 2, '2025-01-08', 450, 12.7),
(9, 1, '2025-01-09', 450, 13.6),
(10, 2, '2025-01-10', 500, 14.3);

-- ===============================
-- 5. BloodUnit (10 records)
-- ===============================
INSERT INTO BloodUnit (donation_id, collection_date, expiry_date, status) VALUES
(1, '2025-01-01', '2025-02-01', 'Available'),
(2, '2025-01-02', '2025-02-02', 'Available'),
(3, '2025-01-03', '2025-02-03', 'Reserved'),
(4, '2025-01-04', '2025-02-04', 'Available'),
(5, '2025-01-05', '2025-02-05', 'Issued'),
(6, '2025-01-06', '2025-02-06', 'Available'),
(7, '2025-01-07', '2025-02-07', 'Available'),
(8, '2025-01-08', '2025-02-08', 'Reserved'),
(9, '2025-01-09', '2025-02-09', 'Available'),
(10, '2025-01-10', '2025-02-10', 'Available');

-- ===============================
-- 6. Patient (7 records)
-- ===============================
INSERT INTO Patient (full_name, date_of_birth, bloodgroup, gender, hospital_id) VALUES
('Arjun Rao', '2000-02-14', 'A+', 'Male', 1),
('Meera Nair', '1999-05-20', 'O+', 'Female', 2),
('Kiran Shah', '1985-07-11', 'B+', 'Male', 3),
('Pooja Iyer', '1992-09-09', 'AB+', 'Female', 1),
('Rakesh Yadav', '1978-12-01', 'O-', 'Male', 2),
('Simran Kaur', '2001-03-18', 'A-', 'Female', 3),
('Aman Gupta', '2001-03-19', 'AB-', 'Male', 3);

-- ===============================
-- 7. Blood_Request (7 records)
-- ===============================
INSERT INTO Blood_Request (patient_id, bloodgroup, quantity_units, request_date, status) VALUES
(1, 'A+', 1, '2025-02-01', 'Approved'),
(2, 'O+', 2, '2025-02-02', 'Pending'),
(3, 'B+', 1, '2025-02-03', 'Completed'),
(4, 'AB+', 1, '2025-02-04', 'Approved'),
(5, 'O-', 1, '2025-02-05', 'Rejected'),
(6, 'O-', 2, '2025-02-06', 'Rejected'),
(7, 'A-', 1, '2025-02-07', 'Pending');

-- ===============================
-- 8. Request_BloodUnit (Allocations)
-- ===============================
INSERT INTO Request_BloodUnit (bloodrequest_id, bloodunit_id, allocation_date) VALUES
(1, 1, '2025-02-01'),
(3, 3, '2025-02-03'),
(4, 4, '2025-02-04');
