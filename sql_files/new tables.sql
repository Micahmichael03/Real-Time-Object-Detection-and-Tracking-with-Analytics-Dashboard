USE object_detection;
DROP TABLE IF EXISTS detection_logs;

CREATE TABLE detection_vaccineslog (
    id INT AUTO_INCREMENT PRIMARY KEY,
    class_name VARCHAR(50) NOT NULL,
    count INT NOT NULL,
    Currents_date DATE NOT NULL,
    Currents_time TIME NOT NULL
);

CREATE INDEX idx_current_date ON detection_vaccineslog (Currents_date);