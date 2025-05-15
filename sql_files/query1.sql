USE object_detection;

-- Add date and time columns
ALTER TABLE detection_logs
ADD COLUMN Currents_date DATE,
ADD COLUMN Currents_time TIME;

-- Populate new columns with data from timestamp
UPDATE detection_logs
SET date = DATE(timestamp),
    time = TIME(timestamp);

-- Add index on date for faster queries (optional, replaces idx_timestamp)
CREATE INDEX idx_date ON detection_logs(date);

-- Optional: Drop the timestamp column if no longer needed
ALTER TABLE detection_logs
DROP COLUMN date1,
DROP COLUMN time1;

-- Optional: Drop the old timestamp index if timestamp is removed
DROP INDEX idx_timestamp ON detection_logs;