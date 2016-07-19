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
  name TEXT NOT NULL,
  description TEXT DEFAULT NULL,
  settings TEXT DEFAULT NULL,
  public BOOLEAN NOT NULL DEFAULT FALSE,
  active BOOLEAN NOT NULL DEFAULT TRUE
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
  active BOOLEAN DEFAULT TRUE,
  settings TEXT DEFAULT NULL
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
INSERT INTO Sensors (module, class, type, description, unit, settings) VALUES ('sensors.distance', 'GaugeSensor', 'HC-SR04', 'Ultrasonic distance sensor for water gauges', 'cm', '{"trigger_pin": "17", "data_pin": "27"}');
INSERT INTO Sensors (module, class, type, description, unit, settings) VALUES ('sensors.owmrain', 'OwmRainSnow', 'OpenWeatherMap Rain+Snow', 'Sum of rain and snow. Source: OpenWeatherMap', 'mm/3h', '{"apikey": ""}');

-- Default data for notifications
INSERT INTO notifiers (module, class, description, settings, active) VALUES ('notifiers.email', 'EmailNotifier', 'E-Mail', '{"sender": "no-reply@localhost"}', false);
INSERT INTO notifiers (module, class, description, settings, active) VALUES ('notifiers.mqtt', 'MqttNotifier', 'MQTT Broker', NULL, false);
INSERT INTO notifiers (module, class, description, settings, active) VALUES ('notifiers.opensensemap', 'OpenSenseMapNotifier', 'OpenSenseMap', '{"sensebox_id": ""}', false);

INSERT INTO subscribers (notifier, sensor, settings) VALUES (2, 1, NULL);
INSERT INTO subscribers (notifier, sensor, settings) VALUES (3, 1, '{"sensor_id": ""}');
