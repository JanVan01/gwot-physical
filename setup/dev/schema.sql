CREATE EXTENSION postgis;

DROP TABLE IF EXISTS Measurements;
DROP TABLE IF EXISTS Subscribers;
DROP TABLE IF EXISTS Locations;
DROP TABLE IF EXISTS Sensors;
DROP TABLE IF EXISTS Notifiers;

CREATE TABLE Notifiers (
  id SERIAL PRIMARY KEY,
  module TEXT NOT NULL,
  class TEXT NOT NULL,
  description TEXT DEFAULT NULL,
  settings TEXT DEFAULT NULL,
  active BOOLEAN DEFAULT TRUE
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

CREATE TABLE Subscribers (
  id SERIAL PRIMARY KEY,
  notifier INTEGER NOT NULL REFERENCES Notifiers(id),
  sensor INTEGER NOT NULL REFERENCES Sensors(id),
  settings TEXT DEFAULT NULL
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

-- Default data for notifications
INSERT INTO notifiers (id, module, class, description, settings, active) VALUES (1, 'notifiers.email', 'EmailNotifier', 'E-Mail', '{"sender": "no-reply@localhost"}', false);
INSERT INTO notifiers (id, module, class, description, settings, active) VALUES (2, 'notifiers.mqtt', 'MqttNotifier', 'MQTT Broker', NULL, false);
INSERT INTO notifiers (id, module, class, description, settings, active) VALUES (3, 'notifiers.opensensemap', 'OpenSenseMapNotifier', 'OpenSenseMap', '{"sensebox_id": ""}', false);

INSERT INTO subscribers (id, notifier, sensor, settings) VALUES (1, 2, 1, NULL);
INSERT INTO subscribers (id, notifier, sensor, settings) VALUES (2, 3, 1, '{"sensor_id": ""}');