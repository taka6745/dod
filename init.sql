-- Create the database
CREATE DATABASE roster_db;

-- Use the newly created database
USE roster_db;

-- Create the doctors table
CREATE TABLE doctors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- Create the rosters table
CREATE TABLE rosters (
    id INT AUTO_INCREMENT PRIMARY KEY,
    doctor_id INT,
    date DATE,
    start_time TIME,
    end_time TIME,
    business_hours DECIMAL(5, 2),
    after_hours DECIMAL(5, 2),
    FOREIGN KEY (doctor_id) REFERENCES doctors(id)
);

CREATE USER 'DOD'@'%' IDENTIFIED BY 'DODPASS';
GRANT ALL PRIVILEGES ON roster_db.* TO 'DOD'@'%';
FLUSH PRIVILEGES;
