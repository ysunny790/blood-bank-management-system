CREATE DATABASE Bloodbank_Management_System;
USE Bloodbank_Management_System;

-- ===============================
-- 1. Bloodbank Table
-- ===============================
CREATE TABLE Bloodbank (
    bloodbank_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    location VARCHAR(200) NOT NULL,
    contact_no VARCHAR(15) NOT NULL UNIQUE
);

-- ===============================
-- 2. Donor Table
-- ===============================
CREATE TABLE Donor (
    donor_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(150) NOT NULL,
    date_of_birth DATE NOT NULL,
    gender ENUM('Male','Female','Others') NOT NULL,
    bloodgroup ENUM('A+','A-','B+','B-','O+','O-','AB+','AB-') NOT NULL,
    phone_number VARCHAR(15) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE
);

-- ===============================
-- 3. Donation Table
-- ===============================
CREATE TABLE Donation (
    donation_id INT AUTO_INCREMENT PRIMARY KEY,
    donor_id INT NOT NULL,
    bloodbank_id INT NOT NULL,
    donation_date DATE NOT NULL,
    quantity_ml INT NOT NULL CHECK (quantity_ml > 0),
    hemoglobin_level DECIMAL(4,2) NOT NULL CHECK (hemoglobin_level > 0),

    FOREIGN KEY (donor_id)
        REFERENCES Donor(donor_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    FOREIGN KEY (bloodbank_id)
        REFERENCES Bloodbank(bloodbank_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

CREATE INDEX idx_donation_donor ON Donation(donor_id);
CREATE INDEX idx_donation_bloodbank ON Donation(bloodbank_id);

-- ===============================
-- 4. BloodUnit Table
-- ===============================
CREATE TABLE BloodUnit (
    bloodunit_id INT AUTO_INCREMENT PRIMARY KEY,
    donation_id INT NOT NULL,
    collection_date DATE NOT NULL,
    expiry_date DATE NOT NULL,
    status ENUM('Available','Reserved','Issued')
        NOT NULL DEFAULT 'Available',

    CHECK (expiry_date > collection_date),

    FOREIGN KEY (donation_id)
        REFERENCES Donation(donation_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE INDEX idx_bloodunit_donation ON BloodUnit(donation_id);

-- ===============================
-- 5. Hospital Table
-- ===============================
CREATE TABLE Hospital (
    hospital_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    address VARCHAR(200) NOT NULL,
    contact_number VARCHAR(15) NOT NULL UNIQUE
);

-- ===============================
-- 6. Patient Table
-- ===============================
CREATE TABLE Patient (
    patient_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    date_of_birth DATE NOT NULL,
    bloodgroup ENUM('A+','A-','B+','B-','O+','O-','AB+','AB-') NOT NULL,
    gender ENUM('Male','Female','Others') NOT NULL,
    hospital_id INT NOT NULL,

    FOREIGN KEY (hospital_id)
        REFERENCES Hospital(hospital_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

CREATE INDEX idx_patient_hospital ON Patient(hospital_id);

-- ===============================
-- 7. Blood_Request Table
-- ===============================
CREATE TABLE Blood_Request (
    bloodrequest_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    bloodgroup ENUM('A+','A-','B+','B-','O+','O-','AB+','AB-') NOT NULL,
    quantity_units INT NOT NULL CHECK (quantity_units > 0),
    request_date DATE NOT NULL,
    status ENUM('Pending','Approved','Completed','Rejected')
        NOT NULL DEFAULT 'Pending',

    FOREIGN KEY (patient_id)
        REFERENCES Patient(patient_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE INDEX idx_request_patient ON Blood_Request(patient_id);

-- ===============================
-- 8. Request_BloodUnit Table
-- ===============================
CREATE TABLE Request_BloodUnit (
    bloodrequest_id INT NOT NULL,
    bloodunit_id INT NOT NULL,
    allocation_date DATE NOT NULL,

    PRIMARY KEY (bloodrequest_id, bloodunit_id),

    FOREIGN KEY (bloodrequest_id)
        REFERENCES Blood_Request(bloodrequest_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    FOREIGN KEY (bloodunit_id)
        REFERENCES BloodUnit(bloodunit_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

CREATE INDEX idx_requestbloodunit_unit ON Request_BloodUnit(bloodunit_id);