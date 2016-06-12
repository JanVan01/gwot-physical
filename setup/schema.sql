CREATE EXTENSION postgis;

DROP TABLE IF EXISTS Measurements;
DROP TABLE IF EXISTS Locations;
DROP TABLE IF EXISTS Sensors;
DROP TABLE IF EXISTS Subscribers;

CREATE TABLE Subscribers (
  id SERIAL PRIMARY KEY,
  connector TEXT NOT NULL,
  type TEXT NOT NULL,
  name TEXT NOT NULL,
  confirmed BOOLEAN DEFAULT FALSE
);

CREATE TABLE Locations (
  id SERIAL PRIMARY KEY,
  name TEXT DEFAULT NULL,
  geom GEOMETRY,
  height float NOT NULL
);

CREATE TABLE Sensors (
  id SERIAL PRIMARY KEY,
  module TEXT NOT NULL,
  class TEXT NOT NULL,
  type TEXT NOT NULL,
  description TEXT DEFAULT NULL,
  unit TEXT NOT NULL,
  active BOOLEAN DEFAULT TRUE
);

CREATE TABLE Measurements (
  id SERIAL PRIMARY KEY,
  datetime TIMESTAMP DEFAULT NOW(),
  value FLOAT NOT NULL,
  quality FLOAT DEFAULT NULL,
  sensor INTEGER NOT NULL REFERENCES Sensors(id),
  location INTEGER NOT NULL REFERENCES Locations(id)
);

-- Default data for ultrasonic distance sensor
INSERT INTO Sensors (module, class, type, description, unit) VALUES ('sensors.distance', 'DistanceSensor', 'HC-SR04', 'Ultrasonic distance sensor for water gauges', 'cm');