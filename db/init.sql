CREATE DATABASE devices;
use devices;

CREATE TABLE device (
  id int,
  alias VARCHAR(255),
  location VARCHAR(255),
  PRIMARY KEY (id)
);

CREATE TABLE allowed_location (
  id int AUTO_INCREMENT,
  location VARCHAR(255) ,
  device_id int,
  PRIMARY KEY (id),
  FOREIGN KEY (device_id) REFERENCES device(id)
);
