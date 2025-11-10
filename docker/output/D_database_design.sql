-- =============================================================================
-- BOTOBOX IoT SENSOR MANAGEMENT SYSTEM
-- Database Schema Design
-- =============================================================================

-- 1. TABEL: Locations (Lokasi Hotel/Cabin)
-- =============================================================================
CREATE TABLE Locations (
    Location_ID VARCHAR(10) PRIMARY KEY,
    Location_Name VARCHAR(100) NOT NULL,
    City VARCHAR(50) NOT NULL,
    Type VARCHAR(20) CHECK (Type IN ('Hotel', 'Cabin', 'Pod')),
    Total_Units INT NOT NULL CHECK (Total_Units > 0),
    Address TEXT,
    Created_Date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Last_Updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. TABEL: Units (Unit dalam setiap Location)
-- =============================================================================
CREATE TABLE Units (
    Unit_ID VARCHAR(15) PRIMARY KEY,
    Location_ID VARCHAR(10) NOT NULL,
    Unit_Number VARCHAR(10) NOT NULL,
    Unit_Type VARCHAR(20) CHECK (Unit_Type IN ('Standard', 'Deluxe', 'Suite', 'Pod')),
    Floor INT,
    Capacity INT,
    Status VARCHAR(20) DEFAULT 'Active' CHECK (Status IN ('Active', 'Maintenance', 'Inactive')),
    Created_Date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (Location_ID) REFERENCES Locations(Location_ID) ON DELETE CASCADE,
    UNIQUE (Location_ID, Unit_Number)  

-- 3. TABEL: Sensors (Data semua IoT Sensors)
-- =============================================================================
CREATE TABLE Sensors (
    Sensor_ID VARCHAR(20) PRIMARY KEY,
    Unit_ID VARCHAR(15) NOT NULL,
    Sensor_Type VARCHAR(30) NOT NULL CHECK (Sensor_Type IN (
        'Temperature', 'Humidity', 'Occupancy', 'Motion', 
        'Light', 'Air_Quality', 'Energy', 'Door_Contact'
    )),
    Model VARCHAR(50),
    Manufacturer VARCHAR(50),
    Serial_Number VARCHAR(50) UNIQUE,
    Installation_Date DATE NOT NULL,
    Current_Status VARCHAR(20) DEFAULT 'Active' CHECK (Current_Status IN (
        'Active', 'Inactive', 'Maintenance_Required', 'Faulty', 'Retired'
    )),
    Battery_Level INT CHECK (Battery_Level BETWEEN 0 AND 100),
    Last_Reading TIMESTAMP,
    Created_Date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (Unit_ID) REFERENCES Units(Unit_ID) ON DELETE CASCADE
);

-- 4. TABEL: Engineers (Teknisi/Maintenance Engineers)
-- =============================================================================
CREATE TABLE Engineers (
    Engineer_ID VARCHAR(10) PRIMARY KEY,
    First_Name VARCHAR(50) NOT NULL,
    Last_Name VARCHAR(50) NOT NULL,
    Email VARCHAR(100) UNIQUE,
    Phone VARCHAR(20),
    Department VARCHAR(30) CHECK (Department IN ('IoT', 'Facilities', 'IT', 'General')),
    Employment_Type VARCHAR(20) DEFAULT 'Fulltime' CHECK (Employment_Type IN ('Fulltime', 'Contract', 'Vendor')),
    Hire_Date DATE,
    Status VARCHAR(20) DEFAULT 'Active' CHECK (Status IN ('Active', 'Inactive', 'On_Leave')),
    Created_Date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. TABEL: Maintenance_Records (Riwayat Maintenance Sensors)
-- =============================================================================
CREATE TABLE Maintenance_Records (
    Maintenance_ID SERIAL PRIMARY KEY,  -- Auto-increment
    Sensor_ID VARCHAR(20) NOT NULL,
    Engineer_ID VARCHAR(10) NOT NULL,
    Maintenance_Date DATE NOT NULL,
    Maintenance_Type VARCHAR(30) NOT NULL CHECK (Maintenance_Type IN (
        'Routine_Check', 'Repair', 'Replacement', 'Calibration', 
        'Battery_Replacement', 'Software_Update', 'Emergency'
    )),
    Description TEXT NOT NULL,
    Parts_Replaced TEXT,
    Cost DECIMAL(10,2) CHECK (Cost >= 0),
    Status VARCHAR(20) DEFAULT 'Completed' CHECK (Status IN (
        'Scheduled', 'In_Progress', 'Completed', 'Cancelled'
    )),
    Next_Maintenance_Date DATE,
    Created_Date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (Sensor_ID) REFERENCES Sensors(Sensor_ID) ON DELETE CASCADE,
    FOREIGN KEY (Engineer_ID) REFERENCES Engineers(Engineer_ID)
);

-- 6. TABEL: Sensor_Readings (Data pembacaan sensor - opsional untuk analytics)
-- =============================================================================
CREATE TABLE Sensor_Readings (
    Reading_ID BIGSERIAL PRIMARY KEY,
    Sensor_ID VARCHAR(20) NOT NULL,
    Reading_Time TIMESTAMP NOT NULL,
    Reading_Type VARCHAR(20) NOT NULL,
    Value DECIMAL(10,4) NOT NULL,
    Unit VARCHAR(10) NOT NULL,
    Data_Quality VARCHAR(20) DEFAULT 'Good' CHECK (Data_Quality IN (
        'Good', 'Questionable', 'Error', 'Out_of_Range'
    )),
    
    FOREIGN KEY (Sensor_ID) REFERENCES Sensors(Sensor_ID) ON DELETE CASCADE,
    INDEX idx_reading_time (Reading_Time),  -- Untuk query performa
    INDEX idx_sensor_reading (Sensor_ID, Reading_Time)
);

-- 7. TABEL: Alerts (Sistem alert untuk sensor issues)
-- =============================================================================
CREATE TABLE Alerts (
    Alert_ID SERIAL PRIMARY KEY,
    Sensor_ID VARCHAR(20) NOT NULL,
    Alert_Type VARCHAR(30) NOT NULL CHECK (Alert_Type IN (
        'Battery_Low', 'Sensor_Offline', 'Reading_Anomaly', 
        'Maintenance_Due', 'Hardware_Failure'
    )),
    Alert_Message TEXT NOT NULL,
    Severity VARCHAR(10) CHECK (Severity IN ('Low', 'Medium', 'High', 'Critical')),
    Alert_Time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Acknowledged_By VARCHAR(10),
    Acknowledged_Time TIMESTAMP,
    Status VARCHAR(20) DEFAULT 'Active' CHECK (Status IN ('Active', 'Acknowledged', 'Resolved')),
    
    FOREIGN KEY (Sensor_ID) REFERENCES Sensors(Sensor_ID) ON DELETE CASCADE,
    FOREIGN KEY (Acknowledged_By) REFERENCES Engineers(Engineer_ID)
);