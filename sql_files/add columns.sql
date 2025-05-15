USE object_detection;

-- Add date and time columns
ALTER TABLE detection_logs
ADD COLUMN current_date DATE,
ADD COLUMN current_time TIME;

-- Populate new columns with data from timestamp
UPDATE detection_logs
SET date = DATE(timestamp),
    time = TIME(timestamp);

-- Add index on date for faster queries
CREATE INDEX idx_date ON detection_logs(date);

-- Optional: Drop timestamp and its index
ALTER TABLE detection_logs
DROP COLUMN timestamp;
DROP INDEX idx_timestamp ON detection_logs;


ALTER TABLE detection_logs
CHANGE COLUMN date current_date DATE;


ALTER TABLE detection_logs
CHANGE COLUMN time current_time TIME;

ALTER TABLE detection_logs
MODIFY COLUMN Currents_date DATE NOT NULL,
MODIFY COLUMN Currents_time TIME NOT NULL;