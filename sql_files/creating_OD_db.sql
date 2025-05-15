CREATE DATABASE object_detection;
USE object_detection;
-- DROP TABLE IF EXISTS detection_logs;

CREATE TABLE detection_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    class_name VARCHAR(50) NOT NULL,
    count INT NOT NULL,
    date DATE NOT NULL,
    time TIME NOT NULL
);

ALTER TABLE detection_logs
CHANGE COLUMN object_type class_name VARCHAR(50) NOT NULL; 

CREATE INDEX idx_timestamp ON detection_logs (timestamp);