-- 1. Find all available blood units of a specific group
SELECT bloodunit_id, bloodgroup, status
FROM BloodUnit bu
JOIN Donation d ON bu.donation_id = d.donation_id
JOIN Donor dr ON d.donor_id = dr.donor_id
WHERE dr.bloodgroup = 'A+' AND bu.status = 'Available';

-- 2. Count total donations by each donor
SELECT dr.full_name, COUNT(d.donation_id) AS total_donations
FROM Donor dr
LEFT JOIN Donation d ON dr.donor_id = d.donor_id
GROUP BY dr.donor_id, dr.full_name;

-- 3. List all blood requests with patient and hospital
SELECT br.bloodrequest_id, p.full_name AS patient_name, h.name AS hospital_name, br.status
FROM Blood_Request br
JOIN Patient p ON br.patient_id = p.patient_id
JOIN Hospital h ON p.hospital_id = h.hospital_id;

-- 4. Find expired blood units
SELECT bloodunit_id, expiry_date
FROM BloodUnit
WHERE expiry_date < CURDATE();

-- 5. Approve a pending blood request
UPDATE Blood_Request
SET status = 'Approved'
WHERE bloodrequest_id = 2 AND status = 'Pending';

