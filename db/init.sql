CREATE DATABASE devices;
use devices;

CREATE TABLE device (
  id int,
  alias VARCHAR(255),
  location VARCHAR(255),
  PRIMARY KEY (id)
);
